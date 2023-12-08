function addRow() {
    const lastRow = Array.from(document.getElementById("item_table").getElementsByTagName("tr")).pop();
    const cells = lastRow.getElementsByTagName("td");
    let newRow = document.getElementById("item_table").insertRow();
    for (let i = 0; i < cells.length; i++) {
        let newInput = cells[i].children[0].cloneNode();
        const idParts = newInput.id.split('-');
        if (idParts.length != 3) {
            console.log("ERROR");
        }
        newInput.value = ""
        newInput.id = `${idParts[0]}-${Number(idParts[1])+1}-${idParts[2]}`
        newInput.name = newInput.id;
        newRow.insertCell().appendChild(newInput);
    }
}

function countRows() {
    let tableRows = document.getElementById("item_table").getElementsByTagName("tr");
    return tableRows.length;
}

function removeRow() {
    if (countRows() > 1) {
        let tableRows = Array.from(document.getElementById("item_table").getElementsByTagName("tr"));
        tableRows.pop().remove();
    }
}

function removeAllAddedRows() {
    while (countRows() > 1) {
        removeRow();
    }
}

function clearForm() {
    let elements = Array.from(document.getElementById("invoice_form").getElementsByClassName("clearable"));
    for (let i = 0; i < elements.length; i++) {
        elements[i].value = "";
    }
    removeAllAddedRows();
}
