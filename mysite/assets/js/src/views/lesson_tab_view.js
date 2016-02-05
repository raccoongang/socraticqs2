'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/users',
    'collections/lessons',
    'collections/concepts',
    'models/lesson',
    'views/edit_lesson',
    'views/add_lesson',
    'text!templates/lesson_detail.html',
    'text!templates/sidebar_lessons.html'
    ],

    function($, _, Backbone, Users, Lessons, Concepts, lesson, edit_lesson, add_lesson, lesson_detail_template, sidebar_lesson_template){
        var LessonDetailView = Backbone.View.extend({
            template: _.template(lesson_detail_template),

            sidebar_template: _.template(sidebar_lesson_template),

            events:{
                'click #edit_lesson': 'editLesson',
                'click #add_lesson': 'addLesson'
                'click label': 'foo'
            },

            model: {},

            initialize: function(){
                Backbone.on('lesson', this.get_lesson, this);
                this.listenTo(Lessons,'reset', this.lessonsInSidebar);
                $('a[href="#lesson_content"]').on('hide.bs.tab', {add: false}, this.closeTab);

            },

            render: function () {
                $('#title').text(this.model.get('title'));
                this.$el.html(this.template(this.model.toJSON()));
                MathJax.Hub.Queue(["Typeset",MathJax.Hub,'#lesson_content']);
		    },

            get_lesson: function(param){
                Lessons.unit = param['unit'];
                Lessons.fetch({data: {'unit_id':Lessons.unit}, reset:true});
                this.model = new lesson({'id':param['unit_lesson']});
                this.listenTo(this.model, 'change', this.render);
                this.model.fetch();
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
            },

            lessonsInSidebar: function(){
                $('#sidebar_lessons').html(this.sidebar_template({all:Lessons.toJSON()}));
            },

            foo: function(){
                console.log('asdfsdfsaf')
            }

        });
	return LessonDetailView;
});
