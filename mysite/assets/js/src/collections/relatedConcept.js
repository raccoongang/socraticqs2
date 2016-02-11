'use strict';
define(['underscore', 'backbone', 'models/relatedConcept'], function(_, Backbone, relatedConcept) {
    var RelatedConceptCollection = Backbone.Collection.extend({
      model: relatedConcept,

      url: '/ui/api/related-concepts/',

      initialize: function(){
          this.on('add', this.onAdd, this);
      },

      compareBy:'title',

      comparator: function(concept) {
            return concept.get(this.compareBy);
      },

    });
    return new RelatedConceptCollection;
});
