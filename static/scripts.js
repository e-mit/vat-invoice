function addRow(items) {
    var newRow = document.getElementById("item-table").insertRow();
    for (const key in items) {
        newRow.insertCell().innerHTML = `<input type="text" name="${key}">`;
    }
    newRow.insertCell().innerHTML = '<button type="button" onclick="deleteRow(this)">Delete</button>';
}

function deleteRow(btn) {
    var row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

function submitForm() {
    var table = document.getElementById("item-table");
    var formData = [];
    for (var i = 0; i < table.rows.length; i++) {
        var row = table.rows[i];
        var rowData = {};
        for (var j = 0; j < (row.cells.length - 1); j++) {
            var k = row.cells[j].getElementsByTagName("input")[0].name;
            console.log(k);
            rowData[k] = row.cells[j].getElementsByTagName("input")[0].value;
        }
        formData.push(rowData);
    }

    /*
    console.log(Array.from(document.getElementById("item-table").rows));
    for (const row in Array.from(document.getElementById("item-table").rows)) {
      console.log(row);
      var rowData = {};
      for (const cell in Array.from(row.cells)) {
        console.log(cell);
        k = cell.getElementsByTagName("input")[0].name;
        rowData[k] = cell.getElementsByTagName("input")[0].value;
        console.log(k);
        console.log(rowData);
      }
      formData.push(rowData);
    }
    */

    var jsonData = JSON.stringify(formData);
    console.log(jsonData);
    document.getElementById("json-data").value = jsonData;

    var form = document.getElementById("invoice-form")
    form.submit();
  }

  function demoForm(demoData) {
    console.log(demoData);
    clearForm();
  }

  function clearForm() {
  }