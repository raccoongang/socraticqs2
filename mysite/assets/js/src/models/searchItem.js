'use strict';
define(['underscore', 'backbone'], function (_, Backbone) {
    var SearchItem = Backbone.Model.extend({

        defaults: {
            'id': '',
            'title': '',
            'author': '',
            'kind': '',
        },

        initialize: function () {
            console.log('new SearchItem created');
        },

        clear: function () {
            this.destroy();
            this.view.remove();
        },

    });
    return SearchItem;
});

