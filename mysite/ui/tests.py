import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from ct.models import Course, Lesson, Concept, UnitLesson, Unit


class UnitsTests(TestCase):
    """
    Tests for GET and only GET for
    'ui:units-list' API.
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
        result = self.client.post(reverse('ui:units-list'), {'key': 'value'})
        self.assertEqual(result.status_code, 405)

    def test_only_auth_users(self):
        """
        Test that API allowed only for logged in users.
        """
        result = self.client.get(reverse('ui:units-list'))
        self.assertEqual(result.status_code, 403)

    def test_positive_case(self):
        """
        Check positive case for logged in user.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:units-list'), {'course_id': self.course.id})
        self.assertEqual(result.status_code, 200)

    def test_check_result_content(self):
        """
        Test result content returned by API.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:units-list'), {'course_id': self.course.id})
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

    def test_get_put_allowed(self):
        """
        Test that only GET and PUT http method is allowed.
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
        ul_lesson = self.lesson.unitlesson_set.first()
        result = self.client.put(
            reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}),
            data='{"ul_id": %s}' % ul_lesson.id,
            content_type='application/json'
        )
        self.assertEqual(result.status_code, 200)

    def test_handling_order_as_string(self):
        """
        Test that if we will send order as a string nothing fails.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}))
        self.assertEqual(result.status_code, 200)
        ul_lesson = self.lesson.unitlesson_set.first()
        result = self.client.put(
           reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}),
           data='{"ul_id": "%s", "order": "0"}' % ul_lesson.id,
           content_type='application/json'
        )
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

    def test_put_append_into_order(self):
        """
        Testing appending UnitLesosn into particular order.
        """
        self.client.login(username='username', password='top_secret')
        self.unit2 = self.course.create_unit(title='unit_title_2', author=self.user)
        self.lesson2 = self.unit.create_lesson(
            title='test_lesson_title_2', author=self.user, text='test_text_2'
        )
        ul_lesson = self.lesson.unitlesson_set.first()
        result = self.client.put(
            reverse('ui:unit_content', kwargs={'unit_id': self.unit.id}),
            data='{"ul_id": %s}' % ul_lesson.id,
            content_type='application/json'
        )
        self.assertEqual(result.status_code, 200)
        res = {u'lessons': [{u'lesson_title': u'test_lesson_title', u'id': 1, u'order': 0},
                            {u'id': 3, u'lesson_title': u'test_lesson_title_2', u'order': 1}],
               u'concepts': [{u'title': u'test_concept_title', u'ul_id': 2}],
               u'id': 1}
        self.assertEqual(json.loads(result.content), res)


class CourseAPIUnitsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='username', password='top_secret')
        self.course = Course(title='title', description='description', addedBy=self.user)
        self.course.save()

    def test_positive_case(self):
        """
        Check positive case for logged in user.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:course_list'))
        self.assertEqual(result.status_code, 200)

    def test_check_result_content(self):
        """
        Test result content returned by API.
        """
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:course_list'))
        self.assertEqual(json.loads(result.content), [{'id': 1, 'title': 'title'}])


class LessonContentAPIUnitsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='username', password='top_secret')
        self.course = Course(title='title', description='description', addedBy=self.user)
        self.course.save()
        self.unit = Unit(title='TestUnit', addedBy=self.user)
        self.unit.save()
        self.lesson = Lesson(title='Test_title', text='Test', addedBy=self.user)
        self.lesson.save_root()
        self.ul = UnitLesson.create_from_lesson(lesson=self.lesson, unit=self.unit)
        self.ul.save()

    def test_get_list_lesson_case(self):
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:lessons-list') + '?unit_id=%s' % self.unit.id)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(json.loads(result.content), list)


class ConceptContentAPIUnitsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='username', password='top_secret')
        self.course = Course(title='title', description='description', addedBy=self.user)
        self.course.save()
        self.unit = Unit(title='TestUnit', addedBy=self.user)
        self.unit.save()
        self.lesson = Lesson(title='Test_title', text='Test', addedBy=self.user)
        self.lesson.save_root()
        self.ul = UnitLesson.create_from_lesson(lesson=self.lesson, unit=self.unit)
        self.ul.save()

    def test_get_list_concept_case(self):
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:concepts-list'))
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(json.loads(result.content), list)


class SearchUnitLessonTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='top_secret')
        self.client.login(username='username', password='top_secret')
        l1 = Lesson(title='A resolution', text='now I get it', addedBy=self.user)
        l1.save_root()
        l2 = Lesson(title='Test find', text='try to find me', addedBy=self.user)
        l2.save_root()
        l3 = Lesson(title='Not to find', text='you must never see me', addedBy=self.user)
        l3.save_root()
        self.unit = Unit(title='My Courselet', addedBy=self.user)
        self.unit.save()
        ul = UnitLesson.create_from_lesson(lesson=l1, unit=self.unit)
        ul.save()
        ul = UnitLesson.create_from_lesson(lesson=l2, unit=self.unit)
        ul.save()
        ul = UnitLesson.create_from_lesson(lesson=l3, unit=self.unit)
        ul.save()

    def test_rest_for_search(self):
        response = self.client.get('/ui/api/search/?format=json&text=find me')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test find')
        self.assertNotContains(response, 'Not to find')


class CourseInfoAPIUnitsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='username', password='top_secret')
        self.course = Course(title='title', description='description', addedBy=self.user)
        self.course.save()

    def test_get_course_info(self):
        self.client.login(username='username', password='top_secret')
        result = self.client.get(reverse('ui:courses-detail', kwargs={'pk': self.course.id}))
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(json.loads(result.content), dict)
        self.assertEqual(
            json.loads(result.content),
            {
                'description': u'description',
                'added_by': u'username',
                'title': u'title',
                'addedBy': self.user.id,
                'id': self.course.id
            }
        )
