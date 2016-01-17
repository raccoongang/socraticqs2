'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'collections/labels',
    'views/issue_row_view',
    'views/add_issue',
    'text!templates/issue_tab.html'
    ],

    function($, _, Backbone, Issues, Labels, issue_row_view, add_issue_view, tab_template){
        var main_tab_view = Backbone.View.extend({

            template: _.template(tab_template),

            events:{
                'click .col-sm-2': 'addIssue'
            },

            initialize: function(){
                this.listenTo(Issues, 'reset', this.render);
                Issues.fetch({reset:true});
                Labels.fetch({reset:true});
            },

            render: function(){
                this.$el.html(this.template());
                this.addAll();
            },

            addOne: function(issue){
                var view = new issue_row_view({ model: issue });
			    $('#table_of_issues').append(view.render().el);
            },

            addAll: function(){
                $('#table_of_issues').empty();
                Issues.each(this.addOne, this);

            },

            addIssue: function(){
                var view = new add_issue_view();
                this.$el.empty();
                this.$el.append(view.render().el);
            }

        });
        return main_tab_view;
    }
);
