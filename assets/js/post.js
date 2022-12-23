window.addEventListener("scroll", handleScroll);

function handleScroll() {
    // hide button
    var scollTop =
        document.documentElement.scrollTop || document.body.scrollTop;
    var clientHeight = document.documentElement.clientHeight;

    if (scollTop >= clientHeight) {
        document.querySelector("#ikaros").style.display = "block";
    } else {
        document.querySelector("#ikaros").style.display = "none";
    }
}
function smoothscroll() {
    // back top
    var currentScrollTop =
        document.documentElement.scrollTop || document.body.scrollTop;

    if (currentScrollTop > 0) {
        window.requestAnimationFrame(smoothscroll);
        window.scrollTo(0, currentScrollTop - currentScrollTop / 10);
    }
}