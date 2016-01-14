'use strict';
define([
  'jquery',
  'underscore',
  'backbone',
  'models/CommentModel'],

  function($, _, Backbone, CommentModel){

      var CommentCollection = Backbone.Collection.extend({
        model: CommentModel
      });
      return CommentCollection;

});
