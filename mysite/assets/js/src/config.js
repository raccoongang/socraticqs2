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
        bootstrap : {
            deps :['jquery']
        }
    },
		paths: {
		jquery: '../jquery/jquery',
		underscore:'../underscore/underscore',
		backbone: '../backbone/backbone',
		text: '../text/text',
        bootstrap: '../bootstrap/dist/js/bootstrap.min'
	}
});

require([
	'jquery',
	'backbone',
	'views/tabs_view',
	'views/search_view',
    'views/sidebar_view',
	'utils/utils',
    'routers/router'
], function ($, Backbone, AppView, SearchView, SidebarView, utils, Workspace) {
    // Main access point for our app

    var router = new Workspace();

    var csrftoken = utils.getCookie('csrftoken');
    var oldSync = Backbone.sync;
    Backbone.sync = function(method, model, options){
        options.beforeSend = function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        };
		var _url = _.isFunction(model.url) ?  model.url() : model.url;
    	_url += _url.charAt(_url.length - 1) == '/' ? '' : '/';
    	options.url = _url;
        return oldSync(method, model, options);
    };


    $('<div class="navbar-form navbar-right" role="search" id="search_box"> <div class="form-group"> <input type="text" class="form-control" placeholder="Search" id="searchText"> </div> <button type="submit" class="btn btn-default" id="search_button">Go</button></div>').insertBefore('.navbar-right');
    //$('nav').next('div').andSelf().wrapAll('<div class="container-fluid" style="padding-left: 300px;"/>');
    //$('body').append('<nav class="navmenu navmenu-default navmenu-fixed-left" role="navigation">sadf</nav>');

    new SidebarView({el:$('#sidebar')});
	new SearchView({el:$('#search_box')});
    new AppView({el:$('#div_for_tabs')});
    Backbone.trigger('sidebar');

});
