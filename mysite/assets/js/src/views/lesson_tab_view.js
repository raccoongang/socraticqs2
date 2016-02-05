'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/users',
    'collections/lessons',
    'collections/concepts',
    'views/edit_lesson',
    'views/add_lesson',
    'text!templates/lesson_detail.html'
    ],

    function($, _, Backbone, Users, Lessons, Concepts, edit_lesson, add_lesson, lesson_detail_template){
        var LessonDetailView = Backbone.View.extend({
            template: _.template(lesson_detail_template),

            events:{
                'click #edit_lesson': 'editLesson',
                'click #add_lesson': 'addLesson'

            },

            initialize: function(){
                Backbone.on('lesson', this.get_lesson, this);
                this.listenTo(Lessons, 'reset', this.render);
                this.listenTo(Lessons, 'change', this.render);
                $('a[href="#lesson_content"]').on('hide.bs.tab', {add: false}, this.closeTab);

            },

            render: function () {
                this.model = Lessons.get(Lessons.unit_lesson)
                this.$el.html(this.template(this.model.toJSON()));
                MathJax.Hub.Queue(["Typeset",MathJax.Hub,'#lesson_content']);
		    },

            get_lesson: function(param){
                Lessons.unit = param['unit'];
                Lessons.unit_lesson = param['unit_lesson'];
                Lessons.fetch({data: {'ul_id': Lessons.unit_lesson}, reset:true});
                Concepts.fetch({data:{'unit_id': Lessons.unit}, reset:true});
                Backbone.history.navigate('lesson');
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

            closeTab: function(){
                Backbone.history.navigate();
            }

        });
	return LessonDetailView;
});