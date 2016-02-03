'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'models/lesson',
    'collections/lessons',
    'text!templates/edit_lesson.html'
    ],

    function($, _, Backbone, lesson, Lessons, edit_lesson){
        var EditLessonView = Backbone.View.extend({

            template: _.template(edit_lesson),

            events:{
                "click #ok_button": 'updateLesson',
                "click #cancel_button": "goBackToMainView",
                "click .label_to_add": "addLabel",
                "click #labels>div>label": "removeLabel"
            },

            initialize: function () {
              this.listenTo(this.model, 'change', this.goBackToMainView);
            },

            render: function () {
                this.$el.empty();
                this.$el.html(this.template(this.model.toJSON()));
		    },

            getFormInfo: function(){
                var unindexed_array = $('#lesson_form').serializeArray();
                var for_template = {};
                $.map(unindexed_array, function(n, i){
                    for_template[n.name] = n.value;
                });
                return for_template;
            },

            updateLesson: function(){
                $('.has-error').removeClass('has-error');
                $('.help-block').addClass('hidden');
                var form_data = this.getFormInfo();
                var temp_model = new lesson(form_data);
                if (temp_model.isValid()){this.model.save(form_data);}
                else{this.showErrors(temp_model.errors)}
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
	return EditLessonView;
});