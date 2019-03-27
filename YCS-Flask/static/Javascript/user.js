function validate(fieldId, btnId) {
    var x = document.getElementById(fieldId);
    x.disabled = !x.disabled;
    var btn = document.getElementById(btnId);
    if (btn.value == "Edit")
        btn.value = "Save";
    else if (btn.value == "Save")
        btn.value = "Edit";
}