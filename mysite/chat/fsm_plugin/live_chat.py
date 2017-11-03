from ct.models import Response
from fsm.base_fsm_node import BaseFMSNode
from chat.models import Message, ChatDivider, UnitError


is_additional = False

def ask_edge(self, edge, fsmStack, request, **kwargs):
    """
    Try to transition to ASK, or WAIT_ASK if not ready.
    """
    fsm = edge.fromNode.fsm
    if not fsmStack.state.linkState:  # instructor detached
        return fsm.get_node('END')
    elif fsmStack.state.linkState.fsmNode.node_name_is_one_of('QUESTION'):  # in progress
        fsmStack.state.unitLesson = fsmStack.state.linkState.unitLesson
        fsmStack.state.save()
        return edge.toNode  # so go straight to asking question
    return fsm.get_node('WAIT_ASK')


def assess_edge(self, edge, fsmStack, request, **kwargs):
    """
    Try to transition to ASSESS, or WAIT_ASSESS if not ready,
    or jump to ASK if a new question is being asked.
    """
    fsm = edge.fromNode.fsm
    if not fsmStack.state.linkState:  # instructor detached
        return fsm.get_node('END')
    elif fsmStack.state.linkState.fsmNode.node_name_is_one_of('QUESTION'):
        if fsmStack.state.unitLesson == fsmStack.state.linkState.unitLesson:
            return fsm.get_node('WAIT_ASSESS')
        else:  # jump to the new question
            fsmStack.state.unitLesson = fsmStack.state.linkState.unitLesson
            fsmStack.state.save()
            return fsm.get_node('TITLE')
    else:
        return edge.toNode  # go to assessment


def get_lesson_url(self, node, state, request, **kwargs):
    """
    Get URL for any lesson.
    """
    course = state.get_data_attr('course')
    unitStatus = state.get_data_attr('unitStatus')
    ul = unitStatus.get_lesson()
    return ul.get_study_url(course.pk)


def check_selfassess_and_next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    fsm = edge.fromNode.fsm

    if not fsmStack.next_point.content.selfeval == 'correct':
        return fsm.get_node('ERRORS')
    return fsm.get_node('WAIT_ASK')
    # return next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs)


def next_edge_teacher_coherent(nodes, fail_node='WAIT_ASK'):
    def wrapp(func):
        def wrapper(self, edge, fsmStack, request, **kwargs):
            if not fsmStack.state or fsmStack.state and not fsmStack.state.linkState:
                return edge.fromNode.fsm.get_node('END')
            if not fsmStack.state.linkState.fsmNode.node_name_is_one_of(*nodes):
                # print "-------> Student in node {} and \n TEACHER in node {}, allowed nodes for teacher {}".format(
                #     fsmStack.state.fsmNode.name,
                #     fsmStack.state.linkState.fsmNode.name,
                #     nodes
                #     )
                return edge.fromNode.fsm.get_node('WAIT_ASK')
            return func(self, edge, fsmStack, request,  **kwargs)
        return wrapper
    return wrapp


class START(BaseFMSNode):
    """
    In this activity you will answer questions
    presented by your instructor in-class.
    """
    def start_event(self, node, fsmStack, request, **kwargs):
        'event handler for START node'
        fsmStack.state.activity = fsmStack.state.linkState.activity
        unit = fsmStack.state.linkState.get_data_attr('unit')
        course = fsmStack.state.linkState.get_data_attr('course')
        fsmStack.state.set_data_attr('unit', unit)
        fsmStack.state.set_data_attr('course', course)
        fsmStack.state.title = 'Live: %s' % unit.title
        return node.get_path(fsmStack.state, request, **kwargs)
    next_edge = ask_edge
    # node specification data goes here
    path = 'fsm:fsm_node'
    title = 'Now Joining a Live Classroom Session'
    edges = (
        dict(name='next', toNode='WAIT_ASK', title='Start answering questions'),
    )

    def _get_message(self, chat, message, current):
        return Message.objects.get_or_create(
            chat=chat,
            text=self.title,
            kind='button',
            is_additional=True,
            owner=chat.user,
        )[0]


class WAIT_ASK(BaseFMSNode):
    """
    The instructor has not assigned the next exercise yet.
    Please wait, and click the Next button when the instructor tells
    you to do so, or when the live classroom session is over.
    """
    next_edge = ask_edge
    # node specification data goes here
    path = 'fsm:fsm_node'
    title = 'Wait for the Instructor to Assign a Question'
    edges = (
        dict(name='next', toNode='TITLE', title='See if question assigned'),
    )


