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
                "click #add_issue_button": 'CreateNewIssue',
                "click #add_issue_cancel_button": "goBackToMainView",
            },

            initialize: function () {

            },

            render: function () {
                this.$el.html(this.template({'user':256}));
                return this;
		    },

            CreateNewIssue: function(){
                var unindexed_array = $('#add_issue_form').serializeArray();
                var model = []
                $.map(unindexed_array, function(n, i){
                    model[n.name] = n.value;
                    });
                Issues.create(model, {success: this.goBackToMainView});
            },

             goBackToMainView: function(){
                Issues.trigger('reset');
                this.remove();
            }
        });
	return AddIssueView;
});