'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/concepts',
    'models/concept',
    'text!templates/concept_view.html',
    ],

    function($, _, Backbone, Concepts, concept, concept_view_template){
        var ConceptView = Backbone.View.extend({
            template: _.template(concept_view_template),


            model: concept,

            initialize: function(){
                //Backbone.on('concept', this.get_lesson, this);
                this.get_lesson();
                this.render();
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
		    },

            get_lesson: function(param){
                Concepts.fetch({data:{'unit_id': 1}, reset:true});
                Backbone.history.navigate('concept');
            },

            backFromEdit: function(){
              this.render();
            },

            closeTab: function(){
                Backbone.history.navigate();
            },

        });
	return ConceptView;
});
