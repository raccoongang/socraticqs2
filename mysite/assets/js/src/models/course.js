'use strict';
define(['underscore', 'backbone'], function(_, Backbone) {
    var course = Backbone.Model.extend({

       defaults:{
        },

        urlRoot: '/ui/api/courses/',

        initialize: function() {
        },

        clear: function() {
            this.destroy();
            this.view.remove();
        },

        validate: function(attrs, options) {
            var errors = this.errors = {};
            if (!attrs.title) errors.title = 'Title is required';
            if (!_.isEmpty(errors)) return errors;
        }
    });
    return course;
});


