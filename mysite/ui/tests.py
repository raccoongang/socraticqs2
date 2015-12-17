import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from ct.models import Course, Lesson, Concept, UnitLesson


class CourseUnitsTests(TestCase):
    """
    Tests for GET and only GET for
    'ui:units_list' API.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='username', password='top_secret')
        self.course = Course(title='test_title', description='test_description', addedBy=self.user)
        self.course.save()
        self.unit = self.course.create_unit(title='unit_title', author=self.user)

    def test_only_get_allowed(self):
        """
        Test that only GET http method is allowed.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.post(reverse('ui:units_list', kwargs={'course_id': self.course.id}), {'key': 'value'})
        self.assertEqual(result.status_code, 405)

    def test_only_auth_users(self):
        """
        Test that API allowed only for logged in users.
        """
        result = self.client.get(reverse('ui:units_list', kwargs={'course_id': self.course.id}))
        self.assertEqual(result.status_code, 403)

    def test_positive_case(self):
        """
        Check positive case for logged in user.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:units_list', kwargs={'course_id': self.course.id}))
        self.assertEqual(result.status_code, 200)

    def test_check_result_content(self):
        """
        Test result content returned by API.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:units_list', kwargs={'course_id': self.course.id}))
        self.assertEqual(
            json.loads(result.content),
            [
                {
                    u'unit_id': self.unit.id,
                    u'unit_title': self.unit.title,
                    u'order': self.unit.courseunit_set.first().order
                }
            ]
        )


class UnitContentTests(TestCase):
    """
    Tests for GET and only GET for
    'ui:unit_content' API.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='username', password='top_secret')
        self.course = Course(title='test_title', description='test_description', addedBy=self.user)
        self.course.save()
        self.unit = self.course.create_unit(title='unit_title', author=self.user)
        self.lesson = self.unit.create_lesson(
            title='test_lesson_title', author=self.user, text='test_text'
        )
        self.concept = Concept(title='test_concept_title', addedBy=self.user)
        self.concept.save()
        self.lesson_concept = Lesson(title='test_lesson_for_concept', addedBy=self.user, concept=self.concept)
        self.lesson_concept.save_root()
        self.ul_lesson_for_concept = UnitLesson.create_from_lesson(lesson=self.lesson_concept, unit=self.unit)

    def test_only_get_allowed(self):
        """
        Test that only GET http method is allowed.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.post(reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}), {'key': 'value'})
        self.assertEqual(result.status_code, 405)

    def test_only_auth_users(self):
        """
        Test that API allowed only for logged in users.
        """
        result = self.client.get(reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}))
        self.assertEqual(result.status_code, 403)

    def test_positive_case(self):
        """
        Check positive case for logged in user.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}))
        self.assertEqual(result.status_code, 200)

    def test_check_result_content(self):
        """
        Test result content returned by API.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}))
        ul_lesson = self.lesson.unitlesson_set.first()
        self.assertEqual(
            json.loads(result.content),
            {
                u'id': self.unit.id,
                u'lessons': [
                    {
                        u'id': ul_lesson.id,
                        u'lesson_title': self.lesson.title,
                        u'order': ul_lesson.order
                    }
                ],
                u'concepts': [
                    {
                        u'ul_id': self.ul_lesson_for_concept.id,
                        u'title': self.concept.title
                    }
                ]
            }
        )
