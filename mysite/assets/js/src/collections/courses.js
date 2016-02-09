'use strict';
define(['underscore', 'backbone', 'models/course'], function(_, Backbone, course) {
    var CoursesCollection = Backbone.Collection.extend({
      model: course,

      url: '/ui/api/courses/',

      initialize: function(){
          this.on('add', this.onAdd, this);
      },


      compareBy:'id',

      comparator: function(issue) {
            return issue.get(this.compareBy);
      },

      onAdd: function(){
          console.log('Lesson added')
      },

    });
    return new CoursesCollection;
});
