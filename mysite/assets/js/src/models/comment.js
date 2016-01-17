'use strict';
define(['underscore', 'backbone'], function(_, Backbone) {
    var comment = Backbone.Model.extend({
        defaults: {
            issue: 1,
            parent: 1,
            author: '',
            text: 'Empty comment',
            assignee: 'Unknown',
        },

        initialize: function() {
        },

        clear: function() {
            this.destroy();
            this.view.remove();
        }
    });
    return comment;
});