from ct.models import UnitStatus, NEED_HELP_STATUS, NEED_REVIEW_STATUS, DONE_STATUS, StudentError

from ..models import Message
from fsm.base_fsm_node import BaseFMSNode

is_additional = True

def next_additional_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    """
    Edge method that moves us to right state for next lesson (or END).
    """
    fsm = edge.fromNode.fsm

    if fsmStack.next_point.student_error.status == NEED_HELP_STATUS:
        additionals = Message.objects.filter(is_additional=True,
                                             chat=fsmStack,
                                             timestamp__isnull=True)
    elif fsmStack.next_point.student_error.status in [NEED_REVIEW_STATUS, DONE_STATUS]:
        Message.objects.filter(student_error=fsmStack.next_point.student_error,
                               is_additional=True,
                               chat=fsmStack,
                               timestamp__isnull=True).delete()
        additionals = Message.objects.filter(is_additional=True,
                                             chat=fsmStack,
                                             timestamp__isnull=True)
    if additionals:
        next_message = additionals.order_by('student_error').first()
        fsmStack.state.unitLesson = next_message.content
        if next_message.student_error != fsmStack.next_point.student_error:
            return fsm.get_node('STUDENTERROR')
    else:
        return fsm.get_node('END')
    return edge.toNode


def check_selfassess_and_next_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    fsm = edge.fromNode.fsm

    if not fsmStack.next_point.content.selfeval == 'correct':
        return fsm.get_node('ERRORS')

    return next_additional_lesson(self, edge, fsmStack, request, useCurrent=False, **kwargs)


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

    # node specification data goes here
    title = 'Start This Courselet'
    edges = (
            dict(name='next', toNode='START_MESSAGE', title='View Next Lesson'),
        )


class START_MESSAGE(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'Click continue to get additional materials'
    edges = (
        dict(name='next', toNode='STUDENTERROR', title='View Next Lesson'),
    )

    def _get_message(self, chat, message, current):
        message = Message.objects.create(
            input_type='options',
            text=self.title,
            chat=chat,
            owner=chat.user,
            kind='button',
            is_additional=is_additional
        )
        return message


class STUDENTERROR(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'Additional lessons begin'
    edges = (
        dict(name='next', toNode='RESOLVE', title='View Next Lesson'),
    )

    def _get_message(self, chat, message, current):
        next_unit_lesson = chat.state.unitLesson
        resolve_message = Message.objects.get(
                        contenttype='unitlesson',
                        content_id=next_unit_lesson.id,
                        chat=chat,
                        owner=chat.user,
                        input_type='custom',
                        kind='message',
                        timestamp__isnull=True,
                        is_additional=True)
        message = Message.objects.get_or_create(
                        contenttype='unitlesson',
                        content_id=resolve_message.student_error.errorModel.id,
                        chat=chat,
                        owner=chat.user,
                        student_error=resolve_message.student_error,
                        input_type='options',
                        kind='button',
                        is_additional=True)[0]
        return message


class RESOLVE(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'It is time to answer'
    edges = (
            dict(name='next', toNode='MESSAGE_NODE', title='Go to self-assessment'),
        )

    def _get_message(self, chat, message, current):
        next_unit_lesson = chat.state.unitLesson
        message = Message.objects.get_or_create(
                            contenttype='unitlesson',
                            content_id=next_unit_lesson.id,
                            chat=chat,
                            owner=chat.user,
                            input_type='custom',
                            kind='message',
                            timestamp__isnull=True,
                            is_additional=True)[0]
        return message


class MESSAGE_NODE(BaseFMSNode):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'Choose the degree of your understanding'
    edges = (
        dict(name='next', toNode='GET_RESOLVE', title='Go to self-assessment'),
    )

    def _get_message(self, chat, message, current):
        message = Message.objects.get_or_create(
            chat=chat,
            owner=chat.user,
            text=chat.state.fsmNode.title,
            student_error=message.student_error,
            input_type='custom',
            kind='message',
            is_additional=True)[0]
        return message


class GET_RESOLVE(BaseFMSNode):
    get_path = get_lesson_url
    next_edge = next_additional_lesson

    # node specification data goes here
    title = 'It is time to answer'
    edges = (
            dict(name='next', toNode='RESOLVE', title='Go to self-assessment'),
        )

    def _get_message(self, chat, message, current):
        next_unit_lesson = chat.state.unitLesson
        message = Message.objects.create(
            contenttype='unitlesson',
            content_id=next_unit_lesson.id,
            input_type='options',
            chat=chat,
            owner=chat.user,
            student_error=message.student_error,
            kind='response',
            userMessage=True,
            is_additional=is_additional)
        return message


class END(BaseFMSNode):
    def get_path(self, node, state, request, **kwargs):
        """
        Get URL for next steps in this unit.
        """
        unitStatus = state.get_data_attr('unitStatus')
        return unitStatus.unit.get_study_url(request.path)
    # node specification data goes here
    title = 'Additional lessons completed'
    help = '''You've finished resolving previous Unit.'''

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
        name='additional',
        hideTabs=True,
        title='Take the courselet core lessons',
        pluginNodes=[START, START_MESSAGE, STUDENTERROR, RESOLVE, MESSAGE_NODE, GET_RESOLVE, END],
    )
    return (spec,)
