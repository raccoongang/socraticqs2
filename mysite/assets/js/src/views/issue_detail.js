'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'text!templates/issue_detail.html'
    ],

    function($, _, Backbone, Issues, issue_detail_template){
        var IssueDetailView = Backbone.View.extend({
            template: _.template(issue_detail_template),

            events:{
                'click #issue_detail_cancel_button': 'goBackToMainView'
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                return this;
		    },

            goBackToMainView: function(){
                Issues.trigger('reset');
                this.remove();
            }
        });
	return IssueDetailView;
});
