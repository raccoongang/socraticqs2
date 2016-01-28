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
                var $elf = this;
                $('body').on('click', '#close_search', function(){
                    $elf.close_search();
                });
            },

            search: function (param) {
                if (param.fromUrl == true) {
                    $('#searchText').val(param.text);
                }
                this.search = (param.text) ? param.text : $('#searchText').val();
                if (this.search.length % 3 == 0 && this.search.length !== 0) {
                    SearchCollection.fetch({data: {text:this.search}, reset: true});
                }
            },

            render: function () {
                this.pathname = window.location.pathname;
                $('nav + div').hide();
                Backbone.history.navigate('search='+this.search+'/');
                var $self_el = $(this.template());
                var $self = this;
                _.each(SearchCollection.toJSON(), function(data){
                    $self_el.find("#search_table").append($self.item_template(data));
                });
                $self_el.insertAfter('nav');
            },

            close_search: function(){
                $('nav + div').remove();
                $('#searchText').val('');
                Backbone.history.navigate(this.pathname);

            }

        });
        return SearchView;
    }
);
