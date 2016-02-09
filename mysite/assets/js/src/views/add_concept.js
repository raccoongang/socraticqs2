'use strict';
define([
        'jquery',
        'underscore',
        'backbone',
        'models/concept',
        'collections/concepts',
        'collections/lessons',
        'text!templates/edit_add_concept.html'
    ],

    function ($, _, Backbone, concept, Concepts, Lessons, edit_concept) {
        var AddConceptView = Backbone.View.extend({

            template: _.template(edit_concept),

            events: {
                "click #ok_button": 'addConcept',
                "click #cancel_button": "goBackToMainView",
            },

            initialize: function () {
                this.listenTo(Concepts, 'add', this.goBackToMainView);
                this.listenTo(this.model, 'change', this.goBackToMainView);
                this.model = new concept({
                    'author': window.settings.user,
                    'unit_id': Concepts.unit,
                    'title': '',
                    'raw_text': ''
                });
            },

            render: function () {
                this.$el.empty();
                var for_template = this.model.toJSON();
                for_template.concepts = Concepts.toJSON();
                this.$el.html(this.template(for_template));
                window.cc = this.$el;
                console.log("this");
            },

            getFormInfo: function (model) {
                var unindexed_array = $('#concept_form').serializeArray();
                $.map(unindexed_array, function (n, i) {
                    model.set(n.name, n.value);
                });
            },

            addConcept: function () {
                $('.has-error').removeClass('has-error');
                $('.help-block').addClass('hidden');
                this.getFormInfo(this.model);
                if (this.model.isValid()) {
                    Concepts.create(this.model, {wait: true});
                }
                else {
                    this.showErrors(this.model.errors)
                }
            },

            goBackToMainView: function () {
                console.log("goBackToMainView");
                this.stopListening();
                this.undelegateEvents();
                var url = '/ui/hack/courses/'+Concepts.course+'/units/'+Concepts.unit+'/concepts/'+this.model.id+'/#concept';
                window.history.pushState("", "", url);
                Backbone.history.trigger('checkurl');

            },

            showErrors: function (errors) {
                for (var e in errors) {
                    var $error = $('[name=' + e + ']'),
                        $group = $error.closest('.form-group');
                    $group.addClass('has-error');
                    $group.find('.help-block').removeClass('hidden').html(errors[e]);
                }
            },


        });
        return AddConceptView;
    });