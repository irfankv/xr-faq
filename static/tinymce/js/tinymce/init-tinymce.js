tinymce.init({
    selector: "textarea.tinymce",
    plugins : "lists pagebreak table searchreplace preview textcolor paste fullpage textcolor colorpicker contextmenu paste directionality noneditable visualchars nonbreaking insertdatetime searchreplace paste textcolor fullpage  textcolor colorpicker",
    toolbar: "undo redo | styleselect | save | table | bold italic | link | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent |  print preview fullpage | forecolor backcolor emoticons charmap code | hr paste pagebreak searchreplace spellchecker template insertdatetime",
    contextmenu: "paste | link image inserttable | cell row column deletetable",
    branding: false,

    setup: function (editor) {
      editor.on('change', function () {
          tinymce.triggerSave();
      });
  }
});