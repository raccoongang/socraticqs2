'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'views/issue_detail',
    'views/label_view',
    'text!templates/issue_row.html',
     "bootstrap"
    ],

    function($, _, Backbone, Issues, detail_view, label_view, row_template){
        var IssueRowView = Backbone.View.extend({
            tagName: 'tr',

            template: _.template(row_template),

            events: {
            },

            detailView:'',

            initialize: function () {
                this.listenTo(this.model, 'change', this.render);
                this.listenTo(this.model, 'destroy', this.remove);
                this.listenTo(this, 'show', this.showDetails);
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                var view = new label_view({model: this.model.toJSON()});
                this.$el.find('#labels_row').append(view.render().el);
                return this;
		    },

            makeDataTabActive: function(){
                $('.nav-tabs > li.active').removeClass('active');
                $('.tab-content > div.active').removeClass('active');
                $('#data_tab').addClass('active');
                $('#data_issues').addClass('active').removeClass('fade');
            },


            showDetails: function(e){
                if (e){e.preventDefault();}
                if (this.model.get('auto_issue')){
                    this.makeDataTabActive();
                }
                else {
                    this.detailView = new detail_view({model: this.model, el: this.parent.el});
                    this.detailView.render();
                }
            },

        });
	return IssueRowView;
});

//TODO try to manually change active class for this tabs