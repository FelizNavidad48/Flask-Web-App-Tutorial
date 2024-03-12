function deleteNote(noteId) {
  print("hello");
}

function patvirtintiAtaskaita(ataskaitosId) {
  fetch("/patvirtintiAtaskaita", {
    method: "POST",
    body: JSON.stringify({ ataskaitosId: ataskaitosId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function patvirtintiVartotoja(vartotojoId) {
  fetch("/patvirtintiVartotoja", {
    method: "POST",
    body: JSON.stringify({ vartotojoId: vartotojoId }),
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

function filtravimoFunkcija() {
  // Declare variables
  let monthInput, idInput, filter, table, tr, td, i, txtValue;
  monthInput = document.getElementById("monthInput");
  idInput = document.getElementById("idInput");
  let monthFilter = monthInput.value.toUpperCase();
  let idFilter = idInput.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  let tdId;
  let tdMonth;
  let txtValueId;
  let txtValueMonth;
  for (i = 0; i < tr.length; i++) {
    tdMonth = tr[i].getElementsByTagName("td")[1];
    tdId = tr[i].getElementsByTagName("td")[0];
    if (tdMonth || tdId) {
      txtValueMonth = tdMonth.getElementsByTagName("input")[0].value;
      txtValueId = tdId.getElementsByTagName("input")[0].value;
      if (monthFilter !== "" && idFilter !== "") {
        if (txtValueMonth.toUpperCase().indexOf(monthFilter) > -1 && txtValueId.toUpperCase().indexOf(idFilter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      } else if(monthFilter !== "" && idFilter === "") {
        if (txtValueMonth.toUpperCase().indexOf(monthFilter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      } else if(monthFilter === "" && idFilter !== "") {
        if(txtValueId.toUpperCase().indexOf(idFilter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}

function parsisiustiMenesioAtaskaita() {
  let menuo = document.getElementById("monthInput");
  if (menuo == null || menuo.value === "") {
    alert("Pasirinkite menesį");
    return;
  }
  let darbuotojoId = document.getElementById("idInput");
  fetch(`/parsisiusti-pdf/${menuo.value.toString()}/${darbuotojoId.value.toString()}`, {
    method: "POST",
    body: JSON.stringify({ menuo: menuo.value }),
  }).then(async (_res) => {
    window.location.href = `/parsisiusti-pdf/${menuo.value.toString()}/${darbuotojoId.value.toString()}`;
  });
}
