define(['jquery',
	    'backbone',
	    'collections/issues',],

function ($, Backbone, Issues) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
			'open': 'open',
            'closed': 'closed'
		},

		open: function () {
			Issues.trigger('open');
		},

		closed: function () {
			Issues.trigger('closed');
		},

	});

	return IssueRouter;
});