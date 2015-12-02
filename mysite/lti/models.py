import json
from django.utils import timezone

from django.db import models
from django.contrib.auth import login
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth

from ct.models import Role, Course


class LTIUser(models.Model):
    """Model for LTI user

    **Fields:**

      .. attribute:: user_id
      uniquely identifies the user within LTI Consumer

      .. attribute:: consumer
      uniquely  identifies the Tool Consumer

      .. attribute:: extra_data
      user params received from LTI Consumer

      .. attribute:: django_user
      Django user to store study progress

      .. attribute:: context_id
      Context id given from LTI params

    LTI user params saved to extra_data field::

        'user_id'
        'context_id'
        'lis_person_name_full'
        'lis_person_name_given'
        'lis_person_name_family'
        'lis_person_sourcedid'
        'tool_consumer_instance_guid'
        'lis_person_contact_email_primary'
        'tool_consumer_info_product_family_code'
    """
    user_id = models.CharField(max_length=255, blank=False)
    consumer = models.CharField(max_length=64, blank=True)
    extra_data = models.TextField(max_length=1024, blank=False)
    django_user = models.ForeignKey(User, null=True, related_name='lti_auth')
    context_id = models.CharField(max_length=255)

    class Meta:  # pragma: no cover
        unique_together = ('user_id', 'consumer', 'context_id')

    def create_links(self):
        """
        Create all needed links to Django and/or UserSocialAuth.
        """
        extra_data = json.loads(self.extra_data)
        username = extra_data.get(
            'lis_person_name_full',
            extra_data.get('lis_person_sourcedid', self.user_id)
        )
        first_name = extra_data.get('lis_person_name_given', '')
        last_name = extra_data.get('lis_person_name_family', '')
        email = extra_data.get('lis_person_contact_email_primary', '').lower()

        defaults = {
            'first_name': first_name,
            'last_name': last_name,
        }

        if email:
            defaults['email'] = email
            social = UserSocialAuth.objects.filter(
                provider='email', uid=email
            ).first()
            if social:
                django_user = social.user
            else:
                django_user = User.objects.filter(email=email).first()
                if not django_user:
                    django_user, created = User.objects.get_or_create(
                        username=username, defaults=defaults
                    )
                social = UserSocialAuth(
                    user=django_user,
                    provider='email',
                    uid=email,
                    extra_data=extra_data
                )
                social.save()
        else:
            django_user, created = User.objects.get_or_create(
                username=username, defaults=defaults
            )
        self.django_user = django_user
        self.save()

    def login(self, request):
        """
        Login linked Django user.
        """
        if self.django_user:
            self.django_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, self.django_user)

    def enroll(self, roles, course_id):
        """Create Role according to user roles from LTI POST

        roles -> roles of LTI user given from LTI Consumer
        course_id -> Course entry id given from Launch URL

        :param roles: (str|list)
        :param course_id: int
        :return: None
        """
        if not isinstance(roles, list):
            roles = roles.split(',')
        course = Course.objects.filter(id=course_id).first()
        if course:
            for role in roles:
                Role.get_or_enroll(
                    role=role,
                    course=course,
                    user=self.django_user
                )

    def is_enrolled(self, roles, course_id):
        """Check enroll status

        :param roles: (str|list)
        :param course_id: int
        :return: bool
        """
        if not isinstance(roles, list):
            roles = roles.split(',')
        course = Course.objects.filter(id=course_id).first()
        if Role.INSTRUCTOR in roles:
            role = Role.INSTRUCTOR
        else:
            role = Role.ENROLLED
        if course:
            return Role.objects.filter(
                role=role,
                course=course,
                user=self.django_user
            ).exists()

    @property
    def is_linked(self):
        """Check link to some Django user

        :return: bool
        """
        return bool(self.django_user)


class CourseRef(models.Model):  # pragma: no cover
    """Course reference

    Represent Course reference with meta information
    such as::

        course -> Courslet Course entry
        instructors -> list of User entry
        date - > creation date
        context_id -> LTI context_id
        tc_guid - > LTI tool_consumer_instance_guid
    """
    course = models.ForeignKey(Course, verbose_name='Courslet Course')
    instructors = models.ManyToManyField(User, verbose_name='Course Instructors')
    date = models.DateTimeField('Creation date and time', default=timezone.now)
    context_id = models.CharField('LTI context_id', max_length=254)
    tc_guid = models.CharField('LTI tool_consumer_instance_guid', max_length=128)

    class Meta:
        verbose_name = "CourseRef"
        verbose_name_plural = "CourseRefs"
        unique_together = ('context_id', 'course')

    def __str__(self):
        return '{0} {1}'.format(
            self.course.title, str(self.date.strftime('%H:%M %d-%m-%y'))
        )
