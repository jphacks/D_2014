function getToday() {
    var today = new Date();
    today.setDate(today.getDate());
    var yyyy = today.getFullYear();
    var mm = ("0" + (today.getMonth() + 1)).slice(-2);
    var dd = ("0" + today.getDate()).slice(-2);
    document.getElementById("deadline_date").value = yyyy + '-' + mm + '-' + dd;
}

function addClassToSelect() {
    // 質問の最後のform-groupをとるために，質問リストを取得
    var parent = document.getElementById('question_list');
    var lastChild = parent.lastElementChild;

    // 最後の質問からtagのリストを取得
    var select = lastChild.lastElementChild.lastElementChild;
    select.setAttribute('class', 'selectpicker form-control');
    select.setAttribute('data-selected-text-format', 'count > 3');
    select.setAttribute('data-style', 'btn-dark');
}