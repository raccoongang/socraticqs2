'use strict';
define([
    'jquery',
    'underscore',
    'backbone',
    'bootstrap'
    ],
    function($, _, Backbone){
        var DataView = Backbone.View.extend({
            tagName: 'tr',

            template: '',

            events: {
            },

            detailView:'',

            initialize: function () {
                console.log('adsfasf');
            },

            render: function () {

		    },

        });
	return DataView;
});


