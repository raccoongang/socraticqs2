from ct.models import UnitStatus, UnitLesson, Lesson, Response
from chat.models import Chat, Message, ChatDivider, UnitError
from fsm.base_fsm_node import BaseFMSNode

is_additional = False

def next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    """
    Edge method that moves us to right state for next lesson (or END).
    """
    fsm = edge.fromNode.fsm
    unitStatus = fsmStack.state.get_data_attr('unitStatus')

    if useCurrent:
        nextUL = unitStatus.get_lesson()
        return edge.toNode
    else:
        nextUL = unitStatus.start_next_lesson()
    if not nextUL:
        unit = fsmStack.state.get_data_attr('unit')
        if unit.unitlesson_set.filter(
            kind=UnitLesson.COMPONENT, order__isnull=True
        ).exists():
            return fsm.get_node('IF_RESOURCES')
        else:
            return fsm.get_node('END')
    else:  # just a lesson to read
        fsmStack.state.unitLesson = nextUL

        return edge.toNode


def next_lesson_after_title(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    """
    Edge method that moves us to right state for next lesson (or END).
    """
    fsm = edge.fromNode.fsm
    unitStatus = fsmStack.state.get_data_attr('unitStatus')
    nextUL = unitStatus.get_lesson()
    if nextUL.is_question():
        return fsm.get_node(name='ASK')
    else:  # just a lesson to read
        return edge.toNode


def check_selfassess_and_next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    fsm = edge.fromNode.fsm

    if not fsmStack.next_point.content.selfeval == 'correct':
        return fsm.get_node('ERRORS')

    return next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs)


def get_lesson_url(self, node, state, request, **kwargs):
    """
    Get URL for any lesson.
    """
    course = state.get_data_attr('course')
    unitStatus = state.get_data_attr('unitStatus')
    ul = unitStatus.get_lesson()
    return ul.get_study_url(course.pk)


class START(BaseFMSNode):
    """
    Initialize data for viewing a courselet, and go immediately
    to first lesson (not yet completed).
    """
    def start_event(self, node, fsmStack, request, **kwargs):
        """
        Event handler for START node.
        """
        unit = fsmStack.state.get_data_attr('unit')
        fsmStack.state.title = 'Study: %s' % unit.title

        try:  # use unitStatus if provided
            unitStatus = fsmStack.state.get_data_attr('unitStatus')
        except AttributeError:  # create new, empty unitStatus
            unitStatus = UnitStatus(unit=unit, user=request.user)
            unitStatus.save()
            fsmStack.state.set_data_attr('unitStatus', unitStatus)
        fsmStack.state.unitLesson = unitStatus.get_lesson()
        return fsmStack.state.transition(
            fsmStack, request, 'next', useCurrent=True, **kwargs
        )

    next_edge = next_lesson
    # node specification data goes here
    title = 'Start This Courselet'
    edges = (
            dict(name='next', toNode='TITLE', title='View Next Lesson'),
        )


class TITLE(BaseFMSNode):
    """
    View a lesson explanation.
    """
    next_edge = next_lesson_after_title
    get_path = get_lesson_url
    # node specification data goes here
    title = 'View an explanation'
    edges = (
        dict(name='next', toNode='LESSON', title='View Next Lesson'),
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
                        is_additional=False)[0]
        return message


class LESSON(BaseFMSNode):
    """
    View a lesson explanation.
    """
    get_path = get_lesson_url
    next_edge = next_lesson
    # node specification data goes here
    title = 'View an explanation'
    edges = (
            dict(name='next', toNode='TITLE', title='View Next Lesson'),
        )

    def _get_message(self, chat, message, current):
        input_type = 'custom'
        next_unit_lesson = chat.state.unitLesson
        kind = next_unit_lesson.lesson.kind
        try:
            unitStatus = chat.state.get_data_attr('unitStatus')
            next_ul = unitStatus.unit.unitlesson_set.get(order=unitStatus.order+1)
            if next_ul and next_ul.lesson.kind in self.SIMILAR_KINDS and kind in self.SIMILAR_KINDS:
                input_type = 'options'
                kind = 'button'
        except UnitLesson.DoesNotExist:
            pass
        return Message.objects.get_or_create(
                contenttype='unitlesson',
                content_id=next_unit_lesson.id,
                chat=chat,
                owner=chat.user,
                input_type=input_type,
                kind=kind,
                is_additional=False)[0]


class ASK(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'View an explanation'
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
            'is_additional': False
        }
        message = Message.objects.create(**_data)
        return message


class GET_ANSWER(BaseFMSNode):
    title = 'It is time to answer'
    edges = (
            dict(name='next', toNode='CONFIDENCE', title='Go to confidence'),
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
            'is_additional': False
        }
        message = Message.objects.create(**_data)
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
                        is_additional=False)[0]
        return message


class GET_CONFIDENCE(BaseFMSNode):
    title = 'Choose confidence'
    edges = (
        dict(name='next', toNode='ASSESS', title='Go to self-assessment'),
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
            is_additional=False,
        )
        message = Message(**_data)
        message.save()
        return message


class ASSESS(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'Assess your answer'
    edges = (
            dict(name='next', toNode='GET_ASSESS', title='Assess yourself'),
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
                        content_id=answer.id,
                        chat=chat,
                        owner=chat.user,
                        kind=answer.kind,
                        is_additional=is_additional)[0]
        return message


class GET_ASSESS(BaseFMSNode):
    get_path = get_lesson_url
    next_edge = check_selfassess_and_next_lesson
    # node specification data goes here
    title = 'Assess your answer'
    edges = (
            dict(name='next', toNode='TITLE', title='View Next Lesson'),
        )

    def get_message(self, chat, message, current):
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
        message = Message(**_data)
        message.save()
        return message


class ERRORS(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'Error options'
    edges = (
            dict(name='next', toNode='GET_ERRORS', title='Choose errors'),
        )

    def _get_message(self, chat, message, current):
        message = Message.objects.get_or_create(
            chat=chat,
            owner=chat.user,
            text='''Below are some common misconceptions. '''
                 '''Select one or more that is similar to your reasoning.''',
            kind='message',
            input_type='custom',
            is_additional=is_additional)[0]
        return message


class GET_ERRORS(BaseFMSNode):
    get_path = get_lesson_url
    next_edge = next_lesson
    # node specification data goes here
    title = 'Classify your error(s)'
    edges = (
            dict(name='next', toNode='TITLE', title='View Next Lesson'),
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

class IF_RESOURCES(BaseFMSNode):
    help = '''Congratulations! You have completed the core lessons for this
              courselet.'''

    title = 'Courselet core lessons completed'
    edges = (
        dict(name='next', toNode='END', title='View Next Lesson'),
    )

    def _get_message(self, chat, message, current):
        if not self.help:
            text = self.get_help(chat.state, request=None)
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


class END(BaseFMSNode):
    # node specification data goes here
    def get_help(self, node, state, request):
        'provide help messages for all views relevant to this stage.'
        unit = state.get_data_attr('unit')
        lessons = list(
            unit.unitlesson_set.filter(
                kind=UnitLesson.COMPONENT, order__isnull=True
            )
        )
        if lessons:
            return '''Please look over the available resources in the side panel.'''
        else:
            return '''Congratulations! You have completed the core lessons for this
                      courselet.'''
    title = 'Courselet core lessons completed'

    def _get_message(self, chat, message, current):
        if not getattr(self, 'help', None):
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
        name='chat',
        hideTabs=True,
        title='Take the courselet core lessons',
        pluginNodes=[
            START,
            TITLE,
            LESSON,
            ASK,
            GET_ANSWER,
            CONFIDENCE,
            GET_CONFIDENCE,
            ASSESS,
            GET_ASSESS,
            ERRORS,
            GET_ERRORS,
            IF_RESOURCES,
            END
        ],

    )
    return (spec,)
