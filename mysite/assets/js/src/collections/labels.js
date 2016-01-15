'use strict';
define(['underscore', 'backbone', 'models/label'], function(_, Backbone, label) {
    var LabelsCollection = Backbone.Collection.extend({
      model: label,

      initialize: function(){
          this.on('add', this.onAdd, this)
      },

      onAdd: function(){
          console.log('Label added')
      }
    });
    return new LabelsCollection;
});
