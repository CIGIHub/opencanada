jQuery(document).ready(function() {
    
    var windowWidth;
    var featureHeight;

    //wrap the work 'leftist' to apply styling
	$('.leftist-feature h1').html($('.leftist-feature h1').html().replace(/(Leftist)/g,'<span>$1</span>'));

    $(window).on('scroll load resize', function(){
    	windowWidth = $(window).width();
		
		//reset feature height on resize
		$('.leftist-feature').css("height", "auto");
    	featureHeight = $('.feature-left').height();
    	$('.leftist-feature').css("height", featureHeight);
    	$('.feature-right').css("height", "100%");  	

    	/*
    		for desktop size fix the table of contents to the left at 100px down the page.  On mobile allow the
    		table of contents to sit inline with the rest of the content.
    	*/
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

