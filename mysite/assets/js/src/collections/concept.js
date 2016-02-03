'use strict';
define(['underscore', 'backbone', 'models/issue'], function (_, Backbone, issue) {
    var fetch = Backbone.Collection.prototype.fetch;
    Backbone.Collection.prototype.fetch = function () {
        this.trigger('beforeFetch');
        return fetch.apply(this, arguments);
    };
    var ConceptCollection = Backbone.Collection.extend({
        model: issue,

        url: '/api//unit_concept/',

        initialize: function () {
            this.on('add', this.onAdd, this);
            this.on('beforeFetch', this.beforeFetch, this);
            console.log(this.url);

        },

        is_open: function () {
            return this.without.apply(this, this.is_close());
        },

        compareBy: 'title',

        comparator: function (issue) {
            return issue.get(this.compareBy);
        },

        onAdd: function () {
            console.log('Is a live')
        },
        beforeFetch: function () {
            console.log("Before fetch");
            console.log(this.url);
        }

    });

    return new ConceptCollection;
});
