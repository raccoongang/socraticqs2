'use strict';
define([
  'jquery',
  'underscore',
  'backbone',
  'models/IssueModel'],

  function($, _, Backbone, IssueModel){

      var IssueCollection = Backbone.Collection.extend({
        model: IssueModel
      });
      return IssueCollection;

});
