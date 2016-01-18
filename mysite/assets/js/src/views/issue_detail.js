'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'collections/users',
    'views/edit_issue',
    'views/label_view',
    'text!templates/issue_detail.html'
    ],

    function($, _, Backbone, Issues, Users, edit_issue, label_view, issue_detail_template){
        var IssueDetailView = Backbone.View.extend({
            template: _.template(issue_detail_template),

            events:{
                'click #issue_detail_cancel_button': 'goBackToMainView',
                'click #is_open_button': 'toggleIssue',
                'click #edit_issue': 'editIssue'
            },

            initialize: function(){
                this.listenTo(this.model, 'change', this.render);
            },

            render: function () {
                var for_template = this.model.toJSON();
                if (for_template.assignee) {
                for_template.assignee_name = Users.getUserById(for_template.assignee).toJSON();}
                else {
                    for_template.assignee_name = '';
                }
                this.$el.html(this.template(for_template));
                var view = new label_view({model: this.model});
                this.$el.find('#labels').append(view.render().el);
		    },

            goBackToMainView: function(){
                this.stopListening();
                this.undelegateEvents();
                Issues.trigger('reset');
            },

            editIssue: function(){
                var view = new edit_issue({model: this.model, el: this.el});
                this.listenToOnce(view, 'cancel', this.render);
                view.render();
            },

            toggleIssue: function(){
                this.model.toggle();
            }
        });
	return IssueDetailView;
});
