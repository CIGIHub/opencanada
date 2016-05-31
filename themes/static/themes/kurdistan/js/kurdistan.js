jQuery(document).ready(function() {
    
    var windowWidth = $(window).width();
    var featureHeight = 0.666*windowWidth;
    var bannerHeight = $("header .banner").outerHeight();
    
    $(window).on('load resize', function() {
        windowWidth = $(window).width();
        featureHeight = 0.666*windowWidth;
        bannerHeight = $("header .banner").outerHeight();
        $('.main-feature').css({
          "width": windowWidth,
            "height": featureHeight
        });
    
        // $('.container-full-bleed').height(featureHeight);
        // $("main").css({"margin-top": -bannerHeight,
        //                 "padding-top": "0px"
        // });
    
    
    });

});

