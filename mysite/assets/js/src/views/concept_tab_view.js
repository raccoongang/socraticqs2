'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/users',
    'collections/concepts',
    'models/concept',
    'views/edit_concept',
    'views/add_concept',
    'text!templates/concept_view.html',
    ],

    function($, _, Backbone, Users, Concepts, concept, edit_concept, add_concept, lesson_view_template){
        var ConceptView = Backbone.View.extend({
            template: _.template(lesson_view_template),

            events:{
                'click #edit_concept': 'editConcept',

            },
            model: concept,

            initialize: function(){
                Backbone.on('concept', this.get_lesson, this);
                //$('a[href="#lesson_content"]').on('hide.bs.tab', {add: false}, this.closeTab);

            },

            render: function () {
                $('#title').text(this.model.get('title'));
                this.$el.html(this.template(this.model.toJSON()));
		    },

            get_lesson: function(param){
                this.listenTo(this.model, 'change', this.render);
                Concepts.fetch({data:{'unit_id': 1}, reset:true});
                Backbone.history.navigate('concept');
            },

            backFromEdit: function(){
              this.render();
            },

            editLesson: function(){
                var view = new edit_concept({model: this.model, el: this.el});
                this.listenToOnce(view, 'cancel', this.backFromEdit);
                view.render();
            },

            closeTab: function(){
                Backbone.history.navigate();
            },

        });
	return ConceptView;
});
