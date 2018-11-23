"""
Test core utility functions.
"""
import mock
from ddt import ddt, data, unpack
from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase

from core.common.utils import send_email, get_onboarding_percentage
from core.common import onboarding
from core.common.utils import get_onboarding_setting, ONBOARDING_STEPS_DEFAULT_TEMPLATE, \
    get_onboarding_status_with_settings


@ddt
class UtilityTest(TestCase):
    """
    Test auxiliary functions.
    """

    def test_send_email(self):
        """
        Test email sending.

        Ensure an email has proper subject and body.
        """
        send_email(
            context_data={
                "milestone": "first",
                "students_number": 2,
                "course_title": "Test Course",
                "lesson_title": "Test Lesson",
                "current_site": Site.objects.get_current(),
                "course_id": 1,
                "unit_lesson_id": 1,
                "courselet_pk": 1
            },
            from_email=settings.EMAIL_FROM,
            to_email=["test@example.com"],
            template_subject="ct/email/milestone_ortc_notify_subject",
            template_text="ct/email/milestone_ortc_notify_text"
        )

        self.assertEqual(len(mail.outbox), 1)

        # FIXME: outbox properties do not get overridden
        # self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_FROM)
        # self.assertEqual(mail.outbox[0].to, "test@example.com")
        # self.assertContains(mail.outbox[0].subject, "2")
        # self.assertContains(mail.outbox[0].subject, "first")
        # self.assertContains(mail.outbox[0].body, "first")
        # self.assertContains(mail.outbox[0].body, "2")
        # self.assertContains(mail.outbox[0].body, "Test Course")
        # self.assertContains(mail.outbox[0].body, "Test Lesson")

    @mock.patch('core.common.utils.c_onboarding_status')
    @unpack
    @data(
        ({onboarding.STEP_1: 0, onboarding.STEP_2: 0, onboarding.STEP_3: 0, onboarding.STEP_4: 0, onboarding.STEP_5: 0, onboarding.STEP_6: 0, onboarding.STEP_7: 0}, 0),
        ({onboarding.STEP_1: 1, onboarding.STEP_2: 0, onboarding.STEP_3: 0, onboarding.STEP_4: 0, onboarding.STEP_5: 0, onboarding.STEP_6: 0, onboarding.STEP_7: 0}, 14.0),
        ({onboarding.STEP_1: 0, onboarding.STEP_2: 1, onboarding.STEP_3: 0, onboarding.STEP_4: 0, onboarding.STEP_5: 0, onboarding.STEP_6: 1, onboarding.STEP_7: 1}, 43.0),
        ({onboarding.STEP_1: 0, onboarding.STEP_2: 0, onboarding.STEP_3: 1, onboarding.STEP_4: 1, onboarding.STEP_5: 1, onboarding.STEP_6: 1, onboarding.STEP_7: 0}, 57.0),
        ({onboarding.STEP_1: 1, onboarding.STEP_2: 0, onboarding.STEP_3: 1, onboarding.STEP_4: 1, onboarding.STEP_5: 1, onboarding.STEP_6: 1, onboarding.STEP_7: 1}, 86.0),
        ({onboarding.STEP_1: 1, onboarding.STEP_2: 1, onboarding.STEP_3: 1, onboarding.STEP_4: 1, onboarding.STEP_5: 1, onboarding.STEP_6: 1, onboarding.STEP_7: 1}, 100.0)
    )
    def test_percentage_of_done(self, steps, result, mock):
        _mock = mock.return_value
        _mock.find_one.return_value = steps
        self.assertEqual(get_onboarding_percentage(1), result)

    @mock.patch('core.common.utils.c_onboarding_status')
    @unpack
    @data(
        (onboarding.INTRODUCTION_COURSE_ID, settings.ONBOARDING_INTRODUCTION_COURSE_ID),
        (onboarding.VIEW_INTRODUCTION, ONBOARDING_STEPS_DEFAULT_TEMPLATE),
        (onboarding.INTRODUCTION_INTRO, ONBOARDING_STEPS_DEFAULT_TEMPLATE),
        (onboarding.CREATE_COURSE, ONBOARDING_STEPS_DEFAULT_TEMPLATE),
        (onboarding.CREATE_COURSELET, ONBOARDING_STEPS_DEFAULT_TEMPLATE),
        (onboarding.CREATE_THREAD, ONBOARDING_STEPS_DEFAULT_TEMPLATE),
        (onboarding.INVITE_SOMEBODY, ONBOARDING_STEPS_DEFAULT_TEMPLATE),
        (onboarding.REVIEW_ANSWERS, ONBOARDING_STEPS_DEFAULT_TEMPLATE),
        # nonexistent key
        ('fake_key', None)
    )
    def test_get_onboarding_setting(self, setting_name, value, _mock):
        self.assertEqual(get_onboarding_setting(setting_name), value)

    @mock.patch('core.common.utils.get_onboarding_setting')
    @mock.patch('core.common.utils.c_onboarding_status')
    def test_get_onboarding_status_with_settings(self, status_mock, settings_mock):

        def mocked_setting(setting_name):
            data = {
                "instructor_intro": {
                    "html": "<p>instructor_intro</p>",
                    "description": "instructor_intro desc",
                    "title": "instructor_intro"
                },
                "create_course": {
                    "html": "<p>create_course</p>",
                    "description": "create_course desc",
                    "title": "create_course"
                },
                "create_courselet": {
                    "html": "<p>create_courselet</p>",
                    "description": "create_courselet desc",
                    "title": "create_courselet"
                },
                "review_answers": {
                    "html": "<p>review_answers</p>",
                    "description": "review_answers desc",
                    "title": "review_answers"
                },
                "invite_somebody": {
                    "html": "<p>invite_somebody</p>",
                    "description": "invite_somebody desc",
                    "title": "invite_somebody"
                },
                "create_thread": {
                    "html": "<p>create_thread</p>",
                    "description": "create_thread desc",
                    "title": "create_thread"
                },
                "view_introduction": {
                    "html": "<p>view_introduction</p>",
                    "description": "view_introduction desc",
                    "title": "view_introduction"
                }
            }
            return data[setting_name]

        expected_result = {
            "instructor_intro": {
                "done": False,
                "settings": {
                    "html": "<p>instructor_intro</p>",
                    "description": "instructor_intro desc",
                    "title": "instructor_intro"
                }
            },
            "create_course": {
                "done": True,
                "settings": {
                    "html": "<p>create_course</p>",
                    "description": "create_course desc",
                    "title": "create_course"
                }
            },
            "create_courselet": {
                "done": False,
                "settings": {
                    "html": "<p>create_courselet</p>",
                    "description": "create_courselet desc",
                    "title": "create_courselet"
                }
            },
            "review_answers": {
                "done": False,
                "settings": {
                    "html": "<p>review_answers</p>",
                    "description": "review_answers desc",
                    "title": "review_answers"
                }
            },
            "invite_somebody": {
                "done": True,
                "settings": {
                    "html": "<p>invite_somebody</p>",
                    "description": "invite_somebody desc",
                    "title": "invite_somebody"
                }
            },
            "create_thread": {
                "done": False,
                "settings": {
                    "html": "<p>create_thread</p>",
                    "description": "create_thread desc",
                    "title": "create_thread"
                }
            },
            "view_introduction": {
                "done": False,
                "settings": {
                    "html": "<p>view_introduction</p>",
                    "description": "view_introduction desc",
                    "title": "view_introduction"
                }
            }
        }
        status_mock = status_mock.return_value
        status_mock.find_one.return_value = {
            onboarding.VIEW_INTRODUCTION: False,
            onboarding.INTRODUCTION_INTRO: False,
            onboarding.CREATE_COURSE: True,
            onboarding.CREATE_COURSELET: False,
            onboarding.CREATE_THREAD: False,
            onboarding.INVITE_SOMEBODY: True,
            onboarding.REVIEW_ANSWERS: False
        }
        settings_mock.side_effect = mocked_setting
        user_id = 1  # value doesn't matter
        data = get_onboarding_status_with_settings(user_id)
        self.assertEqual(data, expected_result)
