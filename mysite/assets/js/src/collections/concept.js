'use strict';
define(['underscore', 'backbone', 'models/concept'], function (_, Backbone, Concept) {
    var fetch = Backbone.Collection.prototype.fetch;
    Backbone.Collection.prototype.fetch = function () {
        this.trigger('beforeFetch');
        return fetch.apply(this, arguments);
    };
    var ConceptCollection = Backbone.Collection.extend({
        model: Concept,

        url: '/ui/api/concept/',

        initialize: function () {
            this.on('add', this.onAdd, this);
            this.on('beforeFetch', this.beforeFetch, this);
            console.log(this.url);

        },


        compareBy: 'title',

        comparator: function (concept) {
            return Concept.get(this.compareBy);
        },

        onAdd: function () {
            console.log('Added Concept')
        },
        beforeFetch: function () {
            console.log("Before fetch");
            console.log(this.url);
        }

    });

    return new ConceptCollection;
});
