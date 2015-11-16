"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import pickle

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import NoReverseMatch
from django.http.response import JsonResponse, HttpResponseRedirect
from ct.models import *
from fsm.models import *
from ct import views, ct_util
import time
import urllib

from ddt import ddt, data, unpack
from mock import patch, Mock


class OurTestCase(TestCase):
    def check_post_get(self, url, postdata, urlTail, expected):
        '''do POST and associated redirect to GET.  Check the redirect
        target and GET response content '''
        origin = 'http://testserver'
        if not url.startswith(origin):
            url = origin + url
        response = self.client.post(url, postdata, HTTP_REFERER=url, HTTP_ORIGIN=origin)
        self.assertEqual(response.status_code, 302)
        url = response['Location']
        self.assertTrue(url.endswith(urlTail))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected)
        return url


class ConceptMethodTests(OurTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jacob', email='jacob@_',
                                             password='top_secret')
        self.client.login(username='jacob', password='top_secret')
        self.wikiUser = User.objects.create_user(username='wikipedia', email='wiki@_',
                                             password='top_secret')
        self.unit = Unit(title='My Courselet', addedBy=self.user)
        self.unit.save()

    def test_sourceDB(self):
        'check wikipedia concept retrieval'
        c, lesson = Concept.get_from_sourceDB('New York City', self.user)
        self.assertEqual(c.title, 'New York City')
        self.assertEqual(c.addedBy, self.user)
        self.assertEqual(lesson.addedBy, self.wikiUser)
        self.assertEqual(lesson.concept, c)
        self.assertTrue(lesson.is_committed())
        self.assertEqual(lesson.changeLog, 'initial text from wikipedia')
        self.assertEqual(lesson.sourceDB, 'wikipedia')
        self.assertEqual(lesson.sourceID, 'New York City')
        self.assertIn('City of New York', lesson.text)
        # check that subsequent retrieval uses stored db record
        c2, l2 = Concept.get_from_sourceDB('New York City', self.user)
        self.assertEqual(c2.pk, c.pk)
        self.assertEqual(l2.pk, lesson.pk)
        self.assertIn(c, list(Concept.search_text('new york')))

    def test_sourceDB_temp(self):
        'check wikipedia temporary document retrieval'
        lesson = Lesson.get_from_sourceDB('New York City', self.user,
                                          doSave=False)
        self.assertIn('City of New York', lesson.text) # got the text?
        self.assertEqual(Lesson.objects.count(), 0) # nothing saved?

    def test_wikipedia_view(self):
        'check wikipedia view and concept addition method'
        url = '/ct/teach/courses/1/units/%d/concepts/wikipedia/%s/' \
          % (self.unit.pk, urllib.quote('New York City'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'City of New York')
        self.check_post_get(url, dict(task='add'), '/', 'City of New York')
        ul = UnitLesson.objects.get(lesson__concept__title='New York City',
                                    unit=self.unit) # check UL & concept added
        self.assertTrue(ul in UnitLesson.search_sourceDB('New York City')[0])
        self.assertTrue(ul in UnitLesson.search_sourceDB('New York City',
                                                         unit=self.unit)[0])

    def test_new_concept(self):
        'check standard creation of a concept bound to a UnitLesson'
        title = 'Important Concept'
        text = 'This concept is very important.'
        concept = Concept.new_concept(title, text, self.unit, self.user)
        self.assertEqual(concept.title, title)
        self.assertFalse(concept.isError)
        lesson = Lesson.objects.get(concept=concept)
        self.assertEqual(lesson.text, text)
        self.assertEqual(lesson.kind, Lesson.BASE_EXPLANATION)
        ul = UnitLesson.objects.get(lesson=lesson)
        self.assertIs(ul.order, None)
        self.assertEqual(ul.treeID, lesson.treeID)
        self.assertEqual(ul.kind, UnitLesson.COMPONENT)
        # check creation of error model
        concept = Concept.new_concept(title, text, self.unit, self.user,
                                      isError=True)
        self.assertTrue(concept.isError)
        lesson = Lesson.objects.get(concept=concept)
        self.assertEqual(lesson.kind, Lesson.ERROR_MODEL)
        ul = UnitLesson.objects.get(lesson=lesson)
        self.assertEqual(ul.kind, UnitLesson.MISUNDERSTANDS)

    def test_error_models(self):
        'check creation and copying of error models'
        concept = Concept.new_concept('big', 'idea', self.unit, self.user)
        lesson = Lesson(title='a test', text='a word', addedBy=self.user)
        lesson.save_root(concept)
        ul = UnitLesson.create_from_lesson(lesson, self.unit)
        emUL1 = views.create_error_ul(Lesson(title='oops', addedBy=self.user,
                                    text='foo'), concept, self.unit, ul)
        emUL2 = views.create_error_ul(Lesson(title='oops', addedBy=self.user,
                                    text='foo'), concept, self.unit, ul)
        parent = UnitLesson.objects.get(lesson__concept=concept)
        ulList = concept.copy_error_models(parent)
        self.assertEqual(len(ulList), 2)
        lessons = [ul.lesson for ul in ulList]
        self.assertIn(emUL1.lesson, lessons)
        self.assertIn(emUL2.lesson, lessons)
        self.assertEqual(parent, ulList[0].parent)
        self.assertEqual(parent, ulList[1].parent)
        # test copying parent to a new unit
        unit3 = Unit(title='Another Courselet', addedBy=self.user)
        unit3.save()
        ul3 = parent.copy(unit3, self.user)
        self.assertEqual(ul3.unit, unit3)
        children = list(ul3.get_errors())
        self.assertEqual(len(children), 2)
        lessons = [ul.lesson for ul in children]
        self.assertIn(emUL1.lesson, lessons)
        self.assertIn(emUL2.lesson, lessons)
        # test adding resolution
        reso = Lesson(title='A resolution', text='now I get it',
                      addedBy=self.user)
        resoUL = ul.save_resolution(reso)
        em, resols = ul.get_em_resolutions()
        resols = list(resols)
        self.assertEqual(resols, [resoUL])
        # test linking a lesson as resolution
        other = Lesson(title='A lesson', text='something else',
                       addedBy=self.user)
        other.save_root()
        otherUL = UnitLesson.create_from_lesson(other, self.unit)
        resoUL2 = ul.copy_resolution(otherUL, self.user)
        em, resols = ul.get_em_resolutions()
        resols = list(resols)
        self.assertEqual(resols, [resoUL, resoUL2])
        # check that it prevents adding duplicate resolutions
        resoUL3 = ul.copy_resolution(otherUL, self.user)
        self.assertEqual(resoUL2, resoUL3)
        em, resols = ul.get_em_resolutions()
        resols = list(resols)
        self.assertEqual(resols, [resoUL, resoUL2])

    def test_get_conceptlinks(self):
        'test ConceptLink creation and retrieval'
        concept = Concept.new_concept('bad', 'idea', self.unit, self.user)
        l1 = Lesson(title='ugh', text='brr', addedBy=self.user)
        l1.save_root(concept)
        ul1 = UnitLesson.create_from_lesson(l1, self.unit)
        l2 = Lesson(title='foo', text='bar', addedBy=self.user,
                    kind=Lesson.ORCT_QUESTION)
        l2.save_root(concept)
        ul2 = UnitLesson.create_from_lesson(l2, self.unit)
        # create a second commit of this lesson in a different unit
        l3 = Lesson(title='wunder', text='bar', addedBy=self.user,
                    kind=Lesson.ORCT_QUESTION, treeID=l2.treeID)
        l3.save_root(concept)
        unit3 = Unit(title='Another Courselet', addedBy=self.user)
        unit3.save()
        ul3 = UnitLesson.create_from_lesson(l3, unit3)
        clList = concept.get_conceptlinks(self.unit) # should get l1, l2
        self.assertEqual(len(clList), 2)
        self.assertEqual([cl for cl in clList if cl.lesson == l1][0]
                         .relationship, ConceptLink.DEFINES)
        self.assertEqual([cl for cl in clList if cl.lesson == l2][0]
                         .relationship, ConceptLink.TESTS)
        self.assertEqual(distinct_subset([ul1, ul2, ul3]), [ul1, ul2])


class LessonMethodTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jacob', email='jacob@_',
                                             password='top_secret')
        self.ul = create_question_unit(self.user)
        concept = Concept.new_concept('bad', 'idea', self.ul.unit, self.user)
        self.ul.lesson.concept = concept
        self.ul.lesson.save()
        self.unit2 = Unit(title='My Courselet', addedBy=self.user)
        self.unit2.save()

    def test_creation_treeID(self):
        'treeID properly initialized to default?'
        lesson = Lesson(title='foo', text='bar', addedBy=self.user)
        lesson.save_root()
        l2 = Lesson.objects.get(pk=lesson.pk)
        self.assertEqual(l2.treeID, l2.pk)

    def test_search_sourceDB(self):
        'check wikipedia search'
        results = Lesson.search_sourceDB('new york city')
        self.assertTrue(len(results) >= 10)
        self.assertIn('New York City', [t[0] for t in results])
        self.assertEqual(len(results[0]), 3)

    def test_checkout(self):
        'check Lesson commit and checkout'
        self.assertFalse(self.ul.lesson.is_committed())
        self.ul.lesson.conceptlink_set.create(concept=self.ul.lesson.concept,
                                              addedBy=self.user)
        ul2 = self.ul.copy(self.unit2, self.user)  # copy to new unit
        self.assertTrue(self.ul.lesson.is_committed())
        self.assertEqual(self.ul.lesson, ul2.lesson)
        self.assertEqual(self.ul.lesson.changeLog, 'snapshot for fork by jacob')
        self.assertNotEqual(self.ul.pk, ul2.pk)
        self.assertEqual(ul2.lesson.title, self.ul.lesson.title)
        lesson = ul2.checkout(self.user)
        self.assertEqual(lesson.title, self.ul.lesson.title)
        lesson.text = 'Big bad wolf'
        lesson.changeLog = 'why I changed everything'
        ul2.checkin(lesson)
        ul2b = UnitLesson.objects.get(pk=ul2.pk)
        self.assertEqual(ul2b.lesson.title, self.ul.lesson.title)
        self.assertEqual(ul2b.lesson.concept, self.ul.lesson.concept)
        self.assertEqual(ul2b.lesson.text, 'Big bad wolf')
        self.assertFalse(self.ul.lesson.pk == ul2b.lesson.pk)
        self.assertEqual(Concept.objects.get(conceptlink__lesson__unitlesson=ul2b),
                         self.ul.lesson.concept)
        self.assertTrue(ul2b.lesson.is_committed())


class FakeRequest(object):
    'trivial holder for request data to pass to test calls'
    def __init__(self, user, sessionDict=None, method='POST', dataDict=None,
                 path='/ct/somewhere/'):
        self.user = user
        self.path = path
        self.method = method
        if not sessionDict:
            sessionDict = {}
        self.session = sessionDict
        if not dataDict:
            dataDict = {}
        setattr(self, method, dataDict)


def create_question_unit(user, utitle='Ask Me some questions',
                         qtitle='What is your quest?',
                         text="(That's a rather personal question.)"):
    unit = Unit(title=utitle, addedBy=user)
    unit.save()
    question = Lesson(title=qtitle, text=text,
                      kind=Lesson.ORCT_QUESTION, addedBy=user)
    question.save_root()
    ul = UnitLesson.create_from_lesson(question, unit, addAnswer=True,
                                       order='APPEND')
    return ul


class ReversePathTests(TestCase):
    def test_home(self):
        'test trimming of args not needed for target'
        url = ct_util.reverse_path_args('ct:home',
                        '/ct/teach/courses/21/units/33/errors/2/')
        self.assertEqual(url, reverse('ct:home'))

    def test_ul_teach(self):
        'check proper extraction of args from path'
        url = ct_util.reverse_path_args('ct:ul_teach',
                        '/ct/teach/courses/21/units/33/errors/2/')
        self.assertEqual(url, reverse('ct:ul_teach', args=(21, 33, 2)))

    def test_ul_id(self):
        'test handling of ID kwargs'
        url = ct_util.reverse_path_args('ct:ul_teach',
                        '/ct/teach/courses/21/units/33/', ul_id=2)
        self.assertEqual(url, reverse('ct:ul_teach', args=(21, 33, 2)))


class PageDataTests(TestCase):
    def test_refresh_timer(self):
        'check refresh timer behavior'
        request = FakeRequest(None)
        pageData = views.PageData(request)
        pageData.set_refresh_timer(request)
        s = pageData.get_refresh_timer(request)
        self.assertEqual(s, '0:00')
        time.sleep(2)
        s = pageData.get_refresh_timer(request)
        self.assertNotEqual(s, '0:00')
        self.assertEqual(s[:3], '0:0')


@ddt
class EnrollTests(TestCase):
    """
    Enroll/Unenroll tests for Course enrollment actions.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')
        self.course = Course(title='test title', description='test descr', addedBy=self.user)
        self.course.save()

    def test_only_post_allowed(self):
        """
        Test for POST checking.
        """
        result = self.client.get(
            reverse('ct:enroll', kwargs={'course_id': self.course.id, 'action': 'enroll'})
        )
        self.assertEqual(result.status_code, 405)

    def test_check_not_ajax(self):
        """
        View should return HttpResponseForbidden('Only Ajax Allowed')
        for non Ajax requests.
        """
        result = self.client.post(
            reverse('ct:enroll', kwargs={'course_id': self.course.id, 'action': 'enroll'}),
            {'role': 'test_role'}
        )
        self.assertContains(result, 'Only Ajax Allowed', status_code=403)

    @data(
        {},
        {'course_id': 1},
        {'action': 'enroll'},
        {'course_id': 'String'},
        {'action': 'wrong_action'}
    )
    def test_improperly_configured_url(self, url_data):
        """
        Test for incorrect url reversing.
        """
        with self.assertRaises(NoReverseMatch):
            self.client.post(
                reverse('ct:enroll', kwargs=url_data),
                {'role': 'test_role'},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )

    @data({}, {'role': 'wrong_role'})
    def test_improperly_configured_post_data(self, post_data):
        """
        Check for improperly configured request.
        """
        result = self.client.post(
            reverse('ct:enroll', kwargs={'course_id': self.course.id, 'action': 'enroll'}),
            post_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertContains(result, 'Improperly configured request', status_code=400)

    def test_request_on_non_existent_course(self):
        """
        Test case where Course does not exists.
        """
        url_data = {'course_id': self.course.id, 'action': 'enroll'}
        self.course.delete()
        result = self.client.post(
            reverse('ct:enroll', kwargs=url_data),
            {'role': Role.ENROLLED},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(result.status_code, 400)

    @patch('ct.views.PartialEnroll.add_partial', return_value='test_token')
    def test_not_authenticated_user(self, add_partial):
        """
        Check that view return status 401 and partial_url to complete enrollment.
        """
        self.client.logout()
        url_data = {'course_id': self.course.id, 'action': 'enroll'}
        result = self.client.post(
            reverse('ct:enroll', kwargs=url_data),
            {'role': Role.ENROLLED},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        data = json.loads(result.content)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(add_partial.call_count, 1)
        self.assertIn(add_partial.return_value, data.get('partial_url'))

    @patch('ct.views.Role.get_or_enroll')
    def test_call_enroll(self, get_or_enroll):
        """
        Check that on POST and Ajax get_or_enroll will be called when action is `enroll`.
        """
        url_data = {'course_id': self.course.id, 'action': 'enroll'}
        result = self.client.post(
            reverse('ct:enroll', kwargs=url_data),
            {'role': Role.ENROLLED},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(get_or_enroll.call_count, 1)

    @patch('ct.views.Role.discard_role')
    def test_call_unenroll(self, discard_role):
        """
        Check that on POST and Ajax discard_role will be called when action is `unenroll`.
        """
        url_data = {'course_id': self.course.id, 'action': 'unenroll'}
        result = self.client.post(
            reverse('ct:enroll', kwargs=url_data),
            {'role': Role.ENROLLED},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(discard_role.call_count, 1)


@ddt
class GetOrEnrollTest(TestCase):
    """
    Tests for get_or_enroll Role classmethod.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.course = Course(title='test title', description='test descr', addedBy=self.user)
        self.course.save()

    def test_no_previous_roles(self):
        """
        Check that role successfully added as is because no previous roles being found.
        """
        role = Role.get_or_enroll(course=self.course, user=self.user, role=Role.ENROLLED)
        self.assertIsInstance(role, Role)
        self.assertEqual(role.user, self.user)
        self.assertEqual(role.course, self.course)
        self.assertEqual(role.role, Role.ENROLLED)
        self.assertTrue(
            Role.objects.filter(course=self.course, user=self.user, role=Role.ENROLLED).exists()
        )

    @data(Role.ENROLLED, Role.SELFSTUDY)
    def test_return_role_if_exists(self, role):
        """
        Chech that classmethod return role is one exists.
        """
        old_role = Role.get_or_enroll(course=self.course, user=self.user, role=role)
        new_role = Role.get_or_enroll(course=self.course, user=self.user, role=role)
        self.assertEqual(old_role.id, new_role.id)

    def test_change_self_if_student(self):
        """
        Check that existent SELFSTUDY role will change into ENROLLED on commint from LTI.
        """
        old_role = Role.get_or_enroll(course=self.course, user=self.user, role=Role.SELFSTUDY)
        lti_role = Role.get_or_enroll(course=self.course, user=self.user, role=Role.ENROLLED)
        self.assertEqual(old_role.id, lti_role.id)
        self.assertEqual(lti_role.role, Role.ENROLLED)

    def test_return_stundent_as_is(self):
        """
        Check that student role will return if one exists and we enrolling as SELFSTUDY.
        """
        old_role = Role.get_or_enroll(course=self.course, user=self.user, role=Role.ENROLLED)
        new_role = Role.get_or_enroll(course=self.course, user=self.user, role=Role.SELFSTUDY)
        self.assertEqual(old_role.id, new_role.id)
        self.assertEqual(new_role.role, Role.ENROLLED)


@ddt
class DiscardRoleTest(TestCase):
    """
    Tests for discard_role Role classmetod.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.course = Course(title='test title', description='test descr', addedBy=self.user)
        self.course.save()

    def test_discard_non_existant_role(self):
        """
        Method should return Boolean flag about action result.
        """
        result = Role.discard_role(course=self.course, user=self.user, role=Role.ENROLLED)
        self.assertFalse(result)

        Role.get_or_enroll(course=self.course, user=self.user, role=Role.ENROLLED)
        result = Role.discard_role(course=self.course, user=self.user, role=Role.ENROLLED)
        self.assertTrue(result)

    @unpack
    @data((Role.ENROLLED, Role.SELFSTUDY), (Role.SELFSTUDY, Role.ENROLLED))
    def test_discard_student_and_self(self, created_role, discarding_role):
        """
        Check discard ENROLLED role if one exists and SELFSTUDY in params and vise versa.
        """
        Role.get_or_enroll(course=self.course, user=self.user, role=created_role)
        result = Role.discard_role(course=self.course, user=self.user, role=discarding_role)
        self.assertTrue(result)
        self.assertFalse(
            Role.objects.filter(course=self.course, user=self.user, role=created_role).exists()
        )


class PartialEnrollTest(TestCase):
    """
    Tests for PartialEnroll view.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.course = Course(title='test title', description='test descr', addedBy=self.user)
        self.course.save()
        self.ul = create_question_unit(self.user)
        concept = Concept.new_concept('bad', 'idea', self.ul.unit, self.user)
        self.ul.lesson.concept = concept
        self.ul.lesson.save()

    @patch('ct.views.uuid.uuid1')
    def test_add_partial_return_token_and_insert_into_table(self, uuid1):
        """
        Check that partial_hash successfully saved into DB.
        """
        hex_moked = Mock(hex='test_token')
        uuid1.return_value = hex_moked
        partial_params = 'Pickle dumped DICT with params'
        result = views.PartialEnroll.add_partial(partial_params)
        self.assertEqual(result, hex_moked.hex)
        self.assertEqual(uuid1.call_count, 1)
        self.assertEqual(
            PartialHashTable.objects.get(token=hex_moked.hex).params, partial_params
        )

    def test_continue_enroll(self):
        """
        Test continue on partial_params - saved partial data should be deleted.
        """
        token = 'test_token'
        partial_params = pickle.dumps({'course': self.course, 'role': Role.ENROLLED})
        self.client.login(username='test', password='test')
        partial_hash = PartialHashTable(token=token, params=partial_params)
        partial_hash.save()
        self.client.get(reverse('ct:enroll_continue', kwargs={'token': token}))
        self.assertFalse(PartialHashTable.objects.filter(token=token).exists())

    def test_redirects_to_course(self):
        """
        Test for redirection to correct url - main integration test.
        """
        url_data = {'course_id': self.course.id, 'action': 'enroll'}
        partial_result = self.client.post(
            reverse('ct:enroll', kwargs=url_data),
            {'role': Role.ENROLLED},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(partial_result.status_code, 401)
        self.client.login(username='test', password='test')
        data = json.loads(partial_result.content)
        result = self.client.get(data.get('partial_url'))
        self.assertRedirects(result, reverse('ct:course_student', kwargs={'course_id': self.course.id}))

    def test_redirects_on_acident_absense_of_token(self):
        """
        Test for redirection to 'ct:courses' if there is no token in HASH_TABLE.
        """
        self.client.login(username='test', password='test')
        result = self.client.get(reverse('ct:enroll_continue', kwargs={'token': 'test_token'}))
        self.assertRedirects(result, reverse('ct:courses'))

    @patch('ct.views.PartialEnroll.remove_partial')
    def test_remove_partial(self, remove_partial):
        """
        Test that remove_partial called on enroll_continue action.
        """
        token = 'test_token'
        partial_params = pickle.dumps({'course': self.course, 'role': Role.ENROLLED})
        self.client.login(username='test', password='test')
        partial_hash = PartialHashTable(token=token, params=partial_params)
        partial_hash.save()
        self.client.get(reverse('ct:enroll_continue', kwargs={'token': token}))
        remove_partial.called_once_with(token)

    @patch('ct.views.PartialEnroll.add_partial', return_value='test_token')
    def test_add_partial(self, add_partial):
        """
        Test that add_partial called on anonymous enrollment action.
        """
        url_data = {'course_id': self.course.id, 'action': 'enroll'}
        self.client.post(
            reverse('ct:enroll', kwargs=url_data),
            {'role': Role.ENROLLED},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        add_partial.called_once_with({'course_id': self.course.id, 'role': Role.ENROLLED})

    def test_bad_request(self):
        """
        Test that we fall in HttpBadRequest wher anonymous or Temporary.
        """
        response = self.client.get(reverse('ct:enroll_continue', kwargs={'token': 'token'}))
        self.assertContains(response, 'User is not authenticated', status_code=401)
        # Get Responde url to became a Temporary
        url = reverse(
            'ct:ul_respond',
            kwargs={'course_id': self.course.id, 'unit_id': self.ul.unit.id, 'ul_id': self.ul.id}
        )
        self.assertFalse(User.objects.filter(groups__name='Temporary').exists())
        self.client.get(url)
        self.assertTrue(User.objects.filter(groups__name='Temporary').exists())
        response = self.client.get(reverse('ct:enroll_continue', kwargs={'token': 'token'}))
        self.assertContains(response, 'User is not authenticated', status_code=401)


@ddt
class PartialIntegrationTest(TestCase):
    """
    General tests for posting actions from Temporary users.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.course = Course(title='test title', description='test descr', addedBy=self.user)
        self.course.save()
        self.ul = create_question_unit(self.user)
        concept = Concept.new_concept('bad', 'idea', self.ul.unit, self.user)
        self.ul.lesson.concept = concept
        self.ul.lesson.save()

    def test_make_temporary_in_decorator(self):
        """
        Test that Anonymous user is transformed into
        Temporary by preview_access decorator.
        """
        response = self.client.get(
            reverse(
                'ct:ul_respond',
                kwargs={'course_id': self.course.id, 'unit_id': self.ul.unit.id, 'ul_id': self.ul.id}
            )
        )
        self.assertIn('id="js--partial"', response.content)
        self.assertTrue(User.objects.filter(username__startswith='anonymous').exists())
        user = User.objects.filter(username__startswith='anonymous').first()
        self.assertTrue(user.groups.filter(name='Temporary').exists())
        self.assertIn('available_backends', response.context)

    def test_post_partial_pause(self):
        """
        Test POST request checking from Temporary user.
        """
        url = reverse(
            'ct:ul_respond',
            kwargs={'course_id': self.course.id, 'unit_id': self.ul.unit.id, 'ul_id': self.ul.id}
        )
        self.client.get(url)
        result = self.client.post(
            reverse('ct:partial_pause'),
            data={'POST': 'text=test+answer&confidence=sure', 'url': url}
        )
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(result, JsonResponse)

    def __need_to_implement_this__post_partial_pause_improperly_configured(self):
        """
        Test checking for improperly configured request.
        """
        url = reverse(
            'ct:ul_respond',
            kwargs={'course_id': self.course.id, 'unit_id': self.ul.unit.id, 'ul_id': self.ul.id}
        )
        self.client.get(url)
        result = self.client.post(
            reverse('ct:partial_pause'),
            data={'POST': '', 'url': url}
        )
        self.assertContains(result, 'Improperly configured request', status_code=400)
        self.assertIsInstance(result, JsonResponse)

    @unpack
    @data(
        (
            'ct:ul_respond',
            'text=test+answer&confidence=sure'
        ),
        (
            'ct:ul_faq',
            'title=test+title&text=test+quiestion&confidence=sure'
        )
    )
    def test_continue_partial(self, url_name, url_post_data):
        """
        Test that GET to 'ct:partial_continue' with correct token
        will continue partial.
        """
        url = reverse(
            url_name,
            kwargs={'course_id': self.course.id, 'unit_id': self.ul.unit.id, 'ul_id': self.ul.id}
        )
        self.client.get(url)
        response = self.client.post(
            reverse('ct:partial_pause'),
            data={'POST': url_post_data, 'url': url}
        )
        continue_url = json.loads(response.content).get('partial_url')
        self.assertIn('partial_continue', continue_url)
        token = continue_url.split('/')[-2]
        self.assertTrue(PartialHashTable.objects.filter(token=token).exists())
        result = self.client.get(continue_url)
        self.assertIsInstance(result, HttpResponseRedirect)
        # post data should be deleted from storage
        self.assertFalse(PartialHashTable.objects.filter(token=token).exists())
        result = self.client.get(continue_url)
        self.assertEqual(result.status_code, 404)
