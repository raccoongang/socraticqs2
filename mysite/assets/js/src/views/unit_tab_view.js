'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'models/unit',
    'text!templates/lesson_detail.html',
    ],

    function($, _, Backbone, Users, Lessons, Concepts, unit){
        var LessonDetailView = Backbone.View.extend({
            template: _.template(lesson_detail_template),

            events:{
            },

            model: {},

            initialize: function() {
                this.get_unit();
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
                this.model = new lesson({'id':this.unit_lesson});
                this.listenTo(this.model, 'change', this.render);
                this.model.fetch();
                Concepts.fetch({data:{'unit_id': Lessons.unit}, reset:true});
            },

            editLesson: function(){
                var view = new edit_lesson({model: this.model, el: this.el});
                view.render();
            },

            closeTab: function(){
                Backbone.history.navigate();
            },

            openTab: function(){
                Backbone.history.navigate('lesson/');
            },

        });
	return LessonDetailView;
});
