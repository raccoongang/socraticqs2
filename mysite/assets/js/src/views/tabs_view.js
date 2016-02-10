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

    function($, _, Backbone, Labels,
             Users, issue_tab_view,
             lesson_tab_view, issue_detail_view,
             tabs_template){
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

            details: function(){
                if (this.detail_tab) {this.detail_tab.stopListening(); this.detail_tab.undelegateEvents();}
                this.detail_tab = new lesson_tab_view({el: $('#details')});

            },

            issue_details: function(params){
                $('a[href="#issues"]').off('show.bs.tab');
                if (this.issue_tab) {this.issue_tab.stopListening(); this.issue_tab.undelegateEvents();}
                this.issue_tab = new issue_detail_view({el:$('#issues'),
                                                        issue_id:params.issue_id});
            },

            issues_list: function(params){
                $('a[href="#issues"]').off('show.bs.tab');
                if (this.issue_tab) {this.issue_tab.stopListening(); this.issue_tab.undelegateEvents();}
                this.issue_tab = new issue_tab_view({el:$('#issues')});
            },

            render: function(){
                this.$el.html(this.template({details: true,
                                             issues: true,
                                             data: true}));
            },

        });
        return tabs_view;
    }
);
