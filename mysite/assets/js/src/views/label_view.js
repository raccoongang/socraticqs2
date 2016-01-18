'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/labels',
    ],

    function($, _, Backbone, Labels){
        var LabelView = Backbone.View.extend({

            template: _.template('<label data="<%= id %>" class="label <%= color %>"><%= title %></label>'),

            initialize: function () {},

            render: function () {
                var labels = this.model.toJSON().labels;
                for (var each in labels) {
                    var label = Labels.getLabelById(labels[each]).toJSON();
                    var new_label = this.template(label);
                    this.$el.append(new_label);
                }
                return this;
		    },

        });
	return LabelView;
});


