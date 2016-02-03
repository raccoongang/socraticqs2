'use strict';
define(['underscore', 'backbone', 'models/lesson'], function(_, Backbone, lesson) {
    var LessonsCollection = Backbone.Collection.extend({
      model: lesson,

      url: '/ui/api/lesson/',

      initialize: function(){
          this.on('add', this.onAdd, this);
      },


      compareBy:'title',

      comparator: function(issue) {
            return issue.get(this.compareBy);
      },

      onAdd: function(){
          console.log('Lesson added')
      },

    });
    return new LessonsCollection;
});
