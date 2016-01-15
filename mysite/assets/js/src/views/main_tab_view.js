'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'views/issue_row_view',
    'text!templates/issue_tab.html'
    ],

    function($, _, Backbone, Issues, issue_row_view,  tab_template){
        var main_tab_view = Backbone.View.extend({
            template: _.template(tab_template),

            initialize: function(){

                this.$tab = $('#lesson_issues');

                this.listenTo(Issues, 'reset', this.render);

                Issues.fetch({reset:true});

            },

            render: function(){
                this.$tab.html(this.template());
                this.addAll();
            },

            addOne: function(issue){
                var view = new issue_row_view({ model: issue });
			    $('#table_of_issues').append(view.render().el);
            },

            addAll: function(){
                $('#table_of_issues').empty();
                Issues.each(this.addOne, this);

            }
        });
        return main_tab_view;
    }
);
