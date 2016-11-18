

def check_selfassess_and_wait_ask(self, edge, fsmStack, request, useCurrent=False, **kwargs):
    fsm = edge.fromNode.fsm

    if fsmStack.next_point.content.selfeval != 'correct':
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

def ask_edge(self, edge, fsmStack, request, **kwargs):
    """
    Try to transition to ASK, or WAIT_ASK if not ready.
    """
    # import ipdb; ipdb.set_trace()
    fsm = edge.fromNode.fsm
    if not fsmStack.state.linkState:  # instructor detached
        return fsm.get_node('END')
    elif fsmStack.state.linkState.fsmNode.name == 'QUESTION':  # in progress
        fsmStack.state.unitLesson = fsmStack.state.linkState.unitLesson
        fsmStack.state.save()
        return edge.toNode  # so go straight to asking question
    return fsm.get_node('WAIT_ASK')


def assess_edge(self, edge, fsmStack, request, **kwargs):
    """
    Try to transition to ASSESS, or WAIT_ASSESS if not ready,
    or jump to ASK if a new question is being asked.
    """
    # import ipdb; ipdb.set_trace()
    fsm = edge.fromNode.fsm
    if not fsmStack.state.linkState:  # instructor detached
        return fsm.get_node('END')
    elif fsmStack.state.linkState.fsmNode.name == 'QUESTION':
        if fsmStack.state.unitLesson == fsmStack.state.linkState.unitLesson:
            return fsm.get_node('WAIT_ASSESS')
        else:  # jump to the new question
            fsmStack.state.unitLesson = fsmStack.state.linkState.unitLesson
            fsmStack.state.save()
            return fsm.get_node('ASK')
    else:
        return edge.toNode  # go to assessment


class START(object):
    """
    In this activity you will answer questions
    presented by your instructor in-class.
    """
    def start_event(self, node, fsmStack, request, **kwargs):
        'event handler for START node'
        if hasattr(fsmStack.state.linkState, 'activity'):
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
    title = 'We are waiting for the first question from teacher'
    edges = (
        dict(name='next', toNode='WAIT_ASK', title='Start answering questions'),
    )


class WAIT_ASK(object):
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
        dict(name='next', toNode='ASK', title='See if question assigned'),
    )


class ASK(object):
    """
    In this stage you write a brief answer to a conceptual question.
    """
    def next_edge(self, edge, fsmStack, request, response=None, **kwargs):
        if response:
            fsmStack.state.set_data_attr('response', response)
            fsmStack.state.save_json_data()
        return assess_edge(self, edge, fsmStack, request, response=response,
                           **kwargs)
    # node specification data goes here
    path = 'ct:ul_respond'
    title = 'Answer this Question'
    help = """Listen to your instructor's explanation of this question,
    and ask about anything that's unclear about what you're being asked.
    When the instructor tells you to start, think about the question
    for a minute or two, then briefly write whatever answer you
    come up with. """
    edges = (
        dict(name='next', toNode='GET_ANSWER', title='Proceed to assessment'),
    )

class GET_ANSWER(object):
    get_path = get_lesson_url
    # node specification data goes here
    title = 'It is time to answer'
    edges = (
            dict(name='next', toNode='WAIT_ASSESS', title='Go to self-assessment'),
        )

class WAIT_ASSESS(object):
    """
    The instructor has not ended the question period yet.
    Please wait, and click the Next button when the instructor tells
    you to do so, or when the live classroom session is over.
    """
    next_edge = assess_edge
    # node specification data goes here
    path = 'fsm:fsm_node'
    title = 'Wait for the Instructor to End the Question'
    edges = (
        dict(name='next', toNode='ASSESS', title='See if question done'),
    )


class ASSESS(object):
    """
    In this stage you assess your own answer vs. the correct answer.
    """
    next_edge = ask_edge
    # node specification data goes here
    path = 'ct:assess'
    title = 'Assess your answer'
    help = """Listen to your instructor's explanation of the answer,
    then categorize your assessment, and how well you feel you
    understand this concept now. """
    edges = (
        dict(name='next', toNode='WAIT_ASK', title='Wait for the next question'),
        dict(name='error', toNode='ERRORS', title='Classify your error'),
    )

class GET_ASSESS(object):
    get_path = get_lesson_url
    next_edge = check_selfassess_and_wait_ask
    # node specification data goes here
    title = 'Assess your answer'
    edges = (
            dict(name='next', toNode='WAIT_ASK', title='View Next Lesson'),
        )

class GET_ERRORS(object):
    get_path = get_lesson_url
    next_edge = ask_edge
    # node specification data goes here
    title = 'Classify your error(s)'
    edges = (
            dict(name='next', toNode='WAIT_ASK', title='View Next Lesson'),
        )

class ERRORS(object):
    """
    In this stage you assess whether you made any of the common errors for this concept.
    """
    next_edge = ask_edge
    # node specification data goes here
    title = 'Classify your error(s)'
    help = """If you have questions about the following common errors,
    you can ask your instructor. """
    edges = (
            dict(name='next', toNode='GET_ERRORS', title='Go to the next question'),
        )


class END(object):
    # node specification data goes here
    path = 'ct:unit_tasks_student'
    title = 'Live classroom session completed'
    help = '''The instructor has ended the Live classroom session.
    See below for suggested next steps for what to study now in
    this courselet.'''


def get_specs():
    """
    Get FSM specifications stored in this file.
    """
    from fsm.fsmspec import FSMSpecification
    spec = FSMSpecification(
        name='live_chat',
        hideTabs=True,
        title='Join a Live Classroom Session',
        pluginNodes=[START, WAIT_ASK, ASK, WAIT_ASSESS, GET_ANSWER, GET_ASSESS, GET_ERRORS, ASSESS, ERRORS, END],
    )
    return (spec,)
