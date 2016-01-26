define(['jquery',
	    'backbone',
        'bootstrap',
	    'collections/issues',
        'collections/SearchCollection'],
function ($, Backbone, Bootstrap, Issues, SearchCollection) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
            'ui/hack/(?*text)':'search',
			'ui/hack/lesson/:number(/)': 'getIssues',
			'ui/hack/lesson/:number/:is_open(/)': 'is_open',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id(/)': 'Issues',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id/issues(/)': 'openIssues',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id/issues/:is_open(/)': 'is_open'

		},

        search: function (text) {
            text = (typeof text !== 'undefined' & text !== null) ? text : '';
            if (text.length > 0) {
                text = text.substr(5, text.length);
                var collection = new SearchCollection([], text);
                collection.fetch({
                    'reset': true, error: function (collection, response, options) {
                        console.log('Something take wrong');
                        console.log(response.responseText);
                    }
                });
            }
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