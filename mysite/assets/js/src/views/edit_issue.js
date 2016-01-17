'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'models/issue',
    'collections/issues',
    'text!templates/edit_issue.html'
    ],

    function($, _, Backbone, issue, Issues, add_issue){
        var AddIssueView = Backbone.View.extend({

            template: _.template(add_issue),

            events:{
                "click #ok_button": 'updateIssue',
                "click #cancel_button": "goBackToMainView",
            },

            initialize: function () {

            },

            render: function () {
                this.$el.empty();
                this.$el.html(this.template(this.model.toJSON()));

		    },

            updateIssue: function(){
                $('.has-error').removeClass('has-error');
                $('.help-block').addClass('hidden');
                var unindexed_array = $('#issue_form').serializeArray();
                var model_array = []
                $.map(unindexed_array, function(n, i){
                    model_array[n.name] = n.value;
                    });
                var temp_model = new issue(model_array);

                if (temp_model.isValid()){this.model.save(temp_model);}
                else{this.showErrors(temp_model.errors)}
            },

             goBackToMainView: function(){
                this.model.trigger('change');
            },

            showErrors: function(errors){
                for (var e in errors){
                    var $error = $('[name=' + e + ']'),
                    $group = $error.closest('.form-group');
                    $group.addClass('has-error');
                    $group.find('.help-block').removeClass('hidden').html(errors[e]);
                }
            }
        });
	return AddIssueView;
});