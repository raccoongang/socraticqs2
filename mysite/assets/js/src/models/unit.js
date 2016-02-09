'use strict';
define(['underscore', 'backbone'], function(_, Backbone) {
    var unit = Backbone.Model.extend({

       defaults:{
        },

        urlRoot: '/ui/api/units/',

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
    return unit;
});


