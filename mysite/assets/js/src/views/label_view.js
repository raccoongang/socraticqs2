'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/labels',
    ],

    function($, _, Backbone, Labels){
        var LabelView = Backbone.View.extend({
            tagName: 'p',

            initialize: function () {

            },

            render: function (label_id) {
                var label = Labels.getLabelById(label_id);
                this.$el.html(this.template(label.toJSON()));
                return this;
		    },

        });
	return LabelView;
});


