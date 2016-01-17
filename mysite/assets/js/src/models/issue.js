'use strict';
define(['underscore', 'backbone'], function(_, Backbone) {
    var issue = Backbone.Model.extend({

        initialize: function() {
            console.log('new issue created');
        },

        clear: function() {
            this.destroy();
            this.view.remove();
        },

        toggle: function() {
            this.save({
                is_open: !this.get('is_open')
            });
        },

        validate: function(attrs, options) {
            var errors = this.errors = {};
            if (!attrs.title) errors.title = 'Title is required';
            if (!_.isEmpty(errors)) return errors;
        }
    });
    return issue;
});


