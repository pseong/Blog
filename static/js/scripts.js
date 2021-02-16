
function search_title() {
    var searchtxt = document.getElementById("search").value;
    location.assign("/search/"+searchtxt);
}

function enter_search() {
    if (window.event.keyCode == 13) {
        search_title();
    }
}

function cardClick(post) {
    alert('dd');
}

(function($) {
    "use strict";

    var path = window.location.href;
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
        if($("#dark").is(".dark")) {
            $("p.dark").off()
        }
        $("#dark").toggleClass("dark");
        $("p.dark").on("click", function(e) {
            e.preventDefault();
            $("body").toggleClass("sb-sidenav-toggled");
            $("p.dark").off()
            $("#dark").toggleClass("dark");
        });
    });
})(jQuery);