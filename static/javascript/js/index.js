/**
 * Created by PC on 2017/7/14.
 */
$(function(){
$('.metismenu a').each(function (n, v) {
        var url = $(v).attr("menu-url");
        if (url) {
            $(v).unbind("click").click(function (e) {

                $("#content-main").load(url);
                // $('.nav-list .active').each(function (nn, vv) {
                //     $(vv).removeClass("active");
                //
                // });
                // $(this).parents("li").each(function (nn, vv) {
                //     $(vv).addClass("active");
                // });
            });
        }
    });

})