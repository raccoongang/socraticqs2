define(['jquery',
	    'backbone',
        'bootstrap',
	    'collections/issues'],
function ($, Backbone, Bootstrap, Issues) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
<<<<<<< HEAD
            '(/)':'Issues',
            'search=*text(/)':'search',
=======
            'ui/hack/(?*text)':'search',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id/issues/?search=*text(/)': 'search',
>>>>>>> a97b0ea298f91497e6ac2f6982f8bb621dfedc0f
			'ui/hack/lesson/:number(/)': 'getIssues',
			'ui/hack/lesson/:number/:is_open(/)': 'is_open',
            'ct/teach/courses/:course_id/units/:unit_id/concepts/:concept_id(/)': 'Issues',
            'issues(/)': 'openIssues',
            'issues/:is_open(/)': 'is_open'

		},

        search: function (text) {
            text = (typeof text !== 'undefined' & text !== null) ? text : '';
            if (text.length > 0) {
                Backbone.trigger('newSearch',{text:text, fromUrl: true, });
                var concept_id = this.getUnitLessonId();
                Backbone.trigger('unit_lesson',{unit_lesson: concept_id});
            }
        },

        getUnitLessonId: function(){
          var pathname = window.location.pathname;
          var firstPartOfPath = pathname.match( /concepts\/\d+/ )[0];
          return parseInt(firstPartOfPath.match(/\d+/)[0]);
        },

		is_open: function (is_open) {
            $('a[href="#lesson_issues"]').tab('show');
            var concept_id = this.getUnitLessonId();
            Backbone.trigger('unit_lesson',{unit_lesson: concept_id});
			Issues.trigger(is_open);
		},

		getIssues: function(number){
            Backbone.trigger('unit_lesson',{unit_lesson: number});
        },

        Issues: function(course_id, unit_id, concept_id){
            Backbone.trigger('unit_lesson',{unit_lesson: concept_id});
        },

        openIssues: function(){
            $('a[href="#lesson_issues"]').tab('show');
            var concept_id = this.getUnitLessonId();
            Backbone.trigger('unit_lesson',{unit_lesson: concept_id});
        },

	});

	return IssueRouter;
});
