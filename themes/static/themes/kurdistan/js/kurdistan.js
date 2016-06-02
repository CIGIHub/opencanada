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
        setTimeout(header, 2000);
        setTimeout(text, 3000);
    
    });

    function clouds(){
        $(".right-cloud, .left-cloud").addClass('in-view');
    }
    function header(){
        $("h1").addClass('in-view');
    }
    function text(){
        $(".contributors, ul.share-links").addClass('in-view');
    }

});

