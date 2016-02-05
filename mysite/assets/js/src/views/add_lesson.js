'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'models/lesson',
    'collections/lessons',
    'collections/concepts',
    'text!templates/edit_add_lesson.html'
    ],

    function($, _, Backbone, lesson, Lessons, Concepts, edit_lesson){
        var AddLessonView = Backbone.View.extend({

            template: _.template(edit_lesson),

            events:{
                "click #ok_button": 'addLesson',
                "click #cancel_button": "goBackToMainView",
            },

            initialize: function () {
              this.listenTo(Lessons, 'add', function(){
                                            this.stopListening();
                                            this.undelegateEvents();});
              this.listenTo(this.model, 'change', this.goBackToMainView);
              this.model = new lesson({'author':window.settings.user,
                                        'unit_id':Lessons.unit,
                                        'title':'',
                                        'raw_text':''});

            },

            render: function () {
                this.$el.empty();
                var for_template = this.model.toJSON();
                for_template.concepts = Concepts.toJSON();
                this.$el.html(this.template(for_template));
		    },

            getFormInfo: function(model){
                var unindexed_array = $('#lesson_form').serializeArray();
                $.map(unindexed_array, function(n, i){
                    model.set(n.name, n.value);
                });
            },

            addLesson: function(){
                $('.has-error').removeClass('has-error');
                $('.help-block').addClass('hidden');
                console.log(this.model);
                this.getFormInfo(this.model);
                if (this.model.isValid()){Lessons.create(this.model,{wait:true});}
                else{this.showErrors(this.model.errors)}
            },

             goBackToMainView: function(){
                this.stopListening();
                this.undelegateEvents();
                this.trigger('cancel');
            },

            showErrors: function(errors){
                for (var e in errors){
                    var $error = $('[name=' + e + ']'),
                    $group = $error.closest('.form-group');
                    $group.addClass('has-error');
                    $group.find('.help-block').removeClass('hidden').html(errors[e]);
                }
            },


        });
	return AddLessonView;
});