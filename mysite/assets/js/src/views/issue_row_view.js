'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'views/issue_detail',
    'views/label_view',
    'text!templates/issue_row.html'
    ],

    function($, _, Backbone, detail_view, label_view, row_template){
        var IssueRowView = Backbone.View.extend({
            tagName: 'tr',

            template: _.template(row_template),

            events: {
                'click a': 'showDetails',
            },

            detailView:'',

            initialize: function () {
                this.listenTo(this.model, 'change', this.render);
                this.listenTo(this.model, 'destroy', this.remove);
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                var labels = this.model.toJSON().labels;
                    for (var each in labels) {
                        var view = new label_view();
                        view.template = _.template('<%= title %>');
                        this.$el.find('#label_row').append(view.render(labels[each]).el);
                }
                return this;
		    },

            showDetails: function(){
                this.detailView = new detail_view({model:this.model, el: this.parent.el});
                this.detailView.render();
            },

        });
	return IssueRowView;
});


