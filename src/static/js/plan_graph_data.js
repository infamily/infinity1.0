// Graph data

function get_graph_data(json) {

  $.ajax({
      url : "/ajax/steps-graph-data/",
      type : "POST",
      data : json,
      success : function(json) {
          redraw(json);
          console.log(json);
      },
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText);
      }
  });
}
