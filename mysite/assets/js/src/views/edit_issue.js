'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'models/issue',
    'collections/issues',
    'collections/labels',
    'views/label_view',
    'text!templates/edit_issue.html'
    ],

    function($, _, Backbone, issue, Issues, Labels, label_view, add_issue){
        var EditIssueView = Backbone.View.extend({

            template: _.template(add_issue),

            events:{
                "click #ok_button": 'updateIssue',
                "click #cancel_button": "goBackToMainView",
                "click .choices": "addLabel",
                "click #labels>div>label": "removeLabel"
            },

            initialize: function () {
                this.for_template = this.model.toJSON();
                this.listenTo(this.model, 'change', function(){this.stopListening();
                this.undelegateEvents();});
            },

            render: function () {
                this.$el.empty();
                this.for_template['all_labels'] = Labels.toJSON();
                this.$el.html(this.template(this.for_template));
                var view = new label_view({model: this.model});
                this.$el.find('#labels').append(view.render().el);
		    },

            updateIssue: function(){
                $('.has-error').removeClass('has-error');
                $('.help-block').addClass('hidden');
                var unindexed_array = $('#issue_form').serializeArray();
                var model_array = []
                $.map(unindexed_array, function(n, i){
                    model_array[n.name] = n.value;
                    });
                model_array['labels']=this.for_template.labels;
                var temp_model = new issue(model_array);

                if (temp_model.isValid()){this.model.save(model_array);}
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
            },

            addLabel: function(event){
                this.for_template.labels.push(parseInt(event.currentTarget.getAttribute('data')));
                this.render();

            },

            removeLabel: function(event){
                var index = this.for_template.labels.indexOf(parseInt(event.currentTarget.getAttribute('data')));
                this.for_template.labels.splice(index, 1);
                this.render();
            }
        });
	return EditIssueView;
});