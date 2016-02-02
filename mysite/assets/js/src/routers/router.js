define(['jquery',
	    'backbone',
        'bootstrap',
	    'collections/issues'],
function ($, Backbone, Bootstrap, Issues) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
            '(/)':'getIssues',
            'search=*text(/)':'search',
            'issues(/)': 'openIssues',
            'issues/*params(/)': 'is_open'

		},

        search: function (text) {
            text = (typeof text !== 'undefined' & text !== null) ? text : '';
            if (text.length > 0) {
                Backbone.trigger('newSearch',{text:text, fromUrl: true, });
                var concept_id = this.getId();
                Backbone.trigger('unit_lesson', concept_id);
            }
        },

        getId: function(){
          var pathname = window.location.pathname;
          var firstPartOfPath = pathname.match( /(concepts|lessons|errors)\/\d+/ );
          if (firstPartOfPath){
              return {'unit_lesson':parseInt(firstPartOfPath[0].match(/\d+/)[0])};
          }
          firstPartOfPath = pathname.match( /units\/\d+/ );
          if (firstPartOfPath){
              return {'unit':parseInt(firstPartOfPath[0].match(/\d+/)[0])};
          }
          firstPartOfPath = pathname.match( /courses\/\d+/ );
          if (firstPartOfPath){
              return {'course':parseInt(firstPartOfPath[0].match(/\d+/)[0])};
          }
         },

		is_open: function (params) {
            var list_of_params = params.split('/');
            for (var each in list_of_params) {
                list_of_params[each]=list_of_params[each].split('=');
            }
            var dict_of_params = {};
            for (var each in list_of_params) {
                dict_of_params[list_of_params[each][0]]=list_of_params[each][1];
            }

            $('a[href="#lesson_issues"]').tab('show');
            var concept_id = this.getId();
            for (var attrname in concept_id) {
                dict_of_params[attrname] = concept_id[attrname];
            }
            Backbone.trigger('unit_lesson',dict_of_params);
			Issues.trigger(dict_of_params['is_open']);
		},

        openIssues: function(){
            this.getIssues();
            $('a[href="#lesson_issues"]').tab('show');
        },

        getIssues: function(){
            var ul_id = this.getId();
            ul_id['is_open']='open';
            Backbone.trigger('unit_lesson',ul_id);
        }
	});

	return IssueRouter;
});
