define(['jquery',
	    'backbone',
	    'collections/issues',],

function ($, Backbone, Issues) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
			'ui/hack/lesson/:number(/)': 'getIssues',
			'ui/hack/lesson/:number/:is_open(/)': 'is_open',
		},

		is_open: function (number, is_open) {
            console.log(is_open);
            Backbone.trigger('unit_lesson',{unit_lesson: number});
			Issues.trigger(is_open);
		},

		getIssues: function(number){
            Backbone.trigger('unit_lesson',{unit_lesson: number});
        },

	});

	return IssueRouter;
});