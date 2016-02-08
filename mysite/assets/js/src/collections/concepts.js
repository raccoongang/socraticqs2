'use strict';
define(['underscore', 'backbone', 'models/concept'], function(_, Backbone, concept) {
    var ConceptCollection = Backbone.Collection.extend({
      model: concept,

      url: '/ui/api/concepts/',

      initialize: function(){
          this.on('add', this.onAdd, this);
      },

      compareBy:'title',

      comparator: function(concept) {
            return concept.get(this.compareBy);
      },

      onAdd: function(){
          console.log('Is a concept');
      },

    });
    return new ConceptCollection;
});
