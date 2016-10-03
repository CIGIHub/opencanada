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

$(function() {

	$.scrollify({
		section:"section",
		setHeights: false,
		sectionName : false,
		after:function(i) {

		}
	});

});