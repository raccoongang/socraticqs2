import os
import sys

from fab_settings import env
from fabric.contrib import django
from fabric.api import local, lcd
from fabric.tasks import Task

sys.path.append(os.path.dirname(__file__) + '/../../mysite/')

django.settings_module('mysite.settings')


class Build(Task):
    base_path = os.path.dirname(__file__) + '/../..'

    def run(self, suffix=None):
        local("gulp")
        with lcd(os.path.join(self.base_path, '../')):
            local('source {}/bin/activate'.format(env.venv_name))
            with lcd(os.path.join(self.base_path, 'mysite')):
                local('python manage.py collectstatic --noinput')


class Install(Task):
    def run(self, suffix=None):
        local("npm install --save-dev")


build = Build()
install = Install()
