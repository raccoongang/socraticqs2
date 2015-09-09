# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from ct.templatetags.ct_extras import md2html


def compile_rst(apps, schema_editor):
    """
    Compile rst into html using md2html templatetag.
    """
    Lesson = apps.get_model("ct", "Lesson")
    Response = apps.get_model("ct", "Response")
    Course = apps.get_model("ct", "Course")
    for lesson in Lesson.objects.all():
        if lesson.text:
            lesson.text_html = md2html(lesson.text)
            lesson.save()
    for response in Response.objects.all():
        if response.text:
            response.text_html = md2html(response.text)
            response.save()
    for course in Course.objects.all():
        if course.description:
            course.description_html = md2html(course.description)
            course.save()


def decompile_rst(apps, schema_editor):
    """
    Function for backward migration.
    """
    Lesson = apps.get_model("ct", "Lesson")
    Response = apps.get_model("ct", "Response")
    Course = apps.get_model("ct", "Course")
    Lesson.objects.all().update(text_html='')
    Response.objects.all().update(text_html='')
    Course.objects.all().update(description_html='')


class Migration(migrations.Migration):
    """
    Data migration to compile rst text in old models into html.
    """
    dependencies = [
        ('ct', '0017_auto_20150910_0321'),
    ]

    operations = [
        migrations.RunPython(compile_rst, reverse_code=decompile_rst)
    ]
