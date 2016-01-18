require.config({
	// The shim config allows us to configure dependencies for
	// scripts that do not call define() to register a module
	shim: {
		underscore: {
			exports: '_'
		},
		backbone: {
			deps: [
				'underscore',
				'jquery'
			],
			exports: 'Backbone'
		},
		backboneLocalstorage: {
			deps: ['backbone'],
			exports: 'Store'
		}
	},
	paths: {
		jquery: '../jquery/jquery',
		underscore:'../underscore/underscore',
		backbone: '../backbone/backbone',
		text: '../text/text'
	}
});

require([
	'backbone',
	'views/main_tab_view',
	'utils/utils',
], function (Backbone, AppView, utils) {
    // Main access point for our app
    var csrftoken = utils.getCookie('csrftoken');
    var oldSync = Backbone.sync;
    Backbone.sync = function(method, model, options){
        options.beforeSend = function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        };
        return oldSync(method, model, options);
    };

    new AppView({el:$('#lesson_issues')});
});
