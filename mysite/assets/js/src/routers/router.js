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
            '(/)':'getIssues',
            'issues/:issue_id(/)': 'showIssueDetail',
            'search=*text(/)':'search',
            'issues(/)': 'openIssues',
            'issues/*params(/)': 'is_open',
            'lesson(/)': 'openLesson'

		},

        initialize: function(options) {
             $('a[href="#lesson_issues"]').on('click', {state: this}, this.openIssues);
             $('a[href="#lesson_content"]').on('click', {state: this}, this.openLesson);

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
          var return_dict = {};
          var firstPartOfPath = pathname.match( /(concepts|lessons|errors)\/\d+/ );
          if (firstPartOfPath){
              return_dict['unit_lesson'] = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
          }
          firstPartOfPath = pathname.match( /units\/\d+/ );
          if (firstPartOfPath){
              return_dict['unit'] = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
          }
          firstPartOfPath = pathname.match( /courses\/\d+/ );
          if (firstPartOfPath){
              return_dict['course'] = parseInt(firstPartOfPath[0].match(/\d+/)[0]);
          }
          return return_dict;
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

        showIssueDetail: function(issue_id){
            var model = new issue({id:issue_id});
            model.fetch();
            this.listenToOnce(model, 'change', function () {
                            $('a[href="#lesson_issues"]').tab('show');
                            this.detailView = new detail_view({model: model, el: $('#lesson_issues')});
                            this.detailView.render();
                            });

        },

        openLesson: function(e){
            if (e) {
                var ul_id = e.data.state.getId();
            }
            else {
                var ul_id = this.getId();
            }

            Backbone.trigger('lesson',ul_id);
            $('a[href="#lesson_content"]').tab('show');
            Backbone.history.navigate('lesson/');
        },

        openIssues: function(e){
            if (e) {
                e.data.state.getIssues();
            }
            else {
                this.getIssues();
            }
            $('a[href="#lesson_issues"]').tab('show');
            Backbone.history.navigate('issues/')
        },

        getIssues: function(){
            var ul_id = this.getId();
            ul_id['is_open']='open';
            Backbone.trigger('unit_lesson',ul_id);
            Backbone.trigger('lesson',ul_id);
        },


	});

	return IssueRouter;
});
