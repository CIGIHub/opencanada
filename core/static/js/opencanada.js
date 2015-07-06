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
          if (target.length) {
            $('html,body').animate({
              scrollTop: target.offset().top
            }, 1000);
            return false;
          }
        }
    });

    //drop cap on articles

    $('.story p').first().html(function (index, html) {
        return '<span class="dropcap">' + html.slice(0, 1) + '</span>' + html.slice(1);
    });

});

function initForWindow(){
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();

    setBodyPadding();

    if($('body').hasClass('template-home-page')){
        setFeatureHeight(windowHeight, windowWidth);
    }
    if($('#article-page').length){
        setArticleHeading(windowWidth);
    }
}

function setFeatureHeight(windowHeight, windowWidth){

    var bannerHeight = $('header').height();
    var tagsHeight = $('.featured-topics').height();
    var featureHeight = windowHeight - bannerHeight - tagsHeight;

    if(windowWidth > 768){
        var featureHeight = windowHeight - bannerHeight - tagsHeight;
    }
    else{
        var featureHeight = windowHeight - bannerHeight;
    }
    $('.jumbotron.feature').css("height", featureHeight + "px");
}

function setBodyPadding(){
    var bannerHeight = $('header').height();
    $('body').css("padding-top", bannerHeight + "px");

}

function setArticleHeading(windowWidth){

    function disableArticleHeader(){
        $('h1').css("width", "");
        $('body').removeClass('article-scroll');
        $('.navbar-collapse').addClass('navbar-right');
        $('.main-menu').removeClass('container-fluid').addClass('container');
    }

    if(windowWidth > 768){
        console.log('here');

        var offset = $('header').height();

        $(window).scroll(function () {
            var titleWidth = $('.title').width();
            $('h1').css("width", titleWidth + "px");

            var fromTop = $(window).scrollTop();

            if (fromTop > offset) {
                $('body').addClass('article-scroll');
                $('.navbar-collapse').removeClass('navbar-right');
                $('.main-menu').addClass('container-fluid').removeClass('container');
            }
            else {
                disableArticleHeader()
            }

        });
    }
    else{
        disableArticleHeader()
         $(window).scroll(function () {
             disableArticleHeader()
         });
    }
}

$(window).resize(function(){

    initForWindow()

});


