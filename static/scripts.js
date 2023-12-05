function addRow(items) {
    let newRow = document.getElementById("item-table").insertRow();
    for (let i = 0; i < items.names.length; i++) {
        newRow.insertCell().innerHTML = `<input type="text" name="${items.names[i]}" data-demo="${items.demos[i]}">`;
    }
    newRow.insertCell().innerHTML = '<button type="button" onclick="deleteRow(this)">Delete</button>';
}

function deleteRow(btn) {
    btn.parentNode.parentNode.remove();
}

function deleteAllRows() {
    let rows = Array.from(document.getElementById("item-table").children)
    for (let i = 0; i < rows.length; i++) {
        rows[i].remove();
    }
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
    document.getElementById("item-data").value = JSON.stringify(formData);
    document.getElementById("invoice-form").submit();
}

function demoForm(items) {
    clearForm();
    addRow(items);
    for (const element of document.querySelectorAll('[data-demo]')) {
        element.value = element.dataset.demo;
    }
}

function clearForm() {
    for (const element of document.querySelectorAll('[data-demo]')) {
        element.value = "";
    }
    deleteAllRows();
}
