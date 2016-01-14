function truncate(str, len) {
    return (str.length > len) ? str.substr(0, len - 3) + '&hellip;' : str;
}

function show_info(title, description, author) {
    $('.nav-tabs a[href="#lesson_description"]').tab('show');
    $('#title').empty().text(title);
    $('#description').empty().append(description);
    $('#author').empty().text(author);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, ".content"]);
}

function show_search_info(title, description, author) {
    $('#title_search').empty().text(title);
    $('#description_search').empty().append(description);
    $('#author_search').empty().text(author);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, ".search_content"]);
}

function get_content_for_unit(unit_id, course_id) {
    var url = '/ui/api/units/' + unit_id + '/content/';
    $('#panel_for_tabs').append('<div id="unit' + unit_id + '" class="collapse in unit"><div class="well"></div></div>');
    var tab_for_unit = $('#unit' + unit_id + ' .well');
    $.get(url).done(function (content) {
        var lessons = content['lessons'];
        var concepts = content['concepts'];
        tab_for_unit.append('<div class="btn-group btn-group-justified" role="group" aria-label="lessons"><div class="btn-group" role="group" style="width:80%;"><button type="button" class="btn btn-default" data-toggle="collapse" data-target="#lessons' + unit_id + '" aria-expanded="true" aria-controls="lesson1">Lessons</button></div><div class="btn-group" role="group" style="width:20%;"> <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus-sign"></span>&nbsp; </button> </div> </div>');
        tab_for_unit.append('<div id="lessons' + unit_id + '" class="collapse in"><div class="well"><ul></ul></div></div>');
        var lessons_tab = $('#lessons' + unit_id + ' .well ul');
        for (lesson in lessons) {
            var x = $('<li><a class="lesson" lesson_id="' + lessons[lesson]['id'] + '" href="#" lesson_order="' + lessons[lesson]['order'] + '">"' + lessons[lesson]['lesson_title'] + '</a></li>');
            lessons_tab.append(x);
            $('.lesson').draggable({revert: true, axis: "y"});
        $(x).droppable({
            drop: function (event, ui) {
                $('#blank_div').remove();
                var a = $(this).find('a');
                var ul_id = ui.draggable.attr('lesson_id');
                var order = a.attr('lesson_order');
                var url = '/ui/api/units/' + unit_id + '/content/';
                $.ajax({
                    url: url,
                    type: 'PUT',
                    data: {'ul_id': ul_id, 'order': order},
                    success: function (result) {
                        get_units_for_course(course_id);
                    }
                });
            },
            over: function () {
                $(this).find('a').before('<div style="height:0px;width:100%;" id="blank_div"></span></div>');
                $('#blank_div').animate({'height': '+=35px'}, 500);
            },
            out: function () {
                $('#blank_div').remove();
            }
        });

    }
    tab_for_unit.append('<div class="btn-group btn-group-justified" role="group" aria-label="concepts"><div class="btn-group" role="group" style="width:80%;"><button type="button" class="btn btn-default" data-toggle="collapse" data-target="#concepts' + unit_id + '" aria-expanded="true" aria-controls="lesson1">Concepts</button></div><div class="btn-group" role="group" style="width:20%;"> <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus-sign"></span>&nbsp; </button> </div> </div>');
    tab_for_unit.append('<div id="concepts' + unit_id + '" class="collapse in"><div class="well"><ul></ul></div></div>');
    var conceptss_tab = $('#concepts' + unit_id + ' .well ul');
    for (concept in concepts) {
        conceptss_tab.append('<li><a class="concept" concept_id="' + concepts[concept]['ul_id'] + '" href="#">' + concepts[concept]['title'] + '</a></li>');
    }
}
)
;
}

function get_units_for_course(course_id) {
    $('#issues_tab').addClass("disabled");
    $('#issues_tab a').attr('href', '#');
    var url = '/ui/api/courses/' + course_id + '/units/';
    $.get(url).done(function (units) {
        this.course_tab = $('#panel_for_tabs');
        this.course_tab.empty();
        for (unit_num in units) {
            var unit = units[unit_num];
            var unit_tab_html = '<div class="btn-group btn-group-justified" role="group" aria-label="units"><div class="btn-group" role="group" style="width:80%;"> <button type="button" class="btn btn-default" data-toggle="collapse" data-target="#unit' + unit['unit_id'] + '" aria-expanded="true" aria-controls="unit1">' + truncate(unit['unit_title'], 28) + '</button> </div> </div>';
            this.course_tab.append(unit_tab_html);
            get_content_for_unit(unit['unit_id'], course_id);
        }
    });
}

