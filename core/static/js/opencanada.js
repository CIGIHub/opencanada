var breakpoint = 1000;


jQuery(document).ready(function($) {

    initForWindow();

    $('.camera').hover(function () {
        var target = null;
        var selected = $(this);

        selected.toggleClass('highlighted');
        target = selected.closest($('.overlay'));

        target.find($('.feature-text')).fadeToggle();
        target.find($('.feature-image-overlay')).fadeToggle();

    });

    $('.template-article-page .fa-camera').hover(function(){
        $('.feature-text').fadeToggle();
        $('.feature-image-overlay').fadeToggle();
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

    $('.search-form input[type=text]').keydown(function() {
        if($(this).val() != ''){
            $('.clear-button').show();
        }
    });
    $('.clear-button').click(function(){
        $('.search-form input[type=text]').val('');
        $('.clear-button').hide();
        $('#search-box input').focus();
    });

    if ($(".facebook-share-link").length > 0){
        social_setup();
    }


});

//initialize window based on width and height
function initForWindow(){

    var windowHeight = $(window).height();
    var windowWidth = $(window).width();
    var articleTitleWidth = $('article').width() - 0.2*($('article').width());

    if(($('body').hasClass('template-home-page')) || ($('body').hasClass('template-article-page') && $('.jumbotron').length)){
        setFeatureHeight(windowHeight);
    }
    if($('.template-article-page').length && $('.jumbotron').length) {
        if(windowWidth > breakpoint) {
            var height = $('.jumbotron').height() + 100;
            $('ul.share-links').css('top', height + 'px');
        }
        else{
            $('ul.share-links').css('top', '10px');
        }
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

    function fullHeader(){
        $('header').removeClass('collapsed');
        $('#search-box').removeClass('small-header');
        $('.toggle-mobile').hide();
        $('nav').removeClass('mobile-menu open');
        $('body').removeClass('article-scroll');

        if($('.template-home-page').length){
            $('.tagline').show();
        }
    }

    function collapsedHeader(){

        $('header').addClass('collapsed');
        $('#search-box').addClass('small-header');
        $('.toggle-mobile').show();

        $('nav').addClass('mobile-menu');
        if($('#article-page').length  && $('body').hasClass('article-scroll')  && windowWidth <= breakpoint){
            $('body').removeClass('article-scroll');
        }
        if($('.template-home-page').length){
            $('.tagline').hide();
        }
    }

    function fullScroll(){
        $('header').toggleClass('collapsed scrolled', $(document).scrollTop() > offset);

        if($('header').hasClass('collapsed')){
            $('#main-menu').hide();
            collapsedHeader();

            if($('#article-page').length ){
                $('body').addClass('article-scroll');
                $('header .header-row').removeClass('col-md-4');
            }
        }
        else{
            $('#main-menu').show();
            if(!($('header .header-row').hasClass('col-md-4'))){
                $('header .header-row').addClass('col-md-4');
            }
            fullHeader();

        }
    }

    function collapsedScroll(){
        collapsedHeader();
        $('header').toggleClass('scrolled', $(document).scrollTop() > offset);
    }

    if(windowWidth >= breakpoint){
        
        if($('body').hasClass('small-article')){
            $('body').removeClass('small-article');
        }

        if($(document).scrollTop() > offset){
           if($('#article-page').length){
                $('body').addClass('article-scroll');
            }
            collapsedHeader();
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


function social_setup(){
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '1209700165722055',
      xfbml      : true,
      version    : 'v2.4'
    });
  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

  $(".facebook-share-link").click(function(){
    var href = $(this).data('url');
    FB.ui(
      {
      method: 'share',
      href: href
    }, function(response){});
    });
}
