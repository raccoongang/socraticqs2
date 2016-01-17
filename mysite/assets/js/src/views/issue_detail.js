'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'views/edit_issue',
    'text!templates/issue_detail.html'
    ],

    function($, _, Backbone, Issues, edit_issue, issue_detail_template){
        var IssueDetailView = Backbone.View.extend({
            template: _.template(issue_detail_template),

            events:{
                'click #issue_detail_cancel_button': 'goBackToMainView',
                'click #is_open_button': 'toggleIssue',
                'click #edit_issue': 'editIssue'
            },

            initialize: function(){
                this.listenTo(this.model, 'change', this.render)
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
		    },

            goBackToMainView: function(){
                this.stopListening();
                this.undelegateEvents();
                Issues.trigger('reset');
            },

            editIssue: function(){
                var view = new edit_issue({model: this.model, el: this.el});
                view.render();
            },

            toggleIssue: function(){
                this.model.toggle();
            }
        });
	return IssueDetailView;
});
