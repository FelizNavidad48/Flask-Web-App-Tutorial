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

function redaguoti(ataskaitosId) {
  if (document.getElementById("darbId-" + ataskaitosId).disabled) {

    // pakeicia isvaizda ir leidzia redaguoti
    document.getElementById("darbId-" + ataskaitosId).style.border = "solid"
    document.getElementById("valandos-" + ataskaitosId).style.border = "solid"
    document.getElementById("dezes-" + ataskaitosId).style.border = "solid"
    document.getElementById("atlygis-" + ataskaitosId).style.border = "solid"
    document.getElementById("data-" + ataskaitosId).style.border = "solid"

    document.getElementById("darbId-" + ataskaitosId).style.borderWidth = "thin"
    document.getElementById("dezes-" + ataskaitosId).style.borderWidth = "thin"
    document.getElementById("valandos-" + ataskaitosId).style.borderWidth = "thin"
    document.getElementById("atlygis-" + ataskaitosId).style.borderWidth = "thin"
    document.getElementById("data-" + ataskaitosId).style.borderWidth = "thin"

    document.getElementById("darbId-" + ataskaitosId).disabled = false
    document.getElementById("dezes-" + ataskaitosId).disabled = false
    document.getElementById("valandos-" + ataskaitosId).disabled = false
    document.getElementById("atlygis-" + ataskaitosId).disabled = false
    document.getElementById("data-" + ataskaitosId).disabled = false

    document.getElementById("redagavimo-mygtukas-" + ataskaitosId).name = "floppy"

  } else {

    // atstato sena isvaizda
    document.getElementById("darbId-" + ataskaitosId).style.border = "none"
    document.getElementById("valandos-" + ataskaitosId).style.border = "none"
    document.getElementById("dezes-" + ataskaitosId).style.border = "none"
    document.getElementById("atlygis-" + ataskaitosId).style.border = "none"
    document.getElementById("data-" + ataskaitosId).style.border = "none"

    document.getElementById("darbId-" + ataskaitosId).disabled = true
    document.getElementById("dezes-" + ataskaitosId).disabled = true
    document.getElementById("valandos-" + ataskaitosId).disabled = true
    document.getElementById("atlygis-" + ataskaitosId).disabled = true
    document.getElementById("data-" + ataskaitosId).disabled = true

    document.getElementById("redagavimo-mygtukas-" + ataskaitosId).name = "pencil-square"

    // issiuncia informacija i duomenu baze
    fetch("/redaguoti", {
      method: "POST",
      body: JSON.stringify({
        ataskaitosId: ataskaitosId,
        darbuotojoId: document.getElementById("darbId-" + ataskaitosId).value,
        dezes: document.getElementById("dezes-" + ataskaitosId).value,
        valandos: document.getElementById("valandos-" + ataskaitosId).value,
        atlygis: document.getElementById("atlygis-" + ataskaitosId).value,
        data: document.getElementById("data-" + ataskaitosId).value,
      }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
}

function idFiltravimoFunkcija() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("idInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.getElementsByTagName("input")[0].value;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function menesiuFiltravimoFunkcija() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("monthInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.getElementsByTagName("input")[0].value;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function parsisiusti(ataskaitosId) {
  fetch("/parsisiusti-pdf", {
    method: "POST",
    body: JSON.stringify({ ataskaitosId: ataskaitosId }),
  })
}
