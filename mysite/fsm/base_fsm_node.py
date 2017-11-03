from chat.models import Message
from ct.models import UnitStatus, UnitLesson, Lesson, Response
# from chat.models import Chat, Message, ChatDivider, UnitError
import logging
import re
from functools import partial


class BaseFMSNode(object):
    """
    Base class for all FSM nodes which implements logic to get html (get_html method), get options (get_options)
    and get input (get_input).
    """
    WAIT_NODES_REGS = [r"^WAIT_(?!ASSESS$).*$", r"^RECYCLE$"]
    SIMILAR_KINDS = (Lesson.BASE_EXPLANATION, Lesson.EXPLANATION)

    def get_html(self, message):
        pass

    def get_options(self, message):
        pass

    def get_input(self, message):
        pass

    def _get_message(self, chat, message, current):
        return

    @staticmethod
    def is_wait_node(name):
        return any(
            map(partial(re.search, string=name), BaseFMSNode.WAIT_NODES_REGS)
        )

    def _get_wait_msg(self, chat, message, current, *args, **kwargs):
        """
        Return message for WAIT_* nodes.
        :param chat: chat instance
        :param message: message
        :param current: current msg
        :param args: *
        :param kwargs: **
        :return: message
        """
        lookup = dict(
            chat=chat,
            text=self.title,
            kind='button',
            is_additional=False,
            owner=chat.user
        )
        message = Message.objects.get_or_create(**lookup)[0]
        return message

    def get_message(self, chat, message, current):
        """
        This method return message for current FSM node.
        :param chat: chat instance
        :param message: message
        :param current: current message
        :return: new message or old one.
        """
        new_msg = self._get_message(chat, message, current)
        if not hasattr(self, '_get_message'):
            if self.is_wait_node(self.name):
                return self._get_wait_msg(chat, message, current)
            logging.error("Node {} doesn't have _get_message method. Skipping it...".format(self.__class__.__name__))
        if not new_msg:
            return message
        else:
            return new_msg