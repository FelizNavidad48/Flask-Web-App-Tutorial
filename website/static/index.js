function deleteNote(noteId) {
  print("hello");
}

function patvirtinti(ataskaitosId) {
  fetch("/patvirtinti", {
    method: "POST",
    body: JSON.stringify({ ataskaitosId: ataskaitosId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}