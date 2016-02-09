'use strict';
define(['underscore', 'backbone', 'models/unit'], function(_, Backbone, unit) {
    var UnitsCollection = Backbone.Collection.extend({
      model: unit,

      url: '/ui/api/units/',

      initialize: function(){
          this.on('add', this.onAdd, this);
      },


      compareBy:'order',

      comparator: function(issue) {
            return issue.get(this.compareBy);
      },

      onAdd: function(){
          console.log('Unit added')
      },

    });
    return new UnitsCollection;
});
