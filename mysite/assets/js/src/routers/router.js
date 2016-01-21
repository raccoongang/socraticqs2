define(['jquery',
	    'backbone',
        'bootstrap',
	    'collections/issues'],
function ($, Backbone, Bootstrap, Issues) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
			'ui/hack/lesson/:number(/)': 'getIssues',
			'ui/hack/lesson/:number/:is_open(/)': 'is_open',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id(/)': 'Issues',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id/issues(/)': 'openIssues',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id/issues/:is_open(/)': 'is_open'

		},

		is_open: function (course_id, unit_id, concept_id, is_open) {
            $('a[href="#lesson_issues"]').tab('show');
            Backbone.trigger('unit_lesson',{unit_lesson: concept_id});
			Issues.trigger(is_open);
		},

		getIssues: function(number){
            Backbone.trigger('unit_lesson',{unit_lesson: number});
        },

        Issues: function(course_id, unit_id, concept_id){
            Backbone.trigger('unit_lesson',{unit_lesson: concept_id});
        },

        openIssues: function(course_id, unit_id, concept_id){
            $('a[href="#lesson_issues"]').tab('show');
            Backbone.trigger('unit_lesson',{unit_lesson: concept_id});
        },

	});

	return IssueRouter;
});