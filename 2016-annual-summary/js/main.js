function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

var click_event = $.support.touch ? "tap" : "click";

AOS.init({
//  startEvent: 'DOMContentLoaded',
  offset: 200,
  duration: 1200,
  easing: 'ease',
  delay: 100
});

// Counter on scroll 

var scrollingSpeed = 1.5*1000;
var startDate = $("section:nth-of-type(1)").data("date");

$(window).load(function() {
		$('.counter').html( startDate );
});

var counterFn = debounce(function() {
	var dateInput = $(".counter").text();
	var datePrint = moment(dateInput, "x").format("MMMM DD, YYYY"); // Oct 4th 16; 
	$('.date').text(datePrint);
//	console.log(datePrint);
}, 15);

$('.counter').bind("DOMSubtreeModified",counterFn);

var dd;
function countScroll(d) {
	
//	console.log(d);
	
    var nextDate = $("section:nth-of-type("+[d+1]+")").data("date");
    var prevDate = $("section:nth-of-type("+[d+0]+")").data("date");
						
	if (d === 1) {
		var lastDate = startDate;
	};
	
	dd = d - 1;
	if (dd >= 0) {
		$('.paging').addClass('show');
	};	
	if (dd <= -1) {
		$('.paging').removeClass('show');
	};
	if (dd == -1) {
		dd = dd+1;
	};
	
	$('.aCurrent').html( dd );


	$('.counter').countTo({
		from: nextDate,
		to: prevDate,
		speed: scrollingSpeed,
		refreshInterval: 50,
		onComplete: function(value) {
			var lastDate = nextDate; 
		}
	});
	var lastDate = nextDate;
	
	
}

// Scroll Params

$(function() {

	$.scrollify({
		section:"section",
		sectionName : false,
		setHeights: false,
		offset : 0,
		overflowScroll: true,
		scrollSpeed: scrollingSpeed,
		before:function(i) { // i is section number
			countScroll(i);
			$('.date').removeClass( "fadeOutDown" );
			$('.date').addClass( "animated fadeOutUp" );
		},
		after: function() {
			$('.date').removeClass( "fadeOutUp" );	
			$('.date').addClass( "animated fadeInDown" );	
		},
		afterResize:function() {
			$.scrollify.current()
		}
	});

});

// Show hide date

var topofDiv = $("section:nth-of-type(1)").offset().top; //gets offset of header
var topofDiv2 = $("section:nth-of-type(3)").offset().top; //gets offset of header
var hideDate = $("#note").offset().top + $("#note").outerHeight() - 80; //gets offset of header
var height = $("section:nth-of-type(1)").outerHeight(); //gets height of header
var contribHeight = $(".contrib").offset().top - 100; //gets height of contrib section

$(".dateContainer").hide();
$(window).scroll(function(){
	contribHeight = $(".contrib").offset().top - 10;
    if($(window).scrollTop() > (hideDate)){
       $(".dateContainer").show();
    }else if($(window).scrollTop() > contribHeight){
       $(".dateContainer").hide();
		console.log("hide");
    }
    else{
       $(".dateContainer").hide();
    }
});

// BG image effect

$('.bgTrigger').each(function() {
	$( this ).hover(
  function() {
    $( this ).closest('section').addClass( "zoomImage" );
  }, function() {
    $( this ).closest('section').removeClass( "zoomImage" );
  });
});

// Build direction nav

$("section:nth-of-type(1) a").on(click_event, this, function(e) {
	$.scrollify.next();
});

var n = $( ".story" ).length;
$('.aTotal').html(n-1);

$(".aNext").on(click_event, this, function(e) {
    e.preventDefault();
    $.scrollify.setOptions({
        scrollSpeed: 2500,
    });
    $.scrollify.next();
});

$(".aBack").on(click_event, this, function(e) {
    e.preventDefault();
    $.scrollify.setOptions({
        scrollSpeed: 2500,
    });
    $.scrollify.previous();
});

// Build Nav + Story IDs, 2 pages before first story

$('section').each(function( i ) {
	if( i >= 1 ){
		$( this ).attr( "id", "story" + [i-1] );
	}
	var Title = $( "section:nth-of-type("+[i+1]+")" ).find('h2').text();
	var navString = "<li><a href='"+ '#' + this.id +"'><span>"+ [i-1] +".</span> <h2>" + Title + "</h2></a></li>";
	if( i >= 1 ){
		$( ".mNav-menu ul" ).append( navString );
	}
});

// Animate menu

$( ".mNav" ).on(click_event, this, function() {
  $( ".mNav-menu" ).toggleClass( "closed" );
  $( this ).toggleClass( "hover" );
});

$( ".mNav-menu ul a" ).each(function() {
	$(this).on(click_event, this, function() {
  		$( ".mNav-menu" ).toggleClass( "closed" );
		$( this ).toggleClass( "hover" );
	});
});

// Fade out date on scroll

var scrollCkeckFn = debounce(function() {
	$(window).scroll(function() {

		var scrollTop     = $(this).scrollTop(),
		elementOffset = $.scrollify.current().offset().top,
		distance      = (elementOffset - scrollTop)*-1;

		if (distance > 40) {
				$('.date').removeClass( "fadeOutDown" );
				$('.date').addClass( "animated fadeOutUp" );
		} else if (distance < 40 || distance > 20 ) {
				$('.date').removeClass( "fadeOutUp" );	
				$('.date').addClass( "animated fadeInDown" );	
		} 
		
		if ( $.scrollify.current().hasClass( "contrib" )) {
			$('.date').addClass("hide")
		} else (
			$('.date').removeClass("hide")
		)
//		console.log("scroll "+distance)
	});
}, 100);

scrollCkeckFn();