jQuery(document).ready(function() {

    $('.slider li').hide();
    $('.slider li').first().addClass('first');
    $('.slider li').last().addClass('last');

    function changePager(){
        $('.next').removeClass('inactive');
        $('.prev').removeClass('inactive');

        if($('.last').hasClass('active')){
            $('.next').addClass('inactive');
        }

        if($('.first').hasClass('active')){
            $('.prev').addClass('inactive');
        }
    }

    $(".twitterati-list li a").click(function(e) {
         e.preventDefault();

        var handle = $(this).attr("href");
        var selected = $('#' + handle);
        selected.addClass('active');
        $('.page-overlay').addClass('active');

        $('.slider li').hide();
        selected.show();

        changePager();

    });


    $('.next').click(function(e){

        $('.slider li.active').next().addClass('active');
        $('.slider li.active').prev().removeClass('active');
        $('.slider li').hide();
        $('.slider li.active').show();

        changePager();
       
    });
   

    $('.prev').click(function(e){
        $('.slider li.active').prev().addClass('active');
        $('.slider li.active').next().removeClass('active');
        $('.slider li').hide();
        $('.slider li.active').show();

        changePager();
        
    });

    $('.close-box').click(function(e){
        $('.slider li').hide();
        $('.slider li').removeClass('active');
        $('.page-overlay').removeClass('active');
    });

});

$(window).load(function() {
      $('.slider li').hide();
});

