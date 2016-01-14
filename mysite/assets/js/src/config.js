console.log('config required');

requirejs.config({
	paths: {
		"app" : "app",

	}
});

require(['app'],function(app){
	//app.run(); maybe
});