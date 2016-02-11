'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'mathjax',
    'collections/users',
    'collections/lessons',
    'collections/concepts',
    'models/lesson',
    'views/edit_lesson',
    'views/add_lesson',
    'text!templates/lesson_detail.html',
    ],

    function($, _, Backbone, MathJax, Users, Lessons, Concepts, lesson, edit_lesson, add_lesson, lesson_detail_template){
        var LessonDetailView = Backbone.View.extend({
            template: _.template(lesson_detail_template),

            events:{
                'click #edit_lesson': 'editLesson',
            },

            model: {},

            initialize: function() {
                this.get_lesson();
                $('a[href="#'+this.$el.attr("id")+'"]').on('shown.bs.tab', this.openTab);
            },

            render: function () {
                $('#title').text(this.model.get('title'));
                this.$el.html(this.template(this.model.toJSON()));
                MathJax.Hub.Queue(["Typeset",MathJax.Hub,'#details']);
		    },

            get_lesson: function(){
                var pathname = window.location.pathname;
                var firstPartOfPath = pathname.match( /(concepts|lessons|errors)\/\d+/ );
                if (firstPartOfPath) {
                    this.unit_lesson = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                }
                firstPartOfPath = pathname.match( /units\/\d+/ );
                if (firstPartOfPath){
                   this.unit = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
                }
                this.model = new lesson({'id':this.unit_lesson});
                this.listenTo(this.model, 'change', this.render);
                this.model.fetch();
                Concepts.fetch({data:{'unit_id': this.unit}, reset:true});
            },

            editLesson: function(){
                var view = new edit_lesson({model: this.model, el: this.el});
                view.render();
            },

            openTab: function(){
                Backbone.history.navigate();
            },

        });
	return LessonDetailView;
});
