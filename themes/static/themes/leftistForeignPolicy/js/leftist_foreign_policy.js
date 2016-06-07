jQuery(document).ready(function() {
    
    var windowWidth = $(window).width();
    var featureHeight = $('.leftist-feature').height();

	$('.leftist-feature h1').html($('.leftist-feature h1').html().replace(/(Leftist)/g,'<span>$1</span>'));

    $(window).on('scroll load resize', function(){
    	windowWidth = $(window).width();
    	featureHeight = $('.leftist-feature').height();

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

    	

    });



    

});

