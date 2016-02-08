'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/lessons',
    'text!templates/sidebar_lessons.html',
    ],

    function($, _, Backbone, Lessons, sidebar_template){
        var SideBarView = Backbone.View.extend({

            template: _.template(sidebar_template),

            events: {
                'click label':'goToLesson'
            },

            initialize: function () {
                Backbone.on('lesson', this.getLessonUnit, this);
                this.listenTo(Lessons, 'reset', this.lessonsInSidebar);
                console.log("i'm alive");
            },

            render: function () {
                this.$el.empty();
                var labels = this.model.labels;
                for (var each in labels) {
                    var label = Labels.getLabelById(labels[each]).toJSON();
                    var new_label = this.template(label);
                    this.$el.append(new_label);
                }
                return this;
		    },

            getLessonUnit: function(param){
                var pathname = window.location.pathname;
                var firstPartOfPath = pathname.match( /(concepts|lessons|errors)\/\d+/ );
                Lessons.unit_lesson = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                firstPartOfPath = pathname.match( /units\/\d+/ );
                Lessons.unit = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                firstPartOfPath = pathname.match( /courses\/\d+/ );
                Lessons.course = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                Lessons.fetch({data: {'unit_id':Lessons.unit}, reset:true});
            },

            lessonsInSidebar: function(){
                var lessons = Lessons.toJSON();
                _.each(lessons, function(lesson){
                                    if(lesson.title.length > 25) {
                                      lesson.title = lesson.title.substring(0, 23) + '...';
                                    }
                                });
                this.$el.html(this.template({all:lessons}));
            },

            goToLesson: function(event){
                var unit_lesson = event.currentTarget.getAttribute('data');
                var url = '/ui/hack/courses/'+Lessons.course+'/units/'+Lessons.unit+'/lessons/'+unit_lesson+'/#lesson';
                window.history.pushState("", "", url);
                Backbone.history.trigger('checkurl');
            }
        });
	return SideBarView;
});


