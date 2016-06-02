jQuery(document).ready(function() {
    
    var windowWidth = $(window).width();
    var featureHeight = 0.666*windowWidth;
    var bannerHeight = $("header .banner").outerHeight();
    var featureImage = $(".main-feature");
    
    $(window).on('load resize', function() {
        windowWidth = $(window).width();
        featureHeight = 0.666*windowWidth;
        bannerHeight = $("header .banner").outerHeight();
        $('.main-feature').css({
            "width": windowWidth,
            "height": featureHeight
        });

        setTimeout(clouds, 1000);
    
    });

    function clouds(){

        $(".right-cloud").addClass('in-view');
        $(".left-cloud").addClass('in-view');

    }

});

