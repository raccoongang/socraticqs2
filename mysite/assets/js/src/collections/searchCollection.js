'use strict';
define(['underscore', 'backbone', 'models/searchItem', 'views/search_view'], function(_, Backbone, searchItem, searchView) {
    var SearchCollection = Backbone.Collection.extend({
      model: searchItem,

      url: '/ui/api/search/',

      initialize: function(model, text){
          this.text = text;
          this.query  = text;
      },

      render: function(){

      },

      compareBy:'title',

      comparator: function(issue) {
            return issue.get(this.compareBy);
      },


      onAdd: function(){
          console.log('searchItem added')
      }
    });
    return SearchCollection;
});
