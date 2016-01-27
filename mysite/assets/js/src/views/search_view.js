'use strict';
define([
        'jquery',
        'underscore',
        'backbone',
        'collections/searchItems',
        'text!templates/search_view.html',
        'text!templates/search_item.html'

    ],

    function ($, _, Backbone, SearchCollection, SearchTemplate, ItemTemplate) {
        var SearchView = Backbone.View.extend({
            template: _.template(SearchTemplate),
            item_template: _.template(ItemTemplate),
            events: {
                "keyup #searchText": "search",
                "click #search_button": "search",
                "click #close_search": "close_search",
            },

            initialize: function () {
                Backbone.on('newSearch', this.search, this);
                this.listenTo(SearchCollection, 'reset', this.render);
                Backbone.history.loadUrl();
            },

            search: function (param) {
                var search = (param.text) ? param.text : $('#searchText').val();
                if (search.length >= 3) {
                    SearchCollection.fetch({data: {text:search}, reset: true});
                }
            },

            //TRASH
            render: function () {
                this.close_search();
                this.$el.find("#result").html(this.template());
                var $self_el = $(this.el);
                var $self = this;
                _.each(SearchCollection.toJSON(), function(data){
                    $self_el.find("#search_table").append($self.item_template(data));
                })
            },
            close_search: function(){
                this.$el.find("#result").empty();
            }

        });
        return SearchView;
    }
);