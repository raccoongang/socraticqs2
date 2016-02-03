'use strict';
define(['underscore', 'backbone', 'models/issue'], function(_, Backbone, issue) {
    var ConceptCollection = Backbone.Collection.extend({
      model: issue,

      url: '/api//unit_concept/',

      initialize: function(){
          this.on('add', this.onAdd, this);
      },

      is_open: function() {
          return this.without.apply( this, this.is_close());
      },

      compareBy:'title',

      comparator: function(issue) {
            return issue.get(this.compareBy);
      },

      onAdd: function(){
          console.log('Is a live')
      },

    });
    return new ConceptCollection;
});
