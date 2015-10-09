jQuery(document).ready(function() {

    updateHeaderTransparency();
    updateMainFeature();

    $(window).scroll(function(){
	    updateHeaderTransparency();
	});

    $(window).resize(function(){
        updateHeaderTransparency();
        updateMainFeature();
    });

    function updateHeaderTransparency() {
        var offset = ($('header').height() + parseInt($('main').css('padding-top')) ) * -1;
        $('.main-feature').css("margin-top", offset);

    	if ($('header').hasClass('scrolled') || $('#search-box').hasClass("open")) {
	        transparencyOff();
	    } else if ($('.main-feature').length && !$("body").hasClass("template-home-page")) {
	         transparencyOn();
	    }
    }

    //update the height of the main feature depending on the screen size.
    //since we know the bg image is 1276 x 1020, we can always show the same percentage of the image
    //no matter what screen size we are on.
    function updateMainFeature(){

        var width = $(window).width();
        height = width * 1020 / 1276;
        height = height * 0.85; //85% so there is some overlap into the main content
        $('.main-feature').css("height", height + "px");
    }

    function transparencyOn() {
        $('header').addClass("transparency");
        $('#toggle-mobile').hide();
        $('#search-box-toggle').hide();
        $('#main-menu').hide();
        //$('.wordmark').css("opacity", 0.5);
    }

    function transparencyOff() {
        $('header').removeClass("transparency");
        $('#toggle-mobile').fadeIn(1000);
        $('#search-box-toggle').fadeIn(1000);
        $('#main-menu').show();
        //$('.wordmark').css("opacity",1);

        if ($('#search-box').hasClass("open") && $(window).width() >= breakpoint) {

            if ($('header').hasClass('collapsed')) {
                $('#toggle-mobile').show();
            } else {
               $('#toggle-mobile').hide();
            }
        }
    }
});
