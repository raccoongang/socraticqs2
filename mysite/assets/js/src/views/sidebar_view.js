'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/lessons',
    'views/add_lesson',
    'text!templates/sidebar_template.html',
    ],

    function($, _, Backbone, Lessons, add_lesson, sidebar_template){
        var SideBarView = Backbone.View.extend({

            template: _.template(sidebar_template),

            events: {
                'click label':'goToLesson',
                'click #add_lesson': 'addLesson',

            },

            initialize: function () {
                Backbone.on('lesson', this.getLessonUnit, this);
                this.listenTo(Lessons, 'reset', this.lessonsInSidebar);
            },

            render: function () {

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
                this.$el.html(this.template({all_lessons:lessons}));
            },

            goToLesson: function(event){
                var unit_lesson = event.currentTarget.getAttribute('data');
                var url = '/ui/hack/courses/'+Lessons.course+'/units/'+Lessons.unit+'/lessons/'+unit_lesson+'/#lesson';
                window.history.pushState("", "", url);
                Backbone.history.trigger('checkurl');
            },

            addLesson: function(){
                this.view = new add_lesson({el:$('#lesson_content')});
                this.view.render();
            },

        });
	return SideBarView;
});


