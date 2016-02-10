define([
    'jquery',
    'underscore',
    'backbone',
    'collections/labels',
    'collections/users',
    'views/issue_tab_view',
    'views/lesson_tab_view',
    'views/issue_detail',
    'text!templates/tabs_template.html'
    ],

    function($, _, Backbone, Labels, Users, issue_tab_view, lesson_tab_view, issue_detail_view, tabs_template){
        'use strict';
        var tabs_view = Backbone.View.extend({

            template: _.template(tabs_template),

            events:{
            },

            initialize: function(){
                Labels.fetch({reset:true});
                Users.fetch({reset:true});
                this.render();
                Backbone.on('issues_list', this.issues_list, this);
                Backbone.on('issue_details',this.issue_details, this);
                Backbone.on('details',this.details, this);
                Backbone.history.start();
            },

            details: function(params){
                //this.empty_all();
                if (this.lesson_tab) {this.lesson_tab.stopListening(); this.lesson_tab.undelegateEvents();}
                if (params.unit_lesson) {
                    this.lesson_tab = new lesson_tab_view({el: $('#details')});
                }
                else {
                    //this.lesson_tab = new unit_tab_view({el: $('#details')});
                }
            },

            issue_details: function(params){
                if (this.issue_tab) {this.issue_tab.stopListening(); this.issue_tab.undelegateEvents();}
                this.issue_tab = new issue_detail_view({el:$('#issues'),
                                                        issue_id:params.issue_id});
            },

            issues_list: function(params){
                if (this.issue_tab) {this.issue_tab.stopListening(); this.issue_tab.undelegateEvents();}
                this.issue_tab = new issue_tab_view({el:$('#issues'), params:params});
            },

            render: function(){
                this.$el.html(this.template({details: true,
                                             issues: true,
                                             data: true}));
            },

            empty_all: function(){
                $('#issues').empty;
                $('#details').empty;
                $('#data').empty;
            }

        });
        return tabs_view;
    }
);
