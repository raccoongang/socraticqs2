define(['jquery',
	    'backbone',
        'bootstrap',
	    'models/issue',
        'collections/issues',
        'views/issue_detail'],
function ($, Backbone, Bootstrap, issue, Issues, detail_view) {
	'use strict';

	var IssueRouter = Backbone.Router.extend({
		routes: {
            '(/)':'details',
            'issues/:issue_id(/)': 'showIssueDetail',
            'search=*text(/)':'search',
            'issues(/)': 'openIssues',
            'issues/*params(/)': 'is_open',
		},

        initialize: function(options) {
            $(document).on('click', 'a[href="#issues"]', {state: this}, this.openIssues);
             $('a[href="#details"]').on('click', {state: this}, this.openLesson);
             Backbone.history.on('checkurl', this.openLesson, this);
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
          var params_from_url = {};
          var firstPartOfPath = pathname.match( /(concepts|lessons|errors)\/\d+/ );
          if (firstPartOfPath){
              params_from_url['unit_lesson'] = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
          }
          firstPartOfPath = pathname.match( /units\/\d+/ );
          if (firstPartOfPath){
              params_from_url['unit'] = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
          }
          firstPartOfPath = pathname.match( /courses\/\d+/ );
          if (firstPartOfPath){
              params_from_url['course'] = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
          }
          return params_from_url;
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

            $('a[href="#issues"]').tab('show');
            var concept_id = this.getId();
            for (var attrname in concept_id) {
                dict_of_params[attrname] = concept_id[attrname];
            }
            Backbone.trigger('details',dict_of_params);
			Issues.trigger(dict_of_params['is_open']);
		},

        showIssueDetail: function(issue_id){
            Backbone.trigger('issue_details', {issue_id:issue_id});
            $('a[href="#issues"]').tab('show');
        },

        openLesson: function(e){
            Backbone.trigger('sidebar');
           if (e) {
                var params = e.data.state.getId();
            }
            else {
                var params = this.getId();
            }

            Backbone.trigger('details',params);
            $('a[href="#details"]').tab('show');
        },

        openIssues: function(e){
            if (e) {
                e.data.state.getIssues();
            }
            else {
                this.getIssues();
            }
            $('a[href="#issues"]').tab('show');
            Backbone.history.navigate('issues/')
        },

        details: function(){
            var params = this.getId();
            params['is_open']='open';
            Backbone.trigger('details',params);
            Backbone.trigger('issues_list',params);
            $('a[href="#details"]').tab('show');

        },


	});

	return IssueRouter;
});
