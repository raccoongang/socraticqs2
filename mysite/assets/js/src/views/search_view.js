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
                if (param.fromUrl == true) {
                    $('#searchText').val(param.text);
                }
                this.search = (param.text) ? param.text : $('#searchText').val();
                if (this.search.length >= 3) {
                    SearchCollection.fetch({data: {text:this.search}, reset: true});
                }
            },

            render: function () {
                this.pathname = window.location.pathname;
                $('nav + div').hide();
                var firstPartOfPath = this.pathname.match( /\/ct\/teach\/\w+\/\d+\/\w+\/\d+\/\w+\/\d+\/issues/ )[0];
                Backbone.history.navigate(firstPartOfPath+'/?search='+this.search);
                var $self_el = $(this.template());
                var $self = this;
                _.each(SearchCollection.toJSON(), function(data){
                    $self_el.find("#search_table").append($self.item_template(data));
                });
                $self_el.insertAfter('nav');
            },

            close_search: function(){
                $('nav + div').remove();
                $('nav + div').show();
                Backbone.history.navigate(this.pathname);

            }

        });
        return SearchView;
    }
);
