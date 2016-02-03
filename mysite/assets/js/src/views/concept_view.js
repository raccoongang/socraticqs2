'use strict';
define([
        'jquery',
        'underscore',
        'backbone',
        'collections/concept',
        'text!templates/concept_view.html',

    ],

    function ($, _, Backbone, ConceptCollection, ConceptTemplate) {
        var ConceptView = Backbone.View.extend({

            template: _.template(ConceptTemplate),

            events: {
                "click #concept-link": 'show',
            },

            initialize: function () {
                Backbone.on('Concept', this.show, this);
                this.listenTo(ConceptCollection, 'reset', this.render);
                Backbone.history.loadUrl();
                var $self = this;
                this.saved_url = '';
                window.cc = ConceptCollection;
                console.log("consf");
            },


            render: function () {
                this.pathname = window.location.pathname;
                var saved_url_lst = this.el.baseURI.split('#');
                if (saved_url_lst.length > 1) {
                    this.saved_url = saved_url_lst[1];
                }
                Backbone.history.navigate('=' + this.show + '/');
                var $self_el = $(this.template());
                var $self = this;
                _.each(ConceptCollection.toJSON(), function (data) {
                    $self_el.find("").append();
                });
                $self_el.insertAfter('');
            },
            show: function () {
                ConceptCollection.fetch();
            }
        });
        return ConceptView;
    }
);
