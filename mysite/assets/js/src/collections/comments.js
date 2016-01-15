'use strict';
define(['underscore', 'backbone', 'models/comment'], function(_, Backbone, comment) {
    var CommentsCollection = Backbone.Collection.extend({
      model: comment,

      initialize: function(){
          this.on('add', this.onAdd, this)
      },

      onAdd: function(){
          console.log('Comment added')
      }
    });
    return new CommentsCollection;
});