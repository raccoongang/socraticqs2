'use strict';
define([
        'jquery',
        'underscore',
        'backbone',
        'collections/SearchCollection',
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
                Backbone.history.loadUrl();
                console.log("Searhc");
                this.search({keyCode: '1'});
                this.collection = new SearchCollection();
                this.collection.bind('all', this.render, this);
            },
            search: function () {
                var search = $('#searchText').val();
                if (search.length >= 3) {
                    this.collection.fetch({data: $.param({text: search})});
                    this.render();
                }
            },
            //TRASH
            render: function () {
                this.$el.find("#result").html(this.template());
                var $self_el = $(this.el);
                var $self = this;
                _.each(this.collection.toJSON(), function(data){
                    $self_el.find("#search_table").html($self.item_template(data));
                })
            },
            close_search: function(){
                this.$el.find("#result").empty();
            }

        });
        return SearchView;
    }
);