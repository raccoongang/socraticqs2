from chat.models import Message, UnitError
from ct.models import UnitStatus, UnitLesson, Response
from fsm.base_fsm_node import BaseFMSNode
from fsm.mixins import SIMILAR_KINDS


is_additional = True

def next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    """
    Edge method that moves us to right state for next lesson (or END).
    """
    fsm = edge.fromNode.fsm
    nextUL = fsmStack.state.unitLesson
    if nextUL.is_question():
        return fsm.get_node(name='ASK')
    else:  # just a lesson to read
        return edge.toNode


def check_selfassess_and_next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    fsm = edge.fromNode.fsm

    if not fsmStack.next_point.content.selfeval == 'correct':
        return fsm.get_node('ERRORS')

    return edge.toNode


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
        fsmStack.state.unitLesson = kwargs['unitlesson']
        return fsmStack.state.transition(
            fsmStack, request, 'next', useCurrent=True, **kwargs
        )

    next_edge = next_lesson
    # node specification data goes here
    title = 'Start This Courselet'
    edges = (
            dict(name='next', toNode='LESSON', title='View Next Lesson'),
        )


class LESSON(BaseFMSNode):
    """
    View a lesson explanation.
    """
    get_path = get_lesson_url
    # node specification data goes here
    title = 'View an explanation'
    edges = (
            dict(name='next', toNode='END', title='View Next Lesson'),
        )

    def _get_message(self, chat, message, current):
        input_type = 'custom'
        next_unit_lesson = chat.state.unitLesson
        kind = next_unit_lesson.lesson.kind
        try:
            if is_additional:
                raise UnitLesson.DoesNotExist
            unitStatus = chat.state.get_data_attr('unitStatus')
            next_ul = unitStatus.unit.unitlesson_set.get(order=unitStatus.order+1)
            if next_ul and next_ul.lesson.kind in SIMILAR_KINDS and kind in SIMILAR_KINDS:
                input_type = 'options'
                kind = 'button'
        except UnitLesson.DoesNotExist:
            pass
        message = Message.objects.get_or_create(
                        contenttype='unitlesson',
                        content_id=next_unit_lesson.id,
                        chat=chat,
                        owner=chat.user,
                        input_type=input_type,
                        kind=kind,
                        is_additional=True)[0]
        return message


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
            'is_additional': is_additional
        }
        message = Message(**_data)
        message.save()
        return message


class GET_ANSWER(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'It is time to answer'
    edges = (
            dict(name='next', toNode='ASSESS', title='Go to self-assessment'),
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
            dict(name='next', toNode='END', title='View Next Lesson'),
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
        # if not self.fsm.name == 'live_chat':
        #     message = Message.objects.get_or_create(**_data)[0]
        # else:
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
    # node specification data goes here
    title = 'Classify your error(s)'
    edges = (
            dict(name='next', toNode='END', title='View Next Lesson'),
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
    title = 'Courselet resource lessons completed'
    help = '''Congratulations!  You have completed one of the resources,
    now you can try some more resources from the sidebar.'''

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
        name='resource',
        hideTabs=True,
        title='Take the courselet core lessons',
        pluginNodes=[START, LESSON, ASK, GET_ANSWER,
                     ASSESS, GET_ASSESS, ERRORS,
                     GET_ERRORS, END],
    )
    return (spec,)
