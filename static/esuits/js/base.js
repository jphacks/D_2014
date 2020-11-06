function autoPadding() {
    var navHeader = document.getElementById("header-nav");
    $('body').css('margin-top', $(navHeader).outerHeight());
}