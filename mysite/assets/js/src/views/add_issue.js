'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'text!templates/add_issue.html'
    ],

    function($, _, Backbone, Issues, add_issue){
        var AddIssueView = Backbone.View.extend({

            template: _.template(add_issue),

            events:{
                "click #add_issue_button": 'CreateNewIssue'
            },

            initialize: function () {

            },

            render: function () {
                this.$el.html(this.template());
                return this;
		    },

            CreateNewIssue: function(){
                Issues.create( $('#add_issue_form').serialize() );
            }
        });
	return AddIssueView;
});