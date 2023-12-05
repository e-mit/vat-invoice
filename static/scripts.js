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

      /*
      rowData = {};
      for (const cell in row.cells) {
        k = cell.getElementsByTagName("input")[0].name;
        rowData[k] = cell.getElementsByTagName("input")[0].value;
      }
      formData.push(rowData);
      */

      formData.push({
        description: row.cells[0].getElementsByTagName("input")[0].value,
        price: row.cells[1].getElementsByTagName("input")[0].value,
        rate: row.cells[2].getElementsByTagName("input")[0].value,
        quantity: row.cells[3].getElementsByTagName("input")[0].value
      });
      
    }

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