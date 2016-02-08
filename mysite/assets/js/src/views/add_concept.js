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
        var AddConceptView = Backbone.View.extend({

            template: _.template(edit_concept),

            events:{
                "click #ok_button": 'addConcept',
                "click #cancel_button": "goBackToMainView",
            },

            initialize: function () {
              this.listenTo(Concepts, 'add', function(){
                                            this.stopListening();
                                            this.undelegateEvents();});
              this.listenTo(this.model, 'change', this.goBackToMainView);
              this.model = new concept({'author':window.settings.user,
                                        'unit_id':Concepts.unit,
                                        'title':'',
                                        'raw_text':''});
            },

            render: function () {
                this.$el.empty();
                this.$el.attr("class", 'tab-pane');
                var for_template = this.model.toJSON();
                for_template.concepts = Concepts.toJSON();
                this.$el.html(this.template(for_template));
                window.cc = this.$el;
                console.log("this");
		    },

            getFormInfo: function(model){
                var unindexed_array = $('#concept_form_form').serializeArray();
                $.map(unindexed_array, function(n, i){
                    model.set(n.name, n.value);
                });
            },

            addConcept: function(){
                $('.has-error').removeClass('has-error');
                $('.help-block').addClass('hidden');
                console.log(this.model);
                this.getFormInfo(this.model);
                if (this.model.isValid()){Concepts.create(this.model,{wait:true});}
                else{this.showErrors(this.model.errors)}
            },

             goBackToMainView: function(){
                this.stopListening();
                this.undelegateEvents();
                this.trigger('cancel');
                this.$el.attr("class", 'tab-pane fade');

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
	return AddConceptView;
});