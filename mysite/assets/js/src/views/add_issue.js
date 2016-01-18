'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'models/issue',
    'collections/issues',
    'collections/labels',
    'collections/users',
    'views/label_view',
    'text!templates/edit_issue.html'
    ],

    function($, _, Backbone, issue, Issues, Labels, Users, label_view, add_issue){
        var AddIssueView = Backbone.View.extend({

            template: _.template(add_issue),

            events:{
                "click #ok_button": 'CreateNewIssue',
                "click #cancel_button": "goBackToMainView",
                "click .choices": "addLabel",
                "click #labels div label": "removeLabel"
            },

            initialize: function () {
                this.listenTo(Issues, 'add', function(){
                                            this.stopListening();
                                            this.undelegateEvents();});
                this.model = new issue({'author':window.settings.user,'labels':[]});
                this.for_template = this.model.toJSON();
            },

            render: function () {
                this.$el.empty();

                this.for_template['all_labels'] = Labels.toJSON();
                this.for_template['all_users'] = Users.toJSON();

                this.$el.html(this.template(this.for_template));

                var view = new label_view({model: this.model});
                this.$el.find('#labels').append(view.render().el);
		    },

            getFormInfo: function(){
                var model_array = [];
                var unindexed_array = $('#issue_form').serializeArray();
                $.map(unindexed_array, function(n, i){
                    model_array[n.name] = n.value;
                });
                model_array['labels'] = this.for_template.labels;
                return model_array;
            },

            CreateNewIssue: function(){
                $('.has-error').removeClass('has-error');
                $('.help-block').addClass('hidden');
                console.log(this.getFormInfo());
                var temp_model = new issue(this.getFormInfo());
                if (temp_model.isValid()){
                    Issues.create(temp_model);
                }
                else{
                    this.showErrors(temp_model.errors)
                }
            },

             goBackToMainView: function(){
                this.stopListening();
                this.undelegateEvents();
                Issues.trigger('reset');
            },

            showErrors: function(errors){
                for (var e in errors){
                    var $error = $('[name=' + e + ']'),
                    $group = $error.closest('.form-group');
                    $group.addClass('has-error');
                    $group.find('.help-block').removeClass('hidden').html(errors[e]);
                }
            },

            addLabel: function(event){
                this.for_template = this.getFormInfo();
                this.for_template.labels.push(parseInt(event.currentTarget.getAttribute('data')));
                this.render();
            },

            removeLabel: function(event){
                this.for_template = this.getFormInfo();
                this.for_template.labels.pop(parseInt(event.currentTarget.getAttribute('data')));
                this.render();
            }
        });
	return AddIssueView;
});