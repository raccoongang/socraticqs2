'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/lessons',
    'collections/concepts',
    'views/add_lesson',
    'views/add_concept',
    'text!templates/sidebar_template.html',

    ],

    function($, _, Backbone, Lessons, Concepts, add_lesson, add_concept, sidebar_template){
        var SideBarView = Backbone.View.extend({

            template: _.template(sidebar_template),
            events: {
                'click label':'goToLesson',
                'click #add_lesson': 'addLesson',
                'click #add_concept': 'addConcept',
                'click label_concept':'goToConcept',
            },

            initialize: function () {
                Backbone.on('lesson', this.getLessonUnit, this);
                Backbone.on('concept', this.getConceptUnit, this);
                this.listenTo(Lessons, 'reset', this.lessonsInSidebar);
                this.listenTo(Concepts, 'reset', this.lessonsInSidebar);

                this.lessonsInSidebar();
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

            getConceptUnit: function(param){
                var pathname = window.location.pathname;
                var firstPartOfPath = pathname.match( /(concepts|lessons|errors)\/\d+/ );
                Concepts.unit_lesson = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                firstPartOfPath = pathname.match( /units\/\d+/ );
                Concepts.unit = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                firstPartOfPath = pathname.match( /courses\/\d+/ );
                Concepts.course = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                Concepts.fetch({data: {'unit_id':Concepts.unit}, reset:true});
            },

            lessonsInSidebar: function(){
                var lessons = Lessons.toJSON();
                var concepts = Concepts.toJSON();
                _.each(lessons, function(lesson){
                                    if(lesson.title.length > 25) {
                                      lesson.title = lesson.title.substring(0, 23) + '...';
                                    }
                                });
                _.each(concepts, function(concept){
                                    if(concept.title.length > 25) {
                                      concept.title = concept.title.substring(0, 23) + '...';
                                    }
                                });
                this.$el.html(this.template({all_lessons:lessons, all_concepts:concepts}));
            },

            goToLesson: function(event){
                var unit_lesson = event.currentTarget.getAttribute('data');
                var url = '/ui/hack/courses/'+Lessons.course+'/units/'+Lessons.unit+'/lessons/'+unit_lesson+'/#lesson';
                window.history.pushState("", "", url);
                Backbone.history.trigger('checkurl');
            },

            goToConcept: function(event){
                var unit_lesson = event.currentTarget.getAttribute('data');
                var url = '/ui/hack/courses/'+Concepts.course+'/units/'+Concepts.unit+'/concepts/'+unit_lesson+'/#concept';
                window.history.pushState("", "", url);
                Backbone.history.trigger('checkurl');
            },

            addLesson: function(){
                this.view = new add_lesson({el:$('.tab-content > div.active')});
                this.view.render();
            },
            addConcept: function(){
              console.log("Add concept");
              this.view = new add_concept({el:$('.tab-content > div.active')});
              this.view.render();
            }

        });
	return SideBarView;
});
