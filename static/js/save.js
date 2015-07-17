function save() {
  var editor = ace.edit("editor");

  $.ajax("/slides", {type: 'put', data: editor.getValue()});

  $('#slides-frame')[0].contentWindow.postMessage(JSON.stringify({
    method: 'reloadMarkdown'
  }), window.location.origin);
}
