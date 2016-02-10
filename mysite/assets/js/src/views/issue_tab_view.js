define([
    'jquery',
    'underscore',
    'backbone',
    'collections/issues',
    'collections/labels',
    'collections/users',
    'collections/comments',
    'views/issue_row_view',
    'views/add_issue',
    'text!templates/issue_tab.html'
    ],

    function($, _, Backbone, Issues, Labels, Users, Comments, issue_row_view, add_issue_view, tab_template){
        'use strict';
        var issue_tab_view = Backbone.View.extend({

            template: _.template(tab_template),

            events:{
                'click .col-sm-2': 'addIssue',
                'click .sort_by': 'sortBy',
                'click .show_all': 'showAll',
                'click .close_open_link': 'goToOpenClosed',
                'click .choices': 'filterBy',
            },

            initialize: function(params){
                Backbone.on('unit_lesson', this.new_unit, this);
                this.listenTo(Issues, 'reset', this.render);
                this.listenTo(Issues, 'add', this.render);
                this.listenTo(Issues, 'open', this.addOpen);
                this.listenTo(Issues, 'closed', this.addClosed);
                $('a[href="'+this.$el.attr("id")+'"]').on('shown.bs.tab', this.openTab);
                this.new_unit(params.params);
            },

            new_unit: function(param){
                this.filter = param;
                //TODO get rid of this fuckin shit and make it simplier
                if (param['unit_lesson']){
                    Issues.unit_lesson = param['unit_lesson'];
                    delete this.filter['unit'];
                    delete this.filter['course'];}
                else if (param['unit']) {Issues.unit = param['unit'];
                         delete this.filter['unit_lesson'];
                         delete this.filter['course'];}
                else {Issues.course = param['course'];
                      delete this.filter['unit_lesson'];
                      delete this.filter['unit'];}
                Issues.fetch({data: this.filter, reset:true});
            },

            render: function(){
                this.$el.html(this.template({closed_count: Issues.is_close().length,
                                             open_count: Issues.is_open().length,
                                             all_labels: Labels.toJSON(),
                                             all_users: Users.toJSON(),
                                             filter: this.filter}));
                this.addAll();
            },

            addOne: function(issue){
                var view = new issue_row_view({model: issue});
                view.parent = this;
			    this.$el.find('#table_of_issues').append(view.render().el);
                if (issue.id == this.filter['issue']){
                    view.trigger('show');
                }
            },

            addAll: function(){
                this.$el.find('#table_of_issues').empty();
                var is_open = this.filter.is_open == 'open' ? true : false;
                var collection = Issues.where({is_open: is_open});
                if (this.filter.label){
                    var label = this.filter.label;
                    collection = _.filter(collection, function(issue){ return $.inArray(label,issue.get('labels')) >= 0; });
                }
                if (this.filter.assignee){
                    var assignee = this.filter.assignee;
                    collection = _.filter(collection, function(issue){ return assignee == issue.get('assignee')});
                }
                if (this.filter.author){
                    var author = this.filter.author;
                    collection = _.filter(collection, function(issue){ return author == issue.get('author')});
                }
                for (var each in collection){
                    this.addOne(collection[each]);
                }
            },

            addOpen: function() {
                this.filter.is_open = 'open';
                $('#open_link_th').addClass('success');
                $('#close_link_th').removeClass('success');
                this.addAll();
            },

            addClosed: function() {
                this.filter.is_open = 'closed';
                $('#open_link_th').removeClass('success');
                $('#close_link_th').addClass('success');
                this.addAll();
            },

            showAll: function(event){
                event.preventDefault(event);
                var field = event.currentTarget.getAttribute('data');
                delete this.filter[field];
                this.changeUrl();
                Issues.fetch({data: this.filter, reset:true});
            },

            addIssue: function(){
                var view = new add_issue_view({el: this.el});
                this.listenToOnce(view, 'cancel', this.render);
                view.render();
            },

            sortBy: function(event){
                event.preventDefault(event);
                Issues.compareBy = event.currentTarget.getAttribute('data');
                Issues.sort();
                this.addAll();
            },

            filterBy: function(event){
                event.preventDefault();
                var type = event.currentTarget.getAttribute('data-type');
                this.filter[type] = parseInt(event.currentTarget.getAttribute('data'));
                Issues.fetch({data: this.filter, reset:true});
                this.changeUrl();
            },

            changeUrl: function(){
                var url = 'issues/';
                var exclude = ['unit_lesson', 'unit', 'course', 'issue'];
                for (var each in this.filter){
                    if ($.inArray(each, exclude) == -1) {
                        url += each + '=' + this.filter[each] + '/';
                    }
                }
                Backbone.history.navigate(url);
            },

            openTab: function(e){
                Backbone.history.navigate('issues/');
            },

            goToOpenClosed: function(e){
                e.preventDefault();
                var type = e.currentTarget.getAttribute('data');
                this.filter.is_open = type;
                this.changeUrl();
                Issues.trigger(type);
            },

        });
        return issue_tab_view;
    }
);
