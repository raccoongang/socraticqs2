// One row with issue template
<script type="text/template" id="issue">
    <tr>
        <td>
            <a href="#"> <%= title%> </a>
        </td>
        <td>
            <%= labels %>
        </td>
        <td>
             <%= author_name %>
        </td>
    </tr>
</script>

// Add issue form template
<script type="text/template" id="issue_add">
  <form class="form-horizontal" id="add_issue_form">
        <label>Title</label>
        <input name="title" type="text" class="form-control inp">
        <label>Description</label>
        <textarea class="form-control inp" name="description" rows="3"></textarea>
        <label>Labels</label>
        <select name="labels" class="form-control">
            
        </select>
        <label>Assignee</label>
        <select name="assignee" class="form-control">

        </select>
        <input type="hidden" name="author" value="<%= user %>">
        <input type="hidden" name="unit_lesson">
        <input type="hidden" name="is_open" value="true">
        <hr>
        <button class="btn btn-success" id="add_issue_button">Ok</button>
        <button class="btn btn-warning" id="add_issue_cancel_button">Cancel</button>
  </form>
</script>

// Issuet detail view template
<script type="text/template" id="issue_detail">
    <div id="issue_detail">
        <button class="btn btn-info pull-right" id="edit_issue_button">Edit</button>
        <label>Title</label>
        <p><%= title %></p>
        <label>Description</label>
        <p><%= description %></p>
        <label>Labels</label>
        <p><% _.each(labels, function( label ) {%>
            <%= label %><% } ); %></p>
        <label>Author</label>
        <p><%= author %></p>
        <label>Assignee</label>
        <p><%= assignee %></p>
        <button class="btn btn-warning" id="issue_detail_cancel_button">Go back</button>
        <button class="btn pull-right" id="close_issue_button">Close issue</button>
    </div>
</script>