'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/issue_detail.html'
    ],

    function($, _, Backbone, issue_detail_template){
        var IssueDetailView = Backbone.View.extend({
             template: _.template(issue_detail_template),

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                return this;
		    },

        });
	return IssueDetailView;
});
