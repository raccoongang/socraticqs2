'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'views/issue_detail',
    'text!templates/issue_row.html'
    ],

    function($, _, Backbone, detail_view, row_template){
        var MainTabView = Backbone.View.extend({
            tagName: 'tr',

            template: _.template(row_template),

            events: {
                'click a': 'showDetails',
            },

            initialize: function () {
                this.listenTo(this.model, 'change', this.render);
                this.listenTo(this.model, 'destroy', this.remove);
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));

                return this;
		    },

            showDetails: function(){
                $('#table_of_issues').empty();
                var view = new detail_view({model:this.model});
                $('#table_of_issues').append(view.render().el);
            }
        });
	return MainTabView;
});


