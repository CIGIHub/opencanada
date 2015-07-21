var fullScreen = 992;

jQuery(document).ready(function($) {

    initForWindow();

    $('.fa-camera').click(function () {
        $('.feature-text').fadeToggle();
        $('.feature-image-overlay').fadeToggle();
        $('.fa-camera').toggleClass('highlighted');
    });

    //scroll down arrow
    $('a[href*=#]:not([href=#])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            if($(this).attr('href') == '#features'){
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
        }
    });

});

//initialize window based on width and height
function initForWindow(){

    var windowHeight = $(window).height();
    var windowWidth = $(window).width();

    if($('body').hasClass('template-home-page')){
        setFeatureHeight(windowHeight);
    }

    setOverlayForWindow(windowWidth);
    toggleHeading(windowWidth);
    setBodyPadding();

    $('html').on('touchstart click', function (e) {
        toggleBox(e);
    });

}

//toggle menu in mobile/small window width view
function toggleBox(e){
    var selected = $(e.target);
    var target = null;
    var menu = $('#main-menu');
    var search = $('#search-box');

    if(selected.closest('button').attr('class') == 'menu'){
        target = menu;
    }
    else if (selected.closest('li').attr('class') == 'search'){
        target = search;
    }

    if(target != null){
        if(target == menu){
            if(!(menu.hasClass('open'))){
                if(search.hasClass('open')){
                    search.removeClass('open');
                }
                menu.addClass('open');
            }
        }
        if(target == search ){
            if(!(search.hasClass('open'))){
                if(menu.hasClass('open')){
                    menu.removeClass('open');
                }
               search.addClass('open');
            }
            else{
                search.removeClass('open');
            }
        }
    }
    else{

        if((menu.hasClass('open')) && (!(selected.closest('nav').length))){
            menu.removeClass('open');
        }
        if((search.hasClass('open')) && (!(selected.closest("#search-box").length))){
            search.removeClass('open');
        }
    }

}

//set the Homepage Feature height based on window height
function setFeatureHeight(windowHeight){
    var bannerHeight = $('header').height();
    var featureHeight = windowHeight - bannerHeight;

    $('.jumbotron.main-feature').css("height", featureHeight + "px");
}

//set the body padding based on banner height
function setBodyPadding(){
    var bannerHeight = $('header').height();
    $('body').css("padding-top", bannerHeight + "px");
    $('#search-box').css("top", bannerHeight = "px");

}

function setOverlayForWindow(windowWidth){
    if(windowWidth < fullScreen){
        var overlayFeatures = $('#features').find('.rowheight-2');
        overlayFeatures.each(function(index){
            overlayHeight = $(this).css("height");
            overlayHeight = parseInt(overlayHeight.slice(0, -2));
            $(this).css("height", "280px");
        });
    }
    if(windowWidth > fullScreen){
        var overlayFeatures = $('#features').find('.rowheight-2');
        overlayFeatures.each(function(index){
            if($(this).css("height") == '280px'){
                $(this).css("height", "560px");
            }

        });
    }
}

//toggle Banner heading based on window width and page type∂
function toggleHeading(windowWidth){

    var offset = $('header').height();

    function fullHeader(){
        $('header').removeClass('collapsed');
        $('.banner').removeClass('container-fluid').addClass('container');
        $('.logo').addClass('col-md-5').removeClass('col-md-8');
        $('nav').addClass('vcenter').removeClass('mobile-menu open');
        $('body').removeClass('article-scroll');
    }

    function collapsedHeader(){
        $('header').addClass('collapsed');
        $('.banner').addClass('container-fluid').removeClass('container');
        $('.logo').removeClass('col-md-5').addClass('col-md-8');
        $('nav').removeClass('vcenter').addClass('mobile-menu');

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

    initForWindow();


});


