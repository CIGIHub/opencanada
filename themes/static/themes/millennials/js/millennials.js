jQuery(document).ready(function() {

    $(window).on('load resize', function(){
        var windowWidth = $(window).width();
        if($('.quote').length && windowWidth > 992){
            quoteSize();
        }
    });

    function quoteSize(){
        $('.quote').each(function (index, value){
            var blockHeight = $(this).height();
            var maxHeight = 300;
            var minHeight = 150;
            var fontSize = 1.0;
            var fontAdjust = 1.0;

            // console.log(blockHeight);
            if(blockHeight > maxHeight){
                fontAdjust = maxHeight/blockHeight;

            }
            if(blockHeight < minHeight ){
                fontAdjust = minHeight/blockHeight;
            }
            fontSize = fontSize * fontAdjust;

            $(this).css({'font-size': fontSize+'em', 'line-height' : '130%'});
        });
    }

    // $("a[href*='#']:not([href='#'])").click(function() {
    //     var target = $(this.hash);
    //     target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
    //     if (target.length) {
    //         $('html,body').animate({
    //             scrollTop: target.offset().top - 150
    //             }, 1000);
    //         return false;
    //     }
    // });
});