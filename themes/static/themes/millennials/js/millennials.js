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

    if($('.chapter h3').length){
        $('.chapter h3').each(function(){
            var originalText = $(this).text();
            if (originalText.indexOf(":") >= 0){
                var pieces = originalText.split(":");
                var newText = pieces[0] + '<span class="label">' + pieces[1] + '</span>';
                $(this).html(newText);
            }
        });
    }
    
    if($('.reveal').length){
        $(".reveal").mouseenter(function() {
		 $(".background-photo").css('opacity', '1.0');
        }).mouseleave(function () {
		 $(".background-photo").css('opacity', '0.3');
	 });
    }


    $(".colorize").letterEffect({
                 "effectParam": "color",
                "effectValues": [ "#196518", "#8c1b1b", "#555f04", "#1b5979", "#944b10" ],
            "ambientAnimation": true,
             "ambientstrength": .2,
                        "time": 1,
                        "drift": 0.25,
              "hoverAnimation": true,
                   "hoverTime": .3
        });
});