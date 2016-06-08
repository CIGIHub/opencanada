jQuery(document).ready(function() {
    
    var windowWidth;
    var featureHeight;

    //wrap the work 'leftist' to apply styling
	$('.leftist-feature h1').html($('.leftist-feature h1').html().replace(/(Leftist)/g,'<span>$1</span>'));


    $(window).on('load resize', function(){

    	windowWidth = $(window).width();
    	featureHeight = $('.leftist-feature').height();
     	$('.feature-right').css("height", featureHeight);  	

    });

	$(window).on('scroll', function(){

		if(windowWidth > 768){

    		if($('body').scrollTop() >= (featureHeight - 100)){
	    		$('.table-of-contents').css({
	    			"position": "fixed",
	    			"top": "100px",
	    			"float": "none"
	    		});
	    	}
	    	else{
	    		$('.table-of-contents').css({
	    			"position": "relative",
	    			"top": "",
	    			"float": "left"
	    		});
	    	}
    	}
    	else{
    		$('.table-of-contents').css({
	    			"position": "relative",
	    			"top": "",
	    			"float": "none"
	    		});
    	}
	
    	if($('body').scrollTop() > (featureHeight/4) ){
    		$('.feature-right').addClass('slide-left');
    	}
    	if($('body').scrollTop() < (100) ){
    		$('.feature-right').removeClass('slide-left');
    	}

	});

});

