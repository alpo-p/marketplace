function checkLengthSearch(form) {
    if (form.search.value.length > 100) {
        alert("Liian pitkä hakusana!");
        return false;
    }
    return true;
}