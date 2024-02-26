function addRow() {
    try {
        const lastRow = Array.from(document.getElementById("item-table").getElementsByTagName("tr")).pop();
        const lastRowCells = lastRow.getElementsByTagName("td");
        let newRow = document.getElementById("item-table").insertRow();
        for (let i = 0; i < lastRowCells.length; i++) {
            newRow.insertCell().appendChild(createNewInput(lastRowCells[i].children[0]));
        }
    }
    catch (e) {
        formError(e.message);
    }
}

function createNewInput(oldInput) {
    let newInput = oldInput.cloneNode();
    // Expect id to have the WTF format 'a-N-b'
    const idParts = newInput.id.split('-');
    if (idParts.length != 3) {
        throw new Error("Invalid input id format");
    }
    const newNumber = Number(idParts[1]) + 1
    if (isNaN(newNumber)) {
        throw new Error("Input id NaN");
    }
    newInput.id = `${idParts[0]}-${newNumber}-${idParts[2]}`
    newInput.name = newInput.id;
    newInput.value = ""
    return newInput;
}

function formError(errorDescription = '') {
    let submitters = document.querySelectorAll('input[type=submit][form=invoice-form]');
    for (let submitter of submitters.values()) {
        submitter.disabled = true;
    }
    document.getElementById("error-message").innerHTML = "An error has occurred";
    if (errorDescription) {
        document.getElementById("error-message").innerHTML += `: ${errorDescription}`;
    }
}

function countRows() {
    let tableRows = document.getElementById("item-table").getElementsByTagName("tr");
    return tableRows.length;
}

function removeRow() {
    if (countRows() > 1) {
        let tableRows = Array.from(document.getElementById("item-table").getElementsByTagName("tr"));
        tableRows.pop().remove();
    }
}

function removeAllAddedRows() {
    while (countRows() > 1) {
        removeRow();
    }
}

function clearForm() {
    clearErrors();
    let elements = Array.from(document.getElementById("invoice-form").getElementsByClassName("clearable"));
    for (let i = 0; i < elements.length; i++) {
        elements[i].value = "";
    }
    removeAllAddedRows();
}

function clearErrors() {
    let elements = Array.from(document.getElementsByClassName("error-string"));
    for (let i = 0; i < elements.length; i++) {
        elements[i].remove()
    }
    let cells = Array.from(document.getElementsByClassName("error-cell"));
    for (let i = 0; i < cells.length; i++) {
        cells[i].classList.remove("error-cell");
    }
}

function submitForm() {
    clearErrors();
    let form = document.getElementById("invoice-form")
    if (form.checkValidity()) {
        form.submit();
    }
    else {
        document.getElementById("form-submit").click();
    }
}
