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
	'views/main_tab_view',
	'views/search_view',
	'utils/utils',
    'routers/router'
], function ($, Backbone, AppView, SearchView, utils, Workspace) {
    // Main access point for our app
    var router = new Workspace();
    Backbone.history.start();

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

	$('.nav-tabs').append('<li role="presentation" id="issues_tab"><a data-toggle="tab" href="#lesson_issues">Issues</a></li>');
	$('.nav-tabs').append('<li role="presentation" id="data_tab"><a data-toggle="tab" href="#data_issues" id="data-link">Data</a></li>');
	$('.tab-content').append('<div id="lesson_issues" class="tab-pane fade"></div>');
	$('.tab-content').append('<div id="data_issues" class="tab-pane fade">kjhkjhkjhkjhkjh</div>');
    $('<div class="navbar-form navbar-left" role="search" id="search_box"> <div class="form-group"> <input type="text" class="form-control" placeholder="Search" id="searchText"> </div> <button type="submit" class="btn btn-default" id="search_button">Go</button></div>').insertBefore('.navbar-right');

    new AppView({el:$('#lesson_issues')});
	new SearchView({el:$('#search_box')});

});
