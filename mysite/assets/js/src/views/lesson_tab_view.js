'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/users',
    'collections/lessons',
    'views/edit_lesson',
    'views/add_lesson',
    'text!templates/lesson_detail.html'
    ],

    function($, _, Backbone, Users, Lessons, edit_lesson, add_lesson, lesson_detail_template){
        var LessonDetailView = Backbone.View.extend({
            template: _.template(lesson_detail_template),

            events:{
                'click #edit_lesson': 'editLesson',
                'click #add_lesson': 'addLesson'

            },

            initialize: function(){
                Backbone.on('unit_lesson', this.get_lesson, this);
                this.listenTo(Lessons, 'reset', this.render);
                this.listenTo(Lessons, 'change', this.render);
            },

            render: function () {
                this.model = Lessons.get(Lessons.unit_lesson)
                this.$el.html(this.template(this.model.toJSON()));
		    },

            get_lesson: function(param){
                Lessons.unit = param['unit'];
                Lessons.unit_lesson = param['unit_lesson'];
                Lessons.fetch({data: {'unit': Lessons.unit}, reset:true});
            },

            backFromEdit: function(){
              this.render();
            },

            editLesson: function(){
                var view = new edit_lesson({model: this.model, el: this.el});
                this.listenToOnce(view, 'cancel', this.backFromEdit);
                view.render();
            },

            addLesson: function(){
                var view = new add_lesson({el: this.el});
                this.listenToOnce(view, 'cancel', this.render);
                view.render();
            },

        });
	return LessonDetailView;
});
