var breakpoint = 753;

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
    var articleTitleWidth = $('article').width() - 0.2*($('article').width());

    if($('body').hasClass('template-home-page')){
        setFeatureHeight(windowHeight);
    }

    setOverlayForWindow(windowWidth);
    toggleHeading(windowWidth, articleTitleWidth);
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

    if(selected.closest('button').data('target') == 'main-menu'){
        target = menu;
    }
    else if (selected.closest('button').data('target') == 'search-box') {
        target = search;
    }

    if(target != null){
        if(target == menu){
            if(!(menu.hasClass('open'))){
                if(search.hasClass('open')){
                    search.removeClass('open');
                }

                menu.show( function() {
                    menu.addClass('open');
                });

            }
        }
        if(target == search ){
            if(!(search.hasClass('open'))){
                if(menu.hasClass('open')){
                    menu.removeClass('open');
                }
               search.addClass('open');
                $('#search-box input').focus();
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
    var gap = 0.05*windowHeight;
    console.log(gap);
    var featureHeight = windowHeight - bannerHeight - gap;

    $('.jumbotron.main-feature').css("height", featureHeight + "px");
}

//set the body padding based on banner height
function setBodyPadding(){
    var bannerHeight = $('header').height();
    $('body').css("padding-top", bannerHeight + "px");
    $('#search-box').css("top", bannerHeight = "px");

}

function setOverlayForWindow(windowWidth){
    if(windowWidth <= breakpoint){
        var overlayFeatures = $('#features').find('.rowheight-2');
        overlayFeatures.each(function(index){
            overlayHeight = $(this).css("height");
            overlayHeight = parseInt(overlayHeight.slice(0, -2));
            $(this).css("height", "280px");
        });
    }
    if(windowWidth > breakpoint){
        var overlayFeatures = $('#features').find('.rowheight-2');
        overlayFeatures.each(function(index){
            if($(this).css("height") == '280px'){
                $(this).css("height", "560px");
            }

        });
    }
}

//toggle Banner heading based on window width and page type∂
function toggleHeading(windowWidth, articleTitleWidth){

    var offset = $('header').height();
    console.log(offset);

    function fullHeader(){
        $('header').removeClass('collapsed');
        $('#search-box').removeClass('small-header');
        $('.toggle-mobile').hide();
        $('.toggle-full').show();
        $('.logo').addClass('col-sm-12');
        $('nav').removeClass('mobile-menu open');
        $('body').removeClass('article-scroll');
    }

    function collapsedHeader(){
        $('header').addClass('collapsed');
        $('#search-box').addClass('small-header');
        $('.toggle-mobile').show();
        $('.toggle-full').hide();
        $('.logo').removeClass('col-sm-12');
        $('nav').addClass('mobile-menu');
        if($('#article-page').length  && $('body').hasClass('article-scroll')  && windowWidth <= breakpoint){
            $('body').removeClass('article-scroll');
        }
    }

    function fullScroll(){
        $('header').toggleClass('collapsed scrolled', $(document).scrollTop() > offset);

        if($('header').hasClass('collapsed')){

            $('#main-menu').hide();
            collapsedHeader();
            if($('#article-page').length){
                $('body').addClass('article-scroll');
                $('h1').css('width', articleTitleWidth);

            }
            if($('#article-page').length ){
                var sharelinksPosition = $('.share-links').offset().top - $('.share-links').height();
                var fromBottom = $('footer').outerHeight() + $('.related-articles').outerHeight() + $('.share-links').outerHeight() + 195;
                var bottom = $(document).height() - fromBottom;

                if($(document).scrollTop() > sharelinksPosition){
                    $('.share-links').addClass('sticky');
                }
                if($(document).scrollTop() > bottom){
                    $('.share-links').removeClass('sticky').css('bottom', fromBottom);
                }
                else{
                    $('.share-links').css('bottom', '');
                }
            }

        }
        else{
            $('#main-menu').show();
            $('h1').css('width', '');
            fullHeader();
        }
    }

    function collapsedScroll(){
        collapsedHeader();
        $('header').toggleClass('scrolled', $(document).scrollTop() > offset);
    }

    if(windowWidth >= breakpoint){

        if($('#article-page').length && $('body').hasClass('small-article')){
            $('body').removeClass('small-article');
        }
        if($(document).scrollTop() > offset && $('#article-page').length){
            $('body').addClass('article-scroll');
        }

        else{
            fullHeader();
        }

        $(window).off("scroll touchmove", collapsedScroll );
        $(window).on("scroll touchmove", fullScroll );
    }
    else{

        if($('#article-page').length && $('body').hasClass('article-scroll')){
            $('body').removeClass('article-scroll');
        }
        if($('#article-page').length){
            $('body').addClass('small-article');
        }
        collapsedHeader();
        $(window).off("scroll touchmove", fullScroll );
        $(window).on("scroll touchmove", collapsedScroll );

    }
}

$(window).resize(function(){
    initForWindow();

});


