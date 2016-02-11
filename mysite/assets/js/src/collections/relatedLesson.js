'use strict';
define(['underscore', 'backbone', 'models/relatedLesson'], function(_, Backbone, relatedLesson) {
    var RelatedLessonsCollection = Backbone.Collection.extend({
      model: relatedLesson,

      url: '/ui/api/related-lesson/',

      initialize: function(){
          this.on('add', this.onAdd, this);
      },


      compareBy:'title',

      comparator: function(issue) {
            return issue.get(this.compareBy);
      },

    });
    return new RelatedLessonsCollection;
});