$(document).ready(function () {
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function (xhr, settings) {
            var csrfSafeMethod = function (method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            };
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
    $('.search').hide();
    $('.search_content').hide();
    $('#add_issue_form').hide();
    var url = '/ui/api/courses/';
    $.get(url).done(function (courses) {
        this.courses_tabs = $('#courses_tabs');
        for (course_num in courses) {
            var course = courses[course_num];
            var course_tab_html = '<li><a href="#course_' + course['id'] + '" data-toggle="tab" course-id="' + course['id'] + '">' + course['title'] + '</a></li>'
            this.courses_tabs.append(course_tab_html);
        }
        $('a[href="#course_' + courses[0]['id'] + '"]').trigger('click');
    });
});
$(document).on('shown.bs.offcanvas', '#coursesTree', function () {
    $('#arrow_on_button').rotate({
        angle: 0,
        animateTo: 180,
        duration: 600
    });
});
$(document).on('hidden.bs.offcanvas', '#coursesTree', function (e) {
    $('#arrow_on_button').rotate({
        angle: 180,
        animateTo: 0,
        duration: 600
    });
});

$(document).on('click', 'a[data-toggle="tab"]', function (course) {
    var course_id = $(course.target).attr('course-id');
    if (course_id) {
        get_units_for_course(course_id);
        var url = '/ui/api/course/' + course_id;
        $.get(url, {'format': 'json'}).done(function (course) {
            show_info(course['title'], course['description'], course['added_by']);
        });
    }
    return false;
});

$(document).on('click', '.lesson', function () {
    $('#issues_tab').removeClass("disabled");
    $('#issues_tab a').attr('href', '#lesson_issues');
    var lesson_id = this.getAttribute('lesson_id');
    active_lesson_id = lesson_id;
    var url = '/ui/api/lesson/' + lesson_id + '/';
    $.get(url).done(function (lesson) {
        $('.content').show();
        $('.search').hide();
        show_info(lesson['title'], lesson['text'], lesson['added_by']);
    });
    $('.search_content').hide();
    $('.search').hide();
    $('#search_text').val('');
    return false;
});

$(document).on('click', '.search_lesson', function () {
    var unit_id = this.getAttribute('lesson_id');
    var url = '/ui/api/lesson/' + unit_id + '/';
    $.get(url).done(function (lesson) {
        $('.content').hide();
        $('.search').hide();
        $('.search_content').show();
        show_search_info(lesson['title'], lesson['text'], lesson['added_by']);
    });
    return false;
});

$(document).on('click', '.concept', function () {
    $('#issues_tab').removeClass("disabled");
    $('#issues_tab a').attr('href', '#lesson_issues');
    var concept_id = this.getAttribute('concept_id');
    active_lesson_id = concept_id;
    var url = '/ui/api/concept/' + concept_id + '/';
    $.get(url).done(function (concept) {
        $('.content').show();
        $('.search').hide();
        $('.search_content').hide();
        $('#search_text').val('');
        show_info(concept['title'], concept['text'], concept['added_by']);
    });
    return false;
});

$(document).on('click', '#search_text', function () {
    return false;
});

$(document).on('click', '#search_button', function () {
    var text_to_search = $('#search_text').val();
    var url = '/ui/api/search/';
    $.get(url, {'text': text_to_search}).done(function (find_result) {
        $('.content').hide();
        $(".search_content").hide();
        $('.search').show();
        $('#search_table').empty();
        var table = $('#search_table');
        for (lesson in find_result) {
            var this_lesson = find_result[lesson];
            table.append('<tr><td><a class="search_lesson" href="#" lesson_id=' + this_lesson["id"] + '>' + this_lesson["title"] + '</a></td><td>' + this_lesson["kind"] + '</td><td>' + this_lesson["author"] + '</td></tr>');
        }
        $('.search_lesson').draggable({revert: true});
    });
    return false;
});

$(document).on('click', '#close_search', function () {
    $('.content').show();
    $('.search').hide();
    $('#search_text').val('');
    return false;
});

$(document).on('click', '#back_to_search', function () {
    $('.search').show();
    $('.search_content').hide();
    return false;
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).on('click', '#add_issue_button', function () {
    $('.inp').removeClass('error_input');
    var url = '/ui/api/issues/';
    var data = $('#add_issue_form').serialize();
    $.post(url, data).done(function () {
        $('a[href="#lesson_issues"]').trigger('click');
        $('#add_issue_form').hide();
        $('#lesson_issues_table').show();
    }).fail(function (result) {
        for (each in result['responseJSON']) {
            $('[name="' + each + '"]').addClass('error_input');
            $('[name="' + each + '"]').attr('placeholder', result['responseJSON'][each]);
        }
    })
    return false;
});

$(document).on('click', '#add_issue_cancel_button', function () {
    $('#add_issue_form').hide();
    $('#lesson_issues_table').show();
    return false;
});

$(document).on('click', '#show_issue_cancel_button', function () {
    $('#show_issue_div').hide();
    $('#lesson_issues_table').show();
    return false;
});

function add_filters(authors, assignee, labels) {
    $('#dropdown_author').empty();
    $('#dropdown_assignee').empty();
    $('#dropdown_labels').empty();
    for (x in authors) {
        $('#dropdown_author').append('<li><a href="#" filter="' + authors[x] + '" field="author_name">' + authors[x] + '</a></li>');
    }
    $('#dropdown_author').append('<li role="separator" class="divider"></li><li><a href="#" filter="all" field="author_name">Show all</a></li>');
    for (x in assignee) {
        $('#dropdown_assignee').append('<li><a href="#" filter="' + assignee[x] + '" field="assignee_name">' + assignee[x] + '</a></li>');
    }
    $('#dropdown_assignee').append('<li role="separator" class="divider"></li><li><a href="#" filter="all" field="author_name">Show all</a></li>');
    for (x in labels) {
        $('#dropdown_labels').append('<li><a href="#" filter="' + labels[x] + '" field="labels">' + list_of_labels[labels[x]] + '</a></li>');
    }
    $('#dropdown_labels').append('<li role="separator" class="divider"></li><li><a href="#" filter="all" field="author_name">Show all</a></li>');

}

function get_labels() {
    var labels_url = '/ui/api/labels/';
    $('[name="labels"]').empty();
    $.get(labels_url).done(function (labels) {
        for (each in labels) {
            var label = labels[each];
            list_of_labels[label['id']] = label['title'];
            $('[name="labels"]').append('<option value="' + label['id'] + '">' + label['title'] + '</option>')
        }
    });
}

function show_one_type_of_issues() {
    get_labels();
    var url = '/ui/api/issues/';
    var open_issues = 0;
    var close_issues = 0;
    var authors = [];
    var assignee = [];
    var labels = [];
    $.get(url, {'unit_lesson': active_lesson_id}).done(function (issues) {
        list_of_issues = issues;

        $('#table_of_issues').empty();

        $('#table_of_issues').append('<tr class="active"><td>Title</td><td>Label</td><td>Author</td></tr>');
        for (each in list_of_issues) {
            var issue = list_of_issues[each];
            if (issue['is_open']) {
                open_issues += 1;
            }
            else {
                close_issues += 1;
            }
            var span_affected = '';
            if (issue['affected_count'] > 1) {
                span_affected = '<span class="label label-pill label-danger">' + issue['affected_count'] + '</span>';
            }
            if (issue['is_open'] == is_open_shown) {
                $('#table_of_issues').append('<tr><td><a href="#" issue_id="' + issue['id'] + '" class="issue">' + issue['title'] + '</a> ' + span_affected + '</td><td>' + list_of_labels[issue['labels'][0]] + '</td><td>' + issue['author_name'] + '</td></tr>'
                )
                if (authors.indexOf(issue['author_name']) == -1 && issue['author_name'] != null) {
                    authors.push(issue['author_name']);
                }
                if (assignee.indexOf(issue['assignee_name']) == -1 && issue['assignee_name'] != null) {
                    assignee.push(issue['assignee_name']);
                }
                if (labels.indexOf(issue['labels'][0]) == -1 && issue['labels'][0] != null) {
                    labels.push(issue['labels'][0]);
                }
            }
        }
        add_filters(authors, assignee, labels);
        get_assignee();


        $('#closed_span').text(close_issues);
        $('#open_span').text(open_issues);
    });
};

$(document).on('click', 'a[href="#lesson_issues"]', function () {
    $('#add_issue_form').hide();
    $('#lesson_issues_table').show();
    $('#show_issue_div').hide();

    if ($(this).closest('li').hasClass('disabled') == false) {

        show_one_type_of_issues();
    }
    ;
    return false;

});

function get_assignee() {
    var assignee_url = '/ui/api/assignee/';
    $('[name="assignee"]').empty();
    $.get(assignee_url).done(function (assignees) {
        for (each in assignees) {
            var assignee = assignees[each];
            $('[name="assignee"]').append('<option value="' + assignee['id'] + '">' + assignee['username'] + '</option>')
        }
    })
}

$(document).on('click', ".issue", function () {
    window.current_issue_id = +this.getAttribute('issue_id');
    var url = '/ui/api/issues/' + window.current_issue_id;
    get_assignee();
    get_labels();
    $.get(url).done(function (issue) {
        var is_open = issue['is_open'];
        $("#show_issue_title").text(issue['title']);
        $("#show_issue_description").text(issue['description']);
        $("#show_issue_author").text(issue['author_name']);
        $("#show_issue_assignee").text(issue['assignee_name']);
        $("#show_issue_label").text(list_of_labels[issue['labels'][0]]);
        $('[name="is_open"]').val(is_open);
        if (is_open) {
            $("#is_open_button").text('Close issue').removeClass('btn-danger').addClass('btn-success');
        }
        else {
            $("#is_open_button").text('Reopen issue').removeClass('btn-success').addClass('btn-danger');
        }
        $('[name="title"]').val(issue['title']);
        $('[name="description"]').val(issue['description']);
        $('[name="id"]').val(issue['id']);
        $('[name="labels"]').val(issue['labels'][0]);
        $('[name="unit_lesson"]').val(active_lesson_id);
    });
    $('#lesson_issues_table').hide();
    $('#show_issue_div').show();
    $('#show_issue_inside_div').show();
    $('#update_issue_form').hide();

    //Load comments
    var commnets_url = '/ui/api/comments/?issue_id=' + window.current_issue_id;
    $.get(commnets_url).done(function (comments) {
        var comments_block = $('#comments_div');
        window.com = comments;
        $.each(comments, function (index, value) {
            var comment = '<div>' +
                '<p>' + value['author_name'] + '</p>' +
                '<p>' + value['text'] + '</p>' +
                '</div>';
            comments_block.append(comment);
        })
    });

    return false;
});

$(document).on('click', '#add_new_issue', function () {
    $('.inp').val('');
    $('.inp').removeClass('error_input');
    $('.inp').attr('placeholder', '');
    $('#add_issue_form').show();
    $('#lesson_issues_table').hide();
    $('#show_issue_div').hide();
    $('[name="unit_lesson"]').val(active_lesson_id);
    return false;
});

$(document).on('click', '#edit_issue_button', function () {
    $('#show_issue_inside_div').hide();
    $('#update_issue_form').show();
    return false;
})

$(document).on('click', '#update_issue_cancel_button', function () {
    $('#show_issue_inside_div').show();
    $('#update_issue_form').hide();
    return false;
})

$(document).on('click', '#update_issue_button', function () {
    var issue_id = $('[name="id"]').val();
    var url = '/ui/api/issues/' + issue_id
    $('.inp').removeClass('error_input');
    $('.inp').attr('placeholder', '');
    $('[name="unit_lesson"]').val(active_lesson_id);
    $.ajax({
        url: url,
        type: 'PUT',
        data: $('#update_issue_form').serialize(),
        success: function (result) {
            show_one_type_of_issues();
            $('[issue_id="' + issue_id + '"]').trigger('click');
        },
        error: function (result) {
            for (each in result['responseJSON']) {
                $('[name="' + each + '"]').addClass('error_input');
                $('[name="' + each + '"]').attr('placeholder', result['responseJSON'][each]);
            }
        }
    });
    return false;
});

$(document).on('click', '.dropdown-menu li a', function () {
    var filter = $(this).attr('filter');
    var field = $(this).attr('field');
    $('#table_of_issues').empty();
    $('#table_of_issues').append('<tr class="active"><td>Title</td><td>Label</td><td>Author</td></tr>');
    for (each in list_of_issues) {
        var issue = list_of_issues[each];
        if (issue['is_open'] == is_open_shown) {
            if (issue[field] == filter || filter == 'all') {
                $('#table_of_issues').append('<tr><td><a href="#" issue_id="' + issue['id'] + '" class="issue">' + issue['title'] + '</a></td><td>' + list_of_labels[issue['labels'][0]] + '</td><td>' + issue['author_name'] + '</td></tr>'
                )
            }
        }
    }
});

$(document).on('click', '#is_open_button', function () {
    if ($(this).hasClass('btn-success')) {
        $('[name="is_open"]').val(false);
    }
    else {
        $('[name="is_open"]').val(true);
    }
    $('#update_issue_button').trigger('click');
    return false;
});

$(document).on('click', '#opened_issues', function () {
    $('#open_link_th').addClass('success');
    $('#close_link_th').removeClass('success');
    is_open_shown = true;
    show_one_type_of_issues();
});
$(document).on('click', '#closed_issues', function () {
    $('#close_link_th').addClass('success');
    $('#open_link_th').removeClass('success');
    is_open_shown = false;
    show_one_type_of_issues();
});
$(document).on('click', '#add_comment_button', function () {
    var url = '/ui/api/comments/'
    var text = $('#comments_text');
    //$("#add_comment_button").disable();
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            text: text.val(),
            issue: window.current_issue_id,
            author: window.user_id
        },
        success: function (result) {
            var comment = '<div>' +
                '<p>' + window.user_id + '</p>' +
                '<p>' + text.val() + '</p>' +
                '</div>';
            $('#comments_div').append(comment);
            text.val("");

        },
        error: function (result) {
            for (each in result['responseJSON']) {
                $('[name="' + each + '"]').addClass('error_input');
                $('[name="' + each + '"]').attr('placeholder', result['responseJSON'][each]);
            }
        }
    });
    return false;
})
