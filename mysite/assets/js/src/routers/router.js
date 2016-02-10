define(['jquery',
	    'backbone',
        'bootstrap'],
function ($, Backbone, Bootstrap) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
            '(/)':'details',
            'issue/:issue_id(/)': 'showIssueDetail',
            'search=*text(/)':'search',
            'issues(/)': 'openIssues',
            'issues/*params(/)': 'is_open',
		},

        initialize: function(options) {
             Backbone.history.on('checkurl', this.details, this);
        },

        search: function (text) {
            text = (typeof text !== 'undefined' & text !== null) ? text : '';
            if (text.length > 0) {
                Backbone.trigger('newSearch',{text:text, fromUrl: true, });
                Backbone.trigger('unit_lesson', concept_id);
            }
        },

		is_open: function (params) {
            Backbone.trigger('details');
            Backbone.trigger('issues_list');
            $('a[href="#issues"]').tab('show');
		},

        showIssueDetail: function(issue_id){
            Backbone.trigger('details');
            Backbone.trigger('issue_details', {issue_id:issue_id});
            $('a[href="#issues"]').tab('show');
        },

        openIssues: function(e){
            if (e) {
                e.data.state.details();
            }
            else {
                this.details();
            }
            $('a[href="#issues"]').tab('show');
            Backbone.history.navigate('issues/')
        },

        details: function(){
            Backbone.trigger('sidebar');
            Backbone.trigger('details');
            Backbone.trigger('issues_list');
            $('a[href="#details"]').tab('show');
        },


	});

	return IssueRouter;
});
