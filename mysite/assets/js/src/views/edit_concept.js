'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'models/concept',
    'collections/concepts',
    'text!templates/edit_add_concept.html'
    ],

    function($, _, Backbone, concept, Concepts, edit_concept){
        var EditConceptView = Backbone.View.extend({

            template: _.template(edit_concept),

            events:{
                "click #ok_button": 'updateLesson',
                "click #cancel_button": "goBackToMainView",
            },

            initialize: function () {
              this.listenTo(this.model, 'change', this.goBackToMainView);
            },

            render: function () {
                this.$el.empty();
                this.$el.html(this.template(this.model.toJSON()));
		    },

            getFormInfo: function(){
                var unindexed_array = $('#concept_form').serializeArray();
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
                var temp_model = new concept(form_data);
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
	return EditConceptView;
});