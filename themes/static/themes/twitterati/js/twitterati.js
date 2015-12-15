jQuery(document).ready(function() {

    $('.slider li').hide();
    $('.page-overlay').hide();
    $('.slider li').first().addClass('first');
    $('.slider li').last().addClass('last');

    var slides = $('.slider li').length;
    var hash = window.location.hash;

    if(hash){
        loadSlide(hash);
    }

    function loadSlide(handle){
        $('.slider').show();
        $('.close-box').show();
        $('li' + handle).addClass('active').fadeIn(800);
        $('.page-overlay').fadeIn(300);

        changePager(handle);
    }
    
    function changePager(hash){
        var index = $('.slider li' + hash).index()
        $('.next').removeClass('inactive');
        $('.prev').removeClass('inactive');

        if(index == slides - 1){
            $('.next').addClass('inactive');
        }
        if(index == 0 ){
            $('.prev').addClass('inactive');
        }
    }

    $(".twitterati-list li a").click(function(e) {

        $('.slider li').removeClass('active');
        e.preventDefault();

        var handle = $(this).attr("href");
        var selected = '#' + handle;
        loadSlide(selected);
        window.location.hash = handle;

    });


    $('.next').click(function(e){

        if(!$('.next').hasClass('inactive')){
            $('.slider li.active').fadeOut(800, function(){
                $('.slider li.active').removeClass('active').next().addClass('active');
                $('.slider li.active').fadeIn(800);
                var handle = $('.slider li.active').attr('id');
                var selected = '#' + handle;
                changePager(selected);
                window.location.hash = handle;
            });
            
        }
    });

   
    $('.prev').click(function(e){
        if(!$('.prev').hasClass('inactive')){
            $('.slider li.active').fadeOut(800, function(){
                $('.slider li.active').removeClass('active').prev().addClass('active');
                $('.slider li.active').fadeIn(800);
                var handle = $('.slider li.active').attr('id');
                var selected = '#' + handle;
                changePager(selected);
                window.location.hash = handle;
            });
            
        }   
        
    });

    $('.close-box').click(function(e){
        $('.close-box').fadeOut(400);
        $('.slider').fadeOut(400,function(){
            $('.page-overlay').fadeOut(400);
            $('.slider li').hide().removeClass('active');
        });
        
        var scrollPosition = $(window).scrollTop();
        window.location.hash = '';
        $(window).scrollTop(scrollPosition);
    });

    $('body').click(function(e){
        clickedTarget = $(e.target);
       if($('.page-overlay:visible')){
            if((!(clickedTarget.parents('.slider').length)) && (!(clickedTarget.parents('.twitterati-list').length))){
                $('.close-box').fadeOut(400);
                $('.slider').fadeOut(400,function(){
                    $('.page-overlay').fadeOut(400);
                    $('.slider li').hide().removeClass('active');
                });
                var scrollPosition = $(window).scrollTop();
                window.location.hash = '';
                $(window).scrollTop(scrollPosition);
            }
       }
    });

});

