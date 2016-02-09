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
    ],

    function($, _, Backbone, Users, Lessons, Concepts, lesson, edit_lesson, add_lesson, lesson_detail_template){
        var LessonDetailView = Backbone.View.extend({
            template: _.template(lesson_detail_template),

            events:{
                'click #edit_lesson': 'editLesson',
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
                console.log("tot");
                var view = new edit_lesson({model: this.model, el: this.el});
                this.listenToOnce(view, 'cancel', this.backFromEdit);
                view.render();
            },

            closeTab: function(){
                Backbone.history.navigate();
            },

        });
	return LessonDetailView;
});
