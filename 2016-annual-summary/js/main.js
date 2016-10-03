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


var sections = $("body").find("section").length;
var sections = sections + 10;
//console.log(sections);
var zNumber = 0;

$("section").each(function(c) {
    console.log("this  " + c);
    $(this).addClass("z-"+[sections-c]);
//    $(this).addClass("z-"+[c]);
    
});

$("img").click(function(e){e.preventDefault();});
$("div").click(function(e){e.preventDefault();});