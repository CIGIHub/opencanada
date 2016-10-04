wow = new WOW(
    {
		  boxClass:     'wow',      
		  animateClass: 'animated', 
		  offset:       50,          
		  mobile:       true,       
		  live:         true
	}
)
wow.init();


//var sections = $("body").find("img.cover").length;
//var sections = sections + 10;
////console.log(sections);
//var zNumber = 0;
//
//$("img.cover").each(function(c) {
//    console.log("this  " + c);
//    $(this).addClass("z-"+[sections-c]);
////    $(this).addClass("z-"+[c]);
//});


var scrollingSpeed = 1.5*1000;

$(function() {

	$.scrollify({
		section:"section",
		setHeights: false,
		sectionName : false,
		scrollSpeed: scrollingSpeed,
		after:function(i) { // i is section number
			
			// alert(i);
			$('.counter').countTo({
				from: 50,
				to: 2500,
				speed: scrollingSpeed,
				refreshInterval: 50,
				onComplete: function(value) {
					console.debug(this);
				}
			});
		}
	});

});