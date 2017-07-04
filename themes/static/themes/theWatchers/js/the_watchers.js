jQuery(document).ready(function() {
   
    function sizeFeature(){
        var windowHeight = $(window).height();
        var windowWidth = $(window).width();
        if($('video').length){
            featureHeight = windowWidth * 0.5;
            $('.main-feature').css("height", featureHeight + "px");
        }
    }
    
    $(window).load(function(){
        sizeFeature();
    });

    $(window).resize(function(){
        sizeFeature();
    });
});