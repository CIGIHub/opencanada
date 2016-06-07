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

        if(($(".js").length) && windowWidth > 768){
            setTimeout(clouds, 800);
            setTimeout(textUp, 1500);
            setTimeout(header, 2500);
            setTimeout(text, 4000);
        }
    
    });

    function clouds(){
        $(".right-cloud, .left-cloud").addClass("in-view");
    }
    function textUp(){
        //$(".feature-wrapper").show();
        $(".feature-wrapper").addClass("in-view");
    }
    function header(){
        $("h1").addClass("in-view");
    }
    function text(){
        $(".contributors, ul.share-links").addClass("in-view");
    }

});

