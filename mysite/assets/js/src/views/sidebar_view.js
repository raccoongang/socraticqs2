'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/lessons',
    'collections/courses',
    'collections/units',
    'collections/concepts',
    'views/add_lesson',
    'views/add_concept',
    'text!templates/sidebar_template.html',
    ],

    function($, _, Backbone, Lessons, Courses, Units, add_lesson, sidebar_template){
    function($, _, Backbone, Lessons, Concepts, add_lesson, add_concept, sidebar_template){
        var SideBarView = Backbone.View.extend({

            template: _.template(sidebar_template),

            events: {
                'click label':'goToLesson',
                'click #add_lesson': 'addLesson',
                'change #units_select': 'goToUnit',
                'change #courses_select': 'goToCourse',
                'click #add_concept': 'addConcept',
                //'click label_concept':'goToConcept',
            },

            initialize: function () {
                Backbone.on('sidebar', this.getCourses, this);
                this.listenTo(Lessons, 'reset', this.render);
                this.listenTo(Courses, 'reset', this.getUnits);
                this.listenTo(Units, 'reset', this.getLesson);
                Backbone.on('lesson', this.getLessonUnit, this);
                Backbone.on('concept', this.getConceptUnit, this);
                this.listenTo(Lessons, 'reset', this.lessonsInSidebar);
                this.listenTo(Concepts, 'reset', this.lessonsInSidebar);

                this.lessonsInSidebar();
            },

            getCourses: function(){
                Courses.fetch({reset:true});
            },

            getUnits: function(){
                var pathname = window.location.pathname;

                var firstPartOfPath = pathname.match( /courses\/\d+/ );
                if (firstPartOfPath){
                    this.course = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                }
                else {
                    this.course = Courses.first().id;
                   }
                Units.fetch({data: {'course_id': this.course}, reset: true});
            },


            getLesson: function(){
                var pathname = window.location.pathname;
                var firstPartOfPath = pathname.match( /(concepts|lessons|errors)\/\d+/ );
                if (firstPartOfPath) {
                    this.unit_lesson = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                }
                firstPartOfPath = pathname.match( /units\/\d+/ );
                Lessons.unit = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                firstPartOfPath = pathname.match( /courses\/\d+/ );
                Lessons.course = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                Lessons.fetch({data: {'unit_id':Lessons.unit}, reset:true});

                Concepts.unit_lesson = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                Concepts.unit = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                Concepts.course = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                Concepts.fetch({data: {'unit_id':Concepts.unit}, reset:true});
                if (firstPartOfPath){
                   this.unit = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                }
                else {
                    this.unit = Units.first().get('unit_id');
                    var url = '/ui/hack/courses/'+this.course+'/units/'+this.unit+'/';
                    window.history.pushState("", "", url);
                }
                Lessons.fetch({data: {'unit_id':this.unit}, reset:true});

            },

            render: function(){
                this.$el.empty();
                var lessons = Lessons.toJSON();
                var concepts = Concepts.toJSON();
                window.con = concepts;
                var courses = Courses.toJSON();
                var units = Units.toJSON();
                _.each(lessons, function(lesson){
                                    if(lesson.title.length > 25) {
                                      lesson.title = lesson.title.substring(0, 23) + '...';
                                    }
                                });
                this.$el.html(this.template({all_lessons:lessons,
                                             lesson: this.unit_lesson,
                                             all_units:units,
                                             unit: this.unit,
                                             all_courses:courses,
                                             course: this.course}));
                _.each(concepts, function(concept){
                                    if(concept.title.length > 25) {
                                      concept.title = concept.title.substring(0, 23) + '...';
                                    }
                                });
                this.$el.html(this.template({all_lessons:lessons, all_concepts:concepts}));
            },

            goToLesson: function(event){
                var unit_lesson = event.currentTarget.getAttribute('data');
                if(event.currentTarget.getAttribute('class').indexOf('label_concept') >=0 ){
                    var url = '/ui/hack/courses/'+Concepts.course+'/units/'+Concepts.unit+'/concepts/'+unit_lesson+'/#concept';
                }else {
                    var url = '/ui/hack/courses/' + Lessons.course + '/units/' + Lessons.unit + '/lessons/' + unit_lesson + '/#lesson';
                }
                var url = '/ui/hack/courses/'+this.course+'/units/'+this.unit+'/lessons/'+unit_lesson+'/#lesson';
                window.history.pushState("", "", url);
                Backbone.history.trigger('checkurl');
            },

            goToUnit: function(event){
                var unit = event.currentTarget.value;
                var url = '/ui/hack/courses/'+this.course+'/units/'+unit+'/';
                window.history.pushState("", "", url);
                Backbone.history.trigger('checkurl');
            },

            goToCourse: function(event){
                var course = event.currentTarget.value;
                var url = '/ui/hack/courses/'+course+'/';
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


