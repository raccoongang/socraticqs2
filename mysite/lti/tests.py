# coding=utf-8

import json
import pickle
import oauth2

from mock import patch, Mock
from ddt import ddt, data, unpack
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from psa.models import UserSocialAuth
from ct.models import Course, Role, Unit, CourseUnit
from lti.models import LTIUser, CourseRef
from lti.views import clone_course, create_courseref


class LTITestCase(TestCase):
    def setUp(self):
        """Preconditions."""
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'test')

        mocked_nonce = u'135685044251684026041377608307'
        mocked_timestamp = u'1234567890'
        mocked_decoded_signature = u'my_signature='
        self.headers = {
            u'user_id': 1,
            u'lis_person_name_full': u'Test Username',
            u'lis_person_name_given': u'First',
            u'lis_person_name_family': u'Second',
            u'lis_person_contact_email_primary': u'test@test.com',
            u'oauth_callback': u'about:blank',
            u'launch_presentation_return_url': '',
            u'lti_message_type': u'basic-lti-launch-request',
            u'lti_version': 'LTI-1p0',
            u'roles': u'Student',
            u'context_id': 1,
            u'tool_consumer_info_product_family_code': u'moodle',
            u'context_title': u'Test title',
            u'tool_consumer_instance_guid': u'test.dot.com',

            u'resource_link_id': 'dfgsfhrybvrth',
            u'lis_result_sourcedid': 'wesgaegagrreg',

            u'oauth_nonce': mocked_nonce,
            u'oauth_timestamp': mocked_timestamp,
            u'oauth_consumer_key': u'',
            u'oauth_signature_method': u'HMAC-SHA1',
            u'oauth_version': u'1.0',
            u'oauth_signature': mocked_decoded_signature
        }

        self.unit = Unit(title='Test title', addedBy=self.user)
        self.unit.save()
        self.course = Course(title='Test title',
                             description='test description',
                             access='Public',
                             enrollCode='111',
                             lockout='222',
                             addedBy=self.user)
        self.course.save()
        self.course_ref = CourseRef(
            course=self.course, context_id=self.headers.get('context_id'),
            tc_guid=self.headers.get('tool_consumer_instance_guid')
        )
        self.course_ref.save()
        self.course_ref.instructors.add(self.user)

        self.courseunit = CourseUnit(
            unit=self.unit, course=self.course,
            order=0, addedBy=self.user
        )
        self.courseunit.save()


@patch('lti.views.DjangoToolProvider')
class MethodsTest(LTITestCase):
    """Test for correct request method passed in view."""

    def test_post(self, mocked):
        mocked.return_value.is_valid_request.return_value = True
        response = self.client.post('/lti/',
                                    data=self.headers,
                                    follow=True)
        self.assertTemplateUsed(response, template_name='ct/course.html')

    def test_failure_post(self, mocked):
        mocked.return_value.is_valid_request.return_value = False
        response = self.client.post('/lti/',
                                    data=self.headers,
                                    follow=True)
        self.assertTemplateUsed(response, template_name='lti/error.html')

    def test_get(self, mocked):
        mocked.return_value.is_valid_request.return_value = True
        response = self.client.get('/lti/',
                                   follow=True)
        self.assertTemplateUsed(response, template_name='lti/error.html')


@ddt
@patch('lti.views.DjangoToolProvider')
class ParamsTest(LTITestCase):
    """Test different params handling."""

    def test_tool_consumer_info_product_family_code(self, mocked):
        del self.headers[u'tool_consumer_info_product_family_code']
        mocked.return_value.is_valid_request.return_value = True
        self.client.post('/lti/',
                         data=self.headers,
                         follow=True)
        self.assertTrue(LTIUser.objects.filter(consumer='lti').exists())

    @unpack
    @data(('prof', {u'roles': u'Instructor'}),
          ('student', {u'roles': u'Leaner'}))
    def test_roles(self, role, header, mocked):
        self.headers.update(header)
        mocked.return_value.is_valid_request.return_value = True
        self.client.post('/lti/',
                         data=self.headers,
                         follow=True)
        self.assertTrue(Role.objects.filter(role=role).exists())

    def test_user_id(self, mocked):
        del self.headers[u'user_id']
        mocked.return_value.is_valid_request.return_value = True
        response = self.client.post('/lti/',
                                    data=self.headers,
                                    follow=True)
        self.assertTemplateUsed(response, template_name='lti/error.html')

    def test_roles_none(self, mocked):
        del self.headers[u'roles']
        mocked.return_value.is_valid_request.return_value = True
        self.client.post('/lti/',
                         data=self.headers,
                         follow=True)
        self.assertTrue(Role.objects.filter(role='student').exists())

    def test_lti_user(self, mocked):
        """Default LTI user creation process"""
        mocked.return_value.is_valid_request.return_value = True
        self.client.post('/lti/',
                         data=self.headers,
                         follow=True)
        self.assertTrue(LTIUser.objects.filter(consumer='moodle').exists())
        self.assertTrue(Role.objects.filter(role='student').exists())
        self.assertEqual(LTIUser.objects.get(consumer='moodle').django_user,
                         UserSocialAuth.objects.get(
                             uid=self.headers[u'lis_person_contact_email_primary']
                         ).user)
        self.assertEqual(self.user, UserSocialAuth.objects.get(
            uid=self.headers[u'lis_person_contact_email_primary']
        ).user)

    def test_lti_user_no_email(self, mocked):
        del self.headers[u'lis_person_contact_email_primary']
        mocked.return_value.is_valid_request.return_value = True
        self.client.post('/lti/',
                         data=self.headers,
                         follow=True)
        self.assertTrue(LTIUser.objects.filter(consumer='moodle').exists())
        self.assertTrue(Role.objects.filter(role='student').exists())
        self.assertNotEqual(LTIUser.objects.get(consumer='moodle').django_user,
                            User.objects.get(id=1))

    def test_lti_user_no_username_no_email(self, mocked):
        """Test for non-existent username field

        If there is no username in POST
        we create user with username==user_id
        """
        del self.headers[u'lis_person_name_full']
        del self.headers[u'lis_person_contact_email_primary']
        mocked.return_value.is_valid_request.return_value = True
        self.client.post('/lti/',
                         data=self.headers,
                         follow=True)
        self.assertTrue(LTIUser.objects.filter(consumer='moodle').exists())
        self.assertTrue(Role.objects.filter(role='student').exists())
        self.assertNotEqual(LTIUser.objects.get(consumer='moodle').django_user,
                            User.objects.get(id=1))
        self.assertEqual(LTIUser.objects.get(consumer='moodle').
                         django_user.username,
                         LTIUser.objects.get(consumer='moodle').user_id)

    def test_lti_user_link_social(self, mocked):
        """Default LTI user creation process"""
        social = UserSocialAuth(
            user=self.user,
            uid=self.headers[u'lis_person_contact_email_primary'],
            provider='email'
        )
        social.save()
        mocked.return_value.is_valid_request.return_value = True
        self.client.post('/lti/',
                         data=self.headers,
                         follow=True)
        self.assertTrue(LTIUser.objects.filter(consumer='moodle').exists())
        self.assertTrue(Role.objects.filter(role='student').exists())
        self.assertEqual(LTIUser.objects.get(consumer='moodle').django_user,
                         social.user)


@ddt
@patch('lti.views.DjangoToolProvider')
class ExceptionTest(LTITestCase):
    """Test raising exception."""

    @data(oauth2.MissingSignature, oauth2.Error, KeyError, AttributeError)
    def test_exceptions(self, exception, mocked):
        mocked.return_value.is_valid_request.side_effect = exception()
        response = self.client.get('/lti/', follow=True)
        self.assertTemplateUsed(response, template_name='lti/error.html')


class ModelTest(LTITestCase):
    """Test model LTIUser."""

    def test_lti_user(self):
        """Test enrollment process"""
        lti_user = LTIUser(user_id=1,
                           consumer='test_consimer',
                           extra_data=json.dumps(self.headers),
                           django_user=self.user,
                           course_id=1)
        lti_user.save()

        self.assertFalse(lti_user.is_enrolled('student', 1))

        lti_user.enroll('student', 1)
        self.assertTrue(lti_user.is_enrolled('student', 1))

    def test_lti_user_create_links(self):
        """Creating LTIUser without Django user

        Testing Django user creation process.
        """
        lti_user = LTIUser(user_id=1,
                           consumer='test_consimer',
                           extra_data=json.dumps(self.headers),
                           course_id=1)
        lti_user.save()

        self.assertFalse(lti_user.is_linked)
        lti_user.create_links()
        self.assertTrue(lti_user.is_linked)


@ddt
@patch('lti.views.DjangoToolProvider')
class TestCourseRef(LTITestCase):
    """Testing CourseRef object"""
    @unpack
    @data(('Instructor', 'lti/choice-course-source.html'), ('Student', 'ct/index.html'))
    def test_course_ref_roles(self, role, page, mocked):
        """Test different action for different roles"""
        mocked.return_value.is_valid_request.return_value = True
        self.headers['roles'] = role
        self.course_ref.delete()
        response = self.client.post('/lti/', data=self.headers, follow=True)
        self.assertFalse(CourseRef.objects.filter(course=self.course).exists())
        self.assertTemplateUsed(response, page)

    def test_clone_course(self, mocked):
        """Test Course cloning

        Check that Course is cloned correctly
        and CourseUnit entry also cloned correctly.
        """
        cloned_course = clone_course(self.user, self.course)
        self.assertEqual(cloned_course.title, self.course.title)
        self.assertEqual(cloned_course.description, self.course.description)
        self.assertEqual(cloned_course.access, self.course.access)
        self.assertEqual(cloned_course.enrollCode, self.course.enrollCode)
        self.assertEqual(cloned_course.lockout, self.course.lockout)
        self.assertTrue(cloned_course.courseunit_set.all())
        self.assertNotEqual(cloned_course.courseunit_set.first(), self.courseunit)
        self.assertEqual(cloned_course.courseunit_set.first().unit, self.unit)

    def test_create_courseref_only_lti(self, mocked):
        """Test that only LTI is assowed"""
        request = Mock()
        request.session = {}
        res = create_courseref(request)
        self.assertEqual(res.content, 'Only LTI allowed')

    def test_create_courseref_existed_courseref(self, mocked):
        lti_post = {'context_id': '1',
                    'context_title': 'test title',
                    'tool_consumer_instance_guid': 'test.dot.com'}
        request = Mock()
        request.user = self.user
        request.session = {'LTI_POST': pickle.dumps(lti_post)}
        res = create_courseref(request)
        self.assertEqual(res.url, reverse('ct:edit_course', args=(self.course.id,)))

    def test_create_courseref_non_existed_courseref(self, mocked):
        lti_post = {'context_id': '1111',
                    'context_title': 'test title',
                    'tool_consumer_instance_guid': 'test.dot.com'}
        request = Mock()
        request.user = self.user
        request.session = {'LTI_POST': pickle.dumps(lti_post)}
        res = create_courseref(request)
        self.assertEqual(res.url, reverse('ct:edit_course', args=(2,)))


@patch('lti.views.DjangoToolProvider')
class TestUnit(LTITestCase):
    """Testing Unit template rendering"""
    def test_unit_render(self, mocked):
        mocked.return_value.is_valid_request.return_value = True
        response = self.client.post(
            '/lti/unit/1/', data=self.headers, follow=True
        )
        self.assertTemplateUsed(response, 'ct/study_unit.html')


class TestChoiceCourseSourceForm(LTITestCase):
    """Testing render ChoiceCourseForm"""
    def test_get_fail(self):
        """GET must fail due to @login_required decorator"""
        res = self.client.get(reverse('lti:choice_course_source'))
        self.assertRedirects(res, '/login/?next=' + reverse('lti:choice_course_source'))

    def test_get_success(self):
        """GET must be success"""
        self.client.login(username='test', password='test')
        res = self.client.get(reverse('lti:choice_course_source'))
        self.assertTemplateUsed(res, 'lti/choice-course-source.html')
        self.assertIn('id="choice"', res.content)
        self.assertIn('for="choice_0"', res.content)
        self.assertIn('for="choice_1"', res.content)

    def test_post_fail_only_lti(self):
        """POST must fail due to @only_lti decorator"""
        self.client.login(username='test', password='test')
        res = self.client.post(
            reverse('lti:choice_course_source'),
            data={'choice': '0', 'source': '1'}
        )
        self.assertEqual(res.content, 'Only LTI allowed')

    def test_post_fail_no_courseref(self):
        """POST must fail because of no CourseRef is availabe"""
        self.course_ref.instructors.remove(self.user)
        self.client.login(username='test', password='test')
        res = self.client.post(
            reverse('lti:choice_course_source'),
            data={'choice': '0', 'source': '1'}
        )
        self.assertIn('class="errorlist"', res.content)
