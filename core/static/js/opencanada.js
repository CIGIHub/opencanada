var fullScreen = 992;

jQuery(document).ready(function($) {

    var windowHeight = $(window).height();
    var windowWidth = $(window).width();

    initForWindow( windowHeight, windowWidth);

    $('.fa-camera').click(function () {
        $('.feature-text').fadeToggle();
        $('.feature-image-overlay').fadeToggle();
    });

    //scroll down arrow
    $('a[href*=#]:not([href=#])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            var bannerHeight = $('header').height();
            var scrollDestination = target.offset().top - bannerHeight;
            if (target.length) {
                $('html,body').animate({
                    scrollTop: scrollDestination
                }, 1000);
                return false;
            }
        }
    });

    //slide out menu
    if(windowWidth < fullScreen){
         $('html').on('touchstart click', function (e) {
            toggleMenu(e);
        });
    }
    else{
        $('html').off('touchstart click');
    }



});

//initialize window based on width and height
function initForWindow(windowHeight, windowWidth){

    setBodyPadding(windowWidth);

    if($('body').hasClass('template-home-page')){
        setFeatureHeight(windowHeight);
    }

    toggleHeading(windowWidth);

}

//toggle menu in mobile/small window width view
function toggleMenu(e){
    var selected = $(e.target);
    var menu = $('#main-menu');

    if(selected.parent().data("target") == '#main-menu' ){
        if(!(menu.is(':visible'))){
            menu.show().css("left", "-400px").animate({"left":"0px"}).addClass('mobile-menu open');
        }
    }
    else{
        menu.animate({"left":"-400px"}, function() {
            $(menu).hide().css("left", "").removeClass('open');
        });
    }
}

//set the Homepage Feature height based on window height
function setFeatureHeight(windowHeight){
    var bannerHeight = $('header').height();
    var featureHeight = windowHeight - bannerHeight;

    $('.jumbotron.feature').css("height", featureHeight + "px");
}

//set the body padding based on banner height
function setBodyPadding(){
    var bannerHeight = $('header').height();
    $('body').css("padding-top", bannerHeight + "px");
}

//toggle Banner heading based on window width and page type
function toggleHeading(windowWidth){

    var offset = $('header').height();

    function fullHeader(){
        $('header').removeClass('collapsed');
        $('.banner').removeClass('container-fluid').addClass('container');
        $('.logo').addClass('col-md-5').removeClass('col-md-10');
        $('nav').addClass('vcenter').removeClass('mobile-menu open').show();
        $('body').removeClass('article-scroll');
    }

    function collapsedHeader(){
        $('header').addClass('collapsed');
        $('.banner').addClass('container-fluid').removeClass('container');
        $('.logo').removeClass('col-md-5').addClass('col-md-10');
        $('nav').removeClass('vcenter').addClass('mobile-menu');
        if($('nav').hasClass('open')){
            $('nav').show();
        }
        else{
            $('nav').hide();
        }
        if($('#article-page').length){
            $('body').addClass('article-scroll');
        }
    }

    function fullScroll(){
        $('header').toggleClass('collapsed scrolled', $(document).scrollTop() > offset);

        if($('header').hasClass('collapsed')){
            collapsedHeader();
        }
        else{
            fullHeader();
        }
    }

    function collapsedScroll(){
        collapsedHeader();
        $('header').toggleClass('scrolled', $(document).scrollTop() > offset);
    }

    if(windowWidth > fullScreen){
        fullHeader();
        $(window).off("scroll touchmove", collapsedScroll );
        $(window).on("scroll touchmove", fullScroll );
    }
    else{
        collapsedHeader();
        $(window).off("scroll touchmove", fullScroll );
        $(window).on("scroll touchmove", collapsedScroll );

    }
}

$(window).resize(function(){
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();

    initForWindow( windowHeight, windowWidth);

    if(windowWidth < fullScreen){
         $('html').on('touchstart click', function (e) {
            toggleMenu(e);
        });
    }
    else{
        $('html').off('touchstart click');
    }

});


