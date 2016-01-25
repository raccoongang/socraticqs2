'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'views/issue_detail',
    'views/label_view',
    'text!templates/issue_row.html',
     "bootstrap"
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
                var view = new label_view({model: this.model.toJSON()});
                this.$el.find('#labels_row').append(view.render().el);
                return this;
		    },

            showDetails: function(e){
                e.preventDefault();
                if (this.model.get('auto_issue')){
                    $('.nav-tabs a[href="#data_issues"]').tab('show');
                }
                else {
                    this.detailView = new detail_view({model: this.model, el: this.parent.el});
                    this.detailView.render();
                }
            },

        });
	return IssueRowView;
});


