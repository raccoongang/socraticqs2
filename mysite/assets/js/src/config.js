console.log('config required');

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
		jquery: 'node_modules/jquery/dist/jquery',
		underscore:'node_modules/underscore/underscore',
		backbone: 'node_modules/backbone/backbone',
		text: 'node_modules/requirejs-text/text'
	}
});

//requirejs.config({
//	paths: {
//		"app" : "app",
//
//	}
//});
//
//require(['app'],function(app){
//	//app.run(); maybe
//});

require([
	'backbone',
	'views/main_tab_view',
], function (Backbone, AppView) {

	function getCookie(name) {
	    var matches = document.cookie.match(new RegExp(
	      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
	    ))
	    return matches ? decodeURIComponent(matches[1]) : undefined
	}

	var csrftoken = getCookie('csrftoken');
	var oldSync = Backbone.sync;
    Backbone.sync = function(method, model, options){
        options.beforeSend = function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        };
        return oldSync(method, model, options);
    };

	new AppView({el:$('#lesson_issues')});
});