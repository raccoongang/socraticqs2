'use strict';
define(['underscore', 'backbone'], function(_, Backbone) {
    var issue = Backbone.Model.extend({

        initialize: function() {
            console.log('new issue created');
        },

        clear: function() {
            this.destroy();
            this.view.remove();
        }
    });
    return issue;
});


