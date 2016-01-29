define(['jquery',
	    'backbone',
        'bootstrap',
	    'collections/issues'],
function ($, Backbone, Bootstrap, Issues) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
            '(/)':'openIssues',
            'search=*text(/)':'search',
            'issues(/)': 'openIssues',
            'issues/*params(/)': 'is_open'

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

		is_open: function (params) {
            var list_of_params = params.split('/');
            for (var each in list_of_params) {
                list_of_params[each]=list_of_params[each].split('=');
            }
            var dict_of_params = {};
            for (var each in list_of_params) {
                dict_of_params[list_of_params[each][0]]=list_of_params[each][1];
            }

            $('a[href="#lesson_issues"]').tab('show');
            var concept_id = this.getUnitLessonId();
            console.log(dict_of_params);
            Backbone.trigger('unit_lesson',dict_of_params);
			Issues.trigger(dict_of_params['is_open']);
		},

        openIssues: function(){
            $('a[href="#lesson_issues"]').tab('show');
            var concept_id = this.getUnitLessonId();
            Backbone.trigger('unit_lesson',{unit_lesson: concept_id, is_open:'open'});
        }
	});

	return IssueRouter;
});
