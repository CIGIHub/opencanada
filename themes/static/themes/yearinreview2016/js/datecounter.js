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
