from django.contrib import admin
import ct.models


@admin.register(ct.models.Role)
class AdminRole(admin.ModelAdmin):
    list_display = ('role', 'course', 'user', 'atime')


@admin.register(ct.models.ConceptGraph)
class AdminConceptGraph(admin.ModelAdmin):
    list_display = ('fromConcept', 'toConcept', 'relationship', 'atime')


@admin.register(ct.models.ConceptLink)
class AdminConceptLink(admin.ModelAdmin):
    list_display = ('concept', 'lesson', 'relationship', 'addedBy', 'atime')


@admin.register(ct.models.Concept)
class AdminConcept(admin.ModelAdmin):
    list_display = ('title', 'addedBy', 'approvedBy', 'atime', 'isError', 'isAbort', 'isFail', 'isPuzzled')


@admin.register(ct.models.CourseUnit)
class AdminCourseUnit(admin.ModelAdmin):
    list_display = ('unit', 'course', 'order', 'addedBy', 'atime', 'releaseTime')


@admin.register(ct.models.Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('title', 'description', 'access', 'addedBy', 'atime')


@admin.register(ct.models.Lesson)
class AdminLesson(admin.ModelAdmin):
    list_display = ('title', 'kind', 'medium', 'access', 'sourceDB', 'sourceID', 'addedBy', 'atime')


@admin.register(ct.models.Response)
class AdminResponse(admin.ModelAdmin):
    list_display = ('lesson', 'unitLesson', 'course', 'confidence', 'atime', 'selfeval', 'status', 'author',
                    'needsEval', 'parent')


@admin.register(ct.models.UnitLesson)
class AdminUnitLesson(admin.ModelAdmin):
    list_display = ('unit', 'kind', 'lesson', 'parent', 'order', 'atime', 'addedBy', 'treeID', 'branch')


@admin.register(ct.models.Unit)
class AdminUnit(admin.ModelAdmin):
    list_display = ('title', 'kind', 'atime', 'addedBy')


@admin.register(ct.models.StudentError)
class AdminStudentError(admin.ModelAdmin):
    list_display = ('response', 'errorModel', 'status', 'author', 'activity', 'atime')
