jQuery(document).ready(function($){

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

function setFeatureHeight(){
    var windowHeight = $(window).height();
    var bannerHeight = $('header').height();
    var tagsHeight = $('.featured-topics').height();
    var featureHeight = windowHeight - bannerHeight - tagsHeight;

    $('.jumbotron .feature-image').css("height", featureHeight + "px");
}

$(window).resize(function(){
    setFeatureHeight();
});

$(window).load(function(){
    setFeatureHeight();
});

