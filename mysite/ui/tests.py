import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from ct.models import Course


class CourseUnitsTests(TestCase):
    """
    Tests for GET and only GET for
    'api/courses/(?P<course_id>\d+)/units/' API.
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
                    'unit_id': self.unit.id,
                    'unit_title': 'unit_title',
                    'order': self.unit.courseunit_set.first().order
                }
            ]
        )