class TITLE(BaseFMSNode):
    """
    View a lesson explanation.
    """
    # get_path = get_lesson_url
    # node specification data goes here
    title = 'View an explanation'
    edges = (
        dict(name='next', toNode='ASK', title='View Next Lesson'),
    )

    def _get_message(self, chat, message, current):
        next_unit_lesson = chat.state.unitLesson
        divider = ChatDivider(text=next_unit_lesson.lesson.title,
                              unitlesson=next_unit_lesson)
        divider.save()
        message = Message.objects.get_or_create(
            contenttype='chatdivider',
            content_id=divider.id,
            input_type='custom',
            type='breakpoint',
            chat=chat,
            owner=chat.user,
            kind='message',
            is_additional=is_additional
        )[0]
        return message


class ASK(BaseFMSNode):
    """
    In this stage you write a brief answer to a conceptual question.
    """
    @next_edge_teacher_coherent(["QUESTION"])
    def next_edge(self, edge, fsmStack, request, response=None, **kwargs):
        if response:
            fsmStack.state.set_data_attr('response', response)
            fsmStack.state.save_json_data()
        return ask_edge(
            self, edge, fsmStack, request, response=response, **kwargs
        )
    # node specification data goes here

    # def next_edge(self, edge, fsmStack, request, response=None, **kwargs):
    #     return edge.toNode
    # next_edge = ask_edge
    path = 'ct:ul_respond'
    title = 'Answer this Question'
    help = """Listen to your instructor's explanation of this question,
    and ask about anything that's unclear about what you're being asked.
    When the instructor tells you to start, think about the question
    for a minute or two, then briefly write whatever answer you
    come up with. """
    edges = (
        dict(name='next', toNode='GET_ANSWER', title='Answer a question'),
    )

    def _get_message(self, chat, message, current):
        next_unit_lesson = chat.state.unitLesson
        _data = {
            'contenttype': 'unitlesson',
            'content_id': next_unit_lesson.id,
            'chat': chat,
            'owner': chat.user,
            'input_type': 'custom',
            'kind': next_unit_lesson.lesson.kind,
            'is_additional': is_additional
        }
        message = Message.objects.get_or_create(**_data)[0]
        return message


