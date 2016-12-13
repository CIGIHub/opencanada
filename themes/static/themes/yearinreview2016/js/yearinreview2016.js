    
    var windowWidth = null;

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
            $('.paging').addClass('display');
        };	
        if (dd <= -1) {
            $('.paging').removeClass('display');
        };
        if (dd == -1) {
            dd = dd+1;
        };
        
        $('.aCurrent').html( dd );

    }

// Activate menu
    $( ".mNav" ).on('click', this, function() {
        $( ".mNav-menu" ).toggleClass( "closed" );
        $( this ).toggleClass( "hover" );
    });

    $( ".mNav-menu ol a" ).each(function() {
        $(this).on('click', this, function() {
            $( ".mNav-menu" ).toggleClass( "closed" );
            $( ".mNav" ).toggleClass( "hover" );
        });
    });

function scrollToSection(){
//scroll to next section based on body class
    $(function() {
        $.scrollify({
            section : "section",
            sectionName: false,
            setHeights: false,
            overflowScroll: true,
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

    //Navigate with pager
    $(".aNext").on('click', this, function(e) {
        $.scrollify.next();
    });

    $(".aBack").on('click', this, function(e) {
        $.scrollify.previous();
    });

    // Click touchstart scroll from feature to body
    $("section.feature").on('click', this, function(e) {
	    $.scrollify.next();
    });

}
    

$(window).load(function() {

    windowWidth = $(window).width();

    if(windowWidth > 480){
        scrollToSection();
    }

    //get the number of sections and set total in counter
    var numberOfSections = $( "section" ).length;
    $('.aTotal').html(numberOfSections - 2);
    $('.aCurrent').html( '0' );

    if($("#intro").length){
        $("#intro h2").addClass("fade-right");
    } 

    $('section.feature .fade-right').addClass('in-view'); 
    
});

$(window).resize(function() {
    windowWidth = $(window).width();
    if(windowWidth > 480){
        scrollToSection();
    }
});

//add class to meta content & title to allow it scroll in from the left.
$(window).scroll(function(){
    var windowTop = Math.max($('body').scrollTop(), $('html').scrollTop());
    
    $('section').each(function (index) {
        if (windowTop > ($(this).position().top)){
            $('section .fade-right').removeClass('in-view');
            $('section:eq(' + index + ') .fade-right').addClass('in-view');
        }
    });
});