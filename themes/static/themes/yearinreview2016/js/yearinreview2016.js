jQuery(document).ready(function() {

    var dd;

    function countScroll(d) {	
    
        // var nextDate = $("section:nth-of-type("+[d+1]+")").data("date");
        // var prevDate = $("section:nth-of-type("+[d+0]+")").data("date");
                            
        // if (d === 1) {
        //     var lastDate = startDate;
        // };
        
        dd = d - 1;
        console.log(dd);
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

        // $('.counter').countTo({
        // 	from: nextDate,
        // 	to: prevDate,
        // 	speed: scrollingSpeed,
        // 	refreshInterval: 50,
        // 	onComplete: function(value) {
        // 		var lastDate = nextDate; 
        // 	}
        // });
        //var lastDate = nextDate;
    }

    //scroll to next section based on body class
    $(function() {
        $.scrollify({
            section : "section",
            
            before:function(i) { // i is section number
                countScroll(i);
                $('.date').removeClass( "fadeOutDown" );
                $('.date').addClass( "animated fadeOutUp" );
            },
            after: function() {
                $('.date').removeClass( "fadeOutUp" );	
                $('.date').addClass( "animated fadeInDown" );	
            },
            // afterResize:function() {
            //     $.scrollify.current()
            // }
        });
    });

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
    $("section:nth-of-type(1)").on('touchstart click', this, function(e) {
	    $.scrollify.next();
    });

}); 

$(window).load(function() {
        //get the number of sections and set total in counter
        var numberOfSections = $( "section" ).length;
        $('.aTotal').html(numberOfSections - 2);
        $('.aCurrent').html( '0' );
});