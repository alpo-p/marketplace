function checkLengthSearch(form) {
    if (form.search.value.length > 50) {
        alert("Liian pitkä hakusana!");
        return false;
    }
    return true;
}