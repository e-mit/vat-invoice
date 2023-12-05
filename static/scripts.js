function addRow(items) {
    let newRow = document.getElementById("item-table").insertRow();
    for (const key in items) {
        newRow.insertCell().innerHTML = `<input type="text" name="${key}">`;
    }
    newRow.insertCell().innerHTML = '<button type="button" onclick="deleteRow(this)">Delete</button>';
}

function deleteRow(btn) {
    let row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

function submitForm() {
    const table = document.getElementById("item-table");
    let formData = [];
    for (let i = 0; i < table.rows.length; i++) {
        const row = table.rows[i];
        let rowData = {};
        for (let j = 0; j < (row.cells.length - 1); j++) {
            const k = row.cells[j].getElementsByTagName("input")[0].name;
            rowData[k] = row.cells[j].getElementsByTagName("input")[0].value;
        }
        formData.push(rowData);
    }

    const jsonData = JSON.stringify(formData);
    console.log(jsonData);
    document.getElementById("json-data").value = jsonData;

    const form = document.getElementById("invoice-form")
    form.submit();
  }

  function demoForm(demoData) {
    console.log(demoData);
    clearForm();
  }

  function clearForm() {
  }