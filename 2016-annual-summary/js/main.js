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
var startDate = $("section:nth-of-type(1)").data("date");

$(window).load(function() {
      $('.counter').html( startDate );
});

var lastDate, nextDate = $("section:nth-of-type(2)").data("date");

$(function() {

	$.scrollify({
		section:"section",
		setHeights: false,
		sectionName : false,
		scrollSpeed: 1500,
		before:function(i) { // i is section number
			var d = i+1; 		// play nice with nth-of-type
			var nextDate = $("section:nth-of-type("+[d]+")").data("date");
			
//			alert("i="+i+",d="+d);
			
			if (d == 1) {
				lastDate = startDate;
			};
			$('.counter').countTo({
				from: lastDate,
				to: nextDate,
				speed: scrollingSpeed,
				refreshInterval: 100,
				onComplete: function(value) {
					console.debug(this);
				}
			});
			var lastDate = nextDate;
		}
	});

});