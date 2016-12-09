jQuery(document).ready(function() {

    var dd;
    var startDate = 1451624400;
    $('.counter').html( startDate );
    
    function countScroll(sectionNo) {	

        //move date
        var nextDate;
        var prevDate;

            //console.log("section: " + sectionNo);
            nextItem = sectionNo + 1;
            
            nextDate = $("section:nth-of-type("+ nextItem +")").data("date") * 1000;
            prevDate = $("section:nth-of-type("+ sectionNo +")").data("date") * 1000;
                        
        if (sectionNo === 2) {
            var lastDate = startDate;
        };
        //console.log("lastDate: " + lastDate);

        $('.counter').countTo({
        	from: nextDate,
        	to: prevDate,
        	speed: 1100,
        	refreshInterval: 50,
        	onComplete: function(value) {
        		//var lastDate = nextDate; 
                //console.log(this);
        	}
        });

        var dateInput = $(".counter").text();
	    var datePrint = moment(dateInput, "x").format("MMMM DD, YYYY"); // Oct 4th 16; 
	    //$('.date').text(datePrint);
        //console.log(datePrint);

        var lastDate = nextDate;

        //get section Number and only display pager once past the feature item
        dd = sectionNo - 1;
       
        if (dd >= 0) {
            $('.paging').fadeIn();
        };	
        if (dd <= -1) {
            $('.paging').fadeOut();
        };
        if (dd == -1) {
            dd = dd+1;
        };
        
        $('.aCurrent').html( dd );

    }

    //check if the item is in the viewport
    $.fn.isOnScreen = function(){
        
        var win = $(window);
        
        var viewport = {
            top : win.scrollTop(),
            left : win.scrollLeft()
        };
        viewport.right = viewport.left + win.width();
        viewport.bottom = viewport.top + win.height();
        
        var bounds = this.offset();
        bounds.right = bounds.left + this.outerWidth();
        bounds.bottom = bounds.top + this.outerHeight();
        
        return (!(viewport.right < bounds.left || viewport.left > bounds.right || viewport.bottom < bounds.top || viewport.top > bounds.bottom));
        
    };

    //scroll to next section based on body class
    $(function() {
        $.scrollify({
            section : "section",
            sectionName: false,
            setHeights: false,
            before:function(sectionNo) { 
                countScroll(sectionNo);
                $('.date').removeClass( "fadeOutDown" );
                $('.date').addClass( "animated fadeOutUp" );
            },
            after: function() {
                $('.date').removeClass( "fadeOutUp" );	
                $('.date').addClass( "animated fadeInDown" );	
            },
        });
    });

    // Animate feature text when section is in viewport
    if($("section").isOnScreen){
        $("section .fade-righ").addClass("in-view");
    }
    else{
         $("section .fade-right").removeClass("in-view");
    }

    // Activate menu
    $( ".mNav" ).on('touchstart click', this, function() {
        $( ".mNav-menu" ).toggleClass( "closed" );
        $( this ).toggleClass( "hover" );
    });

    $( ".mNav-menu ol a" ).each(function() {
        $(this).on('touchstart click', this, function() {
            $( ".mNav-menu" ).toggleClass( "closed" );
            $( this ).toggleClass( "hover" );
        });
    });

    //Navigate with pager
    $(".aNext").on('touchstart click', this, function(e) {
        $.scrollify.next();
    });

    $(".aBack").on('touchstart click', this, function(e) {
        $.scrollify.previous();
    });

    // Click to go to next section
    // $("section:nth-of-type(1)").on('touchstart click', this, function(e) {
	//     $.scrollify.next();
    // });

}); 

$(window).load(function() {
    //get the number of sections and set total in counter
    var numberOfSections = $( "section" ).length;
    $('.aTotal').html(numberOfSections - 2);
    $('.aCurrent').html( '0' );

    $('section.feature .fade-right').addClass('in-view');   


});

$(window).scroll(function(){
     var windowTop = Math.max($('body').scrollTop(), $('html').scrollTop());
    
    $('section').each(function (index) {
      

      console.log('windowtop: ' + windowTop);
        console.log('index: ' + index + ' section position: ' + $(this).position().top);
        if (windowTop > ($(this).position().top)){
            
            //console.log(index);            
            $('section .fade-right').removeClass('in-view');
            $('section:eq(' + index + ') .fade-right').addClass('in-view');
        }
    });
});