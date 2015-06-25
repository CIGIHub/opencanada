jQuery(document).ready(function($) {

    $('.article-header').hide();

    $(window).scroll(function () {
        var offset = $('header').height();
        var fromTop = $(window).scrollTop();

        //console.log('offset: ' + offset +  ' from Top: ' + fromTop);

        if (fromTop > offset) {
            $('header').addClass('article-page');
            $('.navbar-collapse').removeClass('navbar-right');
            $('.main-menu').addClass('container-fluid').removeClass('container');
        }
        else{
            $('header').removeClass('article-page');
            $('.navbar-collapse').addClass('navbar-right');
            $('.main-menu').removeClass('container-fluid').addClass('container');
        }
    });


});