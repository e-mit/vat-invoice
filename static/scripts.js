function addRow(items) {
    let newRow = document.getElementById("item-table").insertRow();
    for (const key in items) {
        newRow.insertCell().innerHTML = `<input type="text" name="${key}">`;
    }
    newRow.insertCell().innerHTML = '<button type="button" onclick="deleteRow(this)">Delete</button>';
}

function deleteRow(btn) {
    btn.parentNode.parentNode.remove();
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
    document.getElementById("item-data").value = jsonData;
    document.getElementById("invoice-form").submit();
  }

  function demoForm() {
    clearForm();
    for (const element of document.querySelectorAll('[data-demo]')) {
        element.value = element.dataset.demo;
    }
    // TODO: add item data
  }

  function clearForm() {
    for (const element of document.querySelectorAll('[data-demo]')) {
        element.value = "";
    }
  }