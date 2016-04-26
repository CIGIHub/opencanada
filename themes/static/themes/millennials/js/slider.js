jQuery(document).ready(function() {

    $('.slider .chapter').hide();
    $('.slider .chapter').first().addClass('first');
    $('.slider .chapter').last().addClass('last');

    var slides = $('.slider .chapter').length;
    var hash = window.location.hash;

    function loadSlide(hash){

        $('.slider .chapter').removeClass('active').hide();
        $('.slider .chapter' + hash).addClass('active').fadeIn(600);
        return false;
        window.location.hash = hash;
    }

    function changePager(hash){
        var index = $('.slider .chapter' + hash).index()
        $('.next').removeClass('inactive');
        $('.prev').removeClass('inactive');

        if(index == slides - 1){
            $('.next').addClass('inactive');
        }
        if(index == 0 ){
            $('.prev').addClass('inactive');
        }
    }

    $('.next').click(function(e){

        if(!$('.next').hasClass('inactive')){
            $('.slider li.active').fadeOut(400, function(){
                $('.slider li.active').removeClass('active').next().addClass('active');
                $('.slider li.active').fadeIn(400);
                var handle = $('.slider li.active').attr('id');
                var selected = '#' + handle;
                changePager(selected);
                window.location.hash = handle;
            });

        }
    });


    $('.prev').click(function(e){
        if(!$('.prev').hasClass('inactive')){
            $('.slider li.active').fadeOut(400, function(){
                $('.slider li.active').removeClass('active').prev().addClass('active');
                $('.slider li.active').fadeIn(400);
                var handle = $('.slider li.active').attr('id');
                var selected = '#' + handle;
                changePager(selected);
                window.location.hash = handle;
            });

        }

    });

    if(hash.length && hash != 'toc' && hash != 'chapter') {
        loadSlide(hash);
    }
    else{
        $('.slider .chapter').first().addClass('active');
        $('.slider .chapter').first().fadeIn(400);
    }

    $(".faces li a").on('click focus', function(e) {
        e.preventDefault();
        hash = $(this).attr("href");
        loadSlide(hash);

    });

    // function scrollView() {
    //   return this.each(function () {
    //     $('html, body').animate({
    //       scrollTop: $(this).offset().top
    //     }, 1000);
    //   });
    // }
});

