'use strict';
define([
  'jquery',
  'underscore',
  'backbone',
  'models/LabelModel'],

  function($, _, Backbone, LabelModel){

      var LabelCollection = Backbone.Collection.extend({
        model: LabelModel
      });
      return LabelCollection;

});
