//wow = new WOW(
//    {
//		  boxClass:     'wow',      
//		  animateClass: 'animated', 
//		  offset:       0,          
//		  mobile:       true,       
//		  live:         true
//	}
//)
//wow.init();
//
//$(document).ready(function() {
//	$('#sticky-navigation').scrollspy();
//});


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

AOS.init({
  startEvent: 'DOMContentLoaded',
  offset: 200,
  duration: 1200,
  easing: 'ease',
  delay: 100
});


var scrollingSpeed = 1.5*1000;
var startDate = $("section:nth-of-type(1)").data("date");


$(window).load(function() {
		$('.counter').html( startDate );
});

$('.counter').bind("DOMSubtreeModified",function(){
	var dateInput = $(".counter").text();
	var datePrint = moment(dateInput, "x").format("MMMM DD, YYYY"); // Oct 4th 16; 
	$('.date').text(datePrint);
});

function countScroll(d) {
    var nextDate = $("section:nth-of-type("+[d+1]+")").data("date");
    var prevDate = $("section:nth-of-type("+[d+0]+")").data("date");
						
	if (d === 1) {
		var lastDate = startDate;
	};

//	alert("next " + nextDate + " | last " + lastDate);

	$('.counter').countTo({
		from: nextDate,
		to: prevDate,
		speed: scrollingSpeed,
		refreshInterval: 50,
		onComplete: function(value) {
//			console.debug(this);
			var lastDate = nextDate; 
		}
	});
	var lastDate = nextDate;             // The function returns the product of p1 and p2
}

$(function() {

	$.scrollify({
		section:"section",
		setHeights: false,
		sectionName : false,
		scrollSpeed: scrollingSpeed,
		before:function(i) { // i is section number
			countScroll(i); // play nice with nth-of-type
			$('.date').removeClass( "fadeOutDown" );
			$('.date').addClass( "animated fadeOutUp" );
		},
		after: function() {
			$('.date').removeClass( "fadeOutUp" );	
			$('.date').addClass( "animated fadeInDown" );	
		}
	});

});

$("#header-2").hide(); // hide the fixed navbar initially

var topofDiv = $("section:nth-of-type(1)").offset().top; //gets offset of header
var height = $("section:nth-of-type(1)").outerHeight(); //gets height of header

$(".dateContainer").hide();
$(window).scroll(function(){
    if($(window).scrollTop() > (topofDiv + height)){
       $(".dateContainer").show();
    }
    else{
       $(".dateContainer").hide();
    }
});



//// 2 Way wowjs http://stackoverflow.com/questions/33187211/wow-js-repeat-animation-every-time-you-scroll-up-or-down
//
//$(function() {
//
//  var $window           = $(window),
//      win_height_padded = $window.height() * 1.1,
//      isTouch           = Modernizr.touch;
//
//  if (isTouch) { $('.revealOnScroll').addClass('animated'); }
//
//  $window.on('scroll', revealOnScroll);
//
//  function revealOnScroll() {
//    var scrolled = $window.scrollTop(),
//        win_height_padded = $window.height() * 1.1;
//
//    // Showed...
//    $(".revealOnScroll:not(.animated)").each(function () {
//      var $this     = $(this),
//          offsetTop = $this.offset().top;
//
//      if (scrolled + win_height_padded > offsetTop) {
//        if ($this.data('timeout')) {
//          window.setTimeout(function(){
//            $this.addClass('animated ' + $this.data('animation'));
//          }, parseInt($this.data('timeout'),10));
//        } else {
//          $this.addClass('animated ' + $this.data('animation'));
//        }
//      }
//    });
//    // Hidden...
//   $(".revealOnScroll.animated").each(function (index) {
//      var $this     = $(this),
//          offsetTop = $this.offset().top;
//      if (scrolled + win_height_padded < offsetTop) {
//        $(this).removeClass('animated fadeInUp flipInX lightSpeedIn')
//      }
//    });
//  }
//
//  revealOnScroll();
//});