'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/issue_row.html'
    ],

    function($, _, Backbone, row_template){
        var MainTabView = Backbone.View.extend({
            tagName: 'tr',

            template: _.template(row_template),

            initialize: function () {
                this.listenTo(this.model, 'change', this.render);
                this.listenTo(this.model, 'destroy', this.remove);
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));

                return this;
		    },
        });
	return MainTabView;
});


