jQuery(document).ready(function() {

	updateHeaderTransparency();    

    $(window).scroll(function(){
	    updateHeaderTransparency();
	});

    function updateHeaderTransparency() {
    	if ($('header').hasClass('collapsed')) {
	        transparencyOff();
	    } else if ($('.jumbotron').length && !$("body").hasClass("template-home-page")) {
	         transparencyOn();
	    }
    }

    function transparencyOn() {
        $('header').addClass("transparency");
        $('#toggle-mobile').hide();
        $('#search-box-toggle').hide();
        $('#main-menu').hide();
    }

    function transparencyOff() {
        $('header').removeClass("transparency");
        $('#toggle-mobile').show();
        $('#search-box-toggle').show();
        $('#main-menu').show();
    }
});