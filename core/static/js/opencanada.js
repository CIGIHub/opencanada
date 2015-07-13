jQuery(document).ready(function($){

    initForWindow();

    $('.fa-camera').click(function(){
        $('.feature-text').fadeToggle();
        $('.feature-image-overlay').fadeToggle();
    });

    //scroll down arrow
    $('a[href*=#]:not([href=#])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
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

    //drop cap on articles
    $('.story p').first().html(function (index, html) {
        return '<span class="dropcap">' + html.slice(0, 1) + '</span>' + html.slice(1);
    });

    $( ".toggle-nav button" ).click(function() {
        var menu = $('#main-menu');

        if(menu.is(':visible')){

            menu.animate({"left":"-400px"}, "slow", function(){
                menu.removeClass('mobile-menu');
            });

        }
        else{
            menu.css("left", "-400px").animate({"left":"0px"}).addClass('mobile-menu');
        }
    });

});

function initForWindow(){
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();

    setBodyPadding(windowWidth);
    if($('body').hasClass('template-home-page')){
        setFeatureHeight(windowHeight, windowWidth);
    }

    toggleHeading(windowWidth);

}

function setFeatureHeight(windowHeight, windowWidth){

    var bannerHeight = $('header').height();
    var featureHeight = windowHeight - bannerHeight;

    $('.jumbotron.feature').css("height", featureHeight + "px");
}

function setBodyPadding(windowWidth){

    var bannerHeight = $('header').height();
    $('body').css("padding-top", bannerHeight + "px");

}

function toggleHeading(windowWidth){

    var offset = $('header').height();

    if(windowWidth > 992){
        //reset to full header for full page display
        $('header').removeClass('collapsed');
        $('.banner').removeClass('container-fluid').addClass('container');
        $('.logo').addClass('col-md-5').removeClass('col-md-10');
        $('body').removeClass('article-scroll');
        $('nav').addClass('col-md-6 vcenter').css("left", "");

        //check for scrolling and toggle header
        $(window).on("scroll touchmove", function () {
            $('header').toggleClass('collapsed', $(document).scrollTop() > offset);

            if($('header').hasClass('collapsed')){
                $('header').addClass('scrolled');
                $('.banner').addClass('container-fluid').removeClass('container');
                $('.logo').removeClass('col-md-5').addClass('col-md-10');
                if($('#article-page').length){
                    $('body').addClass('article-scroll');
                }
            }
            else{
                $('header').removeClass('scrolled');
                $('.banner').removeClass('container-fluid').addClass('container');
                $('.logo').addClass('col-md-5').removeClass('col-md-10');
                $('body').removeClass('article-scroll');
            }
        });
    }
    else{

        if(!($('header').hasClass('collapsed'))){
            $('header').addClass('collapsed');
            $('.banner').addClass('container-fluid').removeClass('container');
            $('.logo').removeClass('col-md-5').addClass('col-xs-8');
            $('nav').removeClass('col-md-6 vcenter');
        }

        $(window).on("scroll touchmove", function () {
             $('header').toggleClass('scrolled', $(document).scrollTop() > offset);


        });

    }
}

$(window).resize(function(){

    initForWindow()

});


