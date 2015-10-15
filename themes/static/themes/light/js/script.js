jQuery(document).ready(function() {

    updateMainFeature();

    $(window).resize(function(){
        updateMainFeature();
    });
    
    //update the height of the main feature depending on the screen size.
    //since we know the bg image is 1276 x 1020, we can always show the same percentage of the image
    //no matter what screen size we are on.
    function updateMainFeature(){

        var width = $(window).width();
        height = width * 1020 / 1276;
        height = height * 0.85; //85% so there is some overlap into the main content
        $('.main-feature').css("height", height + "px");
    }

});
