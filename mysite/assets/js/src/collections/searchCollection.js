'use strict';
define(['underscore', 'backbone', 'models/searchItem'], function(_, Backbone, searchItem) {
    var SearchCollection = Backbone.Collection.extend({
      model: searchItem,

      url: '/ui/api/search/',

      initialize: function(model, options){
          this.text = options.text.replace(/\+/g, ' ');
          this.query  = options.text
      },



      compareBy:'title',

      comparator: function(issue) {
            return issue.get(this.compareBy);
      },


      onAdd: function(){
          console.log('searchItem added')
      }
    });
    return new SearchCollection;
});