class GET_ANSWER(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    next_edge = next_edge_teacher_coherent(["QUESTION", "ANSWER"])(
        lambda self, edge, *args, **kwargs: edge.toNode
    )
    title = 'It is time to answer'
    edges = (
            dict(name='next', toNode='CONFIDENCE', title='Go to self-assessment'),
        )

    def _get_message(self, chat, message, current):
        answer = current.get_answers().first()
        _data = {
            'contenttype': 'response',
            'input_type': 'text',
            'lesson_to_answer': current,
            'chat': chat,
            'owner': chat.user,
            'kind': 'response',
            'userMessage': True,
            'is_additional': is_additional
        }
        message = Message.objects.get_or_create(**_data)[0]
        return message

class CONFIDENCE(BaseFMSNode):
    title = 'Select the level of your confidence?'
    edges = (
        dict(name='next', toNode='GET_CONFIDENCE', title='Go to choosing your confidence'),
    )

    def _get_message(self, chat, message, current):
        # current here is Response instance
        if isinstance(current, Response):
            response_to_chk = current
            answer = current.unitLesson.get_answers().first()
        else:
            response_to_chk = message.response_to_check
            if not message.lesson_to_answer:
                answer = message.response_to_check.unitLesson.get_answers().first()
            else:
                answer = message.lesson_to_answer.get_answers().first()
        message = Message.objects.get_or_create(
                        contenttype='unitlesson',
                        response_to_check=response_to_chk,
                        input_type='custom',
                        text=self.title,
                        chat=chat,
                        owner=chat.user,
                        kind=answer.kind,
                        is_additional=is_additional)[0]
        return message


class GET_CONFIDENCE(BaseFMSNode):
    title = 'Choose confidence'
    edges = (
        dict(name='next', toNode='WAIT_ASSESS', title='Go to self-assessment'),
    )

    def _get_message(self, chat, message, current):
        _data = dict(
            contenttype='response',
            content_id=message.response_to_check.id,
            input_type='options',
            chat=chat,
            owner=chat.user,
            kind='response',
            userMessage=True,
            is_additional=is_additional,
        )
        message = Message.objects.create(**_data)
        return message


class WAIT_ASSESS(BaseFMSNode):
    """
    The instructor has not ended the question period yet.
    Please wait, and click the Next button when the instructor tells
    you to do so, or when the live classroom session is over.
    """
    # next_edge = assess_edge
    # node specification data goes here
    path = 'fsm:fsm_node'
    title = 'Wait for the Instructor to End the Question'
    edges = (
        dict(name='next', toNode='ASSESS', title='See if question done'),
    )

    @next_edge_teacher_coherent(["QUESTION", "ANSWER", "RECYCLE"])
    def next_edge(self, edge, fsmStack, request, response=None, **kwargs):
        if response:
            fsmStack.state.set_data_attr('response', response)
            fsmStack.state.save_json_data()
        return assess_edge(self, edge, fsmStack, request, response=response,
                           **kwargs)

    def _get_message(self, chat, message, current):
        if isinstance(current, Response):
            resp_to_chk = current
        else:
            resp_to_chk = message.response_to_check
        message = Message.objects.get_or_create(
            chat=chat,
            text=self.title,
            kind='button',
            response_to_check=resp_to_chk,
            is_additional=is_additional,
            owner=chat.user,
        )[0]
        return message


class ASSESS(BaseFMSNode):
    """
    In this stage you assess your own answer vs. the correct answer.
    """
    next_edge = next_edge_teacher_coherent(["QUESTION", "ANSWER", "RECYCLE"])(assess_edge)
    # node specification data goes here
    path = 'ct:assess'
    title = 'Assess your answer'
    help = """Listen to your instructor's explanation of the answer,
    then categorize your assessment, and how well you feel you
    understand this concept now. """

    edges = (
        dict(name='next', toNode='GET_ASSESS', title='Assess yourself'),
    )

    def _get_message(self, chat, message, current):
        if isinstance(current, Response):
            response_to_chk = current
            answer = current.unitLesson.get_answers().first()
        else:
            response_to_chk = message.response_to_check
            if not message.lesson_to_answer:
                answer = message.response_to_check.unitLesson.get_answers().first()
            else:
                answer = message.lesson_to_answer.get_answers().first()
        message = Message.objects.get_or_create(
            contenttype='unitlesson',
            response_to_check=response_to_chk,
            input_type='custom',
            content_id=answer.id,
            chat=chat,
            owner=chat.user,
            kind=answer.kind,
            is_additional=is_additional
        )[0]
        return message


class GET_ASSESS(BaseFMSNode):
    get_path = get_lesson_url
    next_edge = next_edge_teacher_coherent(["ANSWER", "RECYCYLE"])(check_selfassess_and_next_lesson)
    # node specification data goes here
    title = 'Assess your answer'
    edges = (
        dict(name='next', toNode='WAIT_ASK', title='View Next Lesson'),
    )

    def _get_message(self, chat, message, current):
        _data = dict(
            contenttype='response',
            content_id=message.response_to_check.id,
            input_type='options',
            chat=chat,
            owner=chat.user,
            kind='response',
            userMessage=True,
            is_additional=is_additional
        )
        message = Message.objects.create(**_data)
        return message


class ERRORS(BaseFMSNode):
    """
    In this stage you assess whether you made any of the common errors for this concept.
    """
    # next_edge = ask_edge
    # node specification data goes here
    title = 'Error options'
    edges = (
        dict(name='next', toNode='GET_ERRORS', title='Choose errors'),
    )
    next_edge = next_edge_teacher_coherent(["ANSWER", "RECYCLE"])(
        lambda self, edge, *args, **kwargs: edge.toNode
    )

    def _get_message(self, chat, message, current):
        message = Message.objects.get_or_create(
            chat=chat,
            owner=chat.user,
            text='''Below are some common misconceptions. '''
                 '''Select one or more that is similar to your reasoning.''',
            kind='message',
            input_type='custom',
            is_additional=is_additional
        )[0]
        return message


class GET_ERRORS(BaseFMSNode):
    get_path = get_lesson_url
    # next_edge = next_lesson
    # node specification data goes here
    title = 'Classify your error(s)'
    edges = (
            dict(name='next', toNode='WAIT_ASK', title='View next question'),
        )
    next_edge = next_edge_teacher_coherent(["ANSWER", "RECYCLE"])(
        lambda self, edge, *args, **kwargs: edge.toNode
    )

    def _get_message(self, chat, message, current):
        uniterror = UnitError.get_by_message(message)
        message = Message.objects.get_or_create(
            contenttype='uniterror',
            content_id=uniterror.id,
            input_type='options',
            chat=chat,
            kind='uniterror',
            owner=chat.user,
            userMessage=False,
            is_additional=is_additional)[0]
        return message


class END(BaseFMSNode):
    # node specification data goes here
    path = 'ct:unit_tasks_student'
    title = 'Live classroom session completed'
    help = '''The instructor has ended the Live classroom session.'''

    def _get_message(self, chat, message, current):
        if not self.help:
            text = chat.state.fsmNode.get_help(chat.state, request=None)
        else:
            text = self.help
        message = Message.objects.get_or_create(
                        chat=chat,
                        owner=chat.user,
                        text=text,
                        input_type='custom',
                        kind='message',
                        is_additional=True)[0]
        return message


def get_specs():
    """
    Get FSM specifications stored in this file.
    """
    from fsm.fsmspec import FSMSpecification
    spec = FSMSpecification(
        name='live_chat',
        hideTabs=True,
        title='Join a Live Classroom Session',
        pluginNodes=[
            START,
            WAIT_ASK,
            TITLE,
            ASK,
            GET_ANSWER,
            CONFIDENCE,
            GET_CONFIDENCE,
            WAIT_ASSESS,
            ASSESS,
            GET_ASSESS,
            ERRORS,
            GET_ERRORS,
            END
        ],
    )
    return (spec,)
