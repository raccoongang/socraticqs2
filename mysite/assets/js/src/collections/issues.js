'use strict';
define(['underscore', 'backbone', 'models/issue'], function(_, Backbone, issue) {
    var IssuesCollection = Backbone.Collection.extend({
      model: issue,

      url: '/api/issues/',

      initialize: function(){
          this.on('add', this.onAdd, this)
      },

      onAdd: function(){
          console.log('Issue added')
      }
    });
    return new IssuesCollection;
});
