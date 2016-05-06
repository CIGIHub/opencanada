(function ($) {

    var breakpoint = 985;
    var xsBreakpoint = 600;
    var windowWidth = $(window).width();

    var chapter = $('.profile .chapter');
    var menuItem = $('#toc li a');

    var pager = $('#pager ul');
    var pagerItem = $('#pager ul li');
    var pagerItemLink = $('#pager ul li a');
    var pagerCount = pagerItem.length;
    var pagerItemWidth = pagerItem.width();
    var pagerWidth = pagerItemWidth * 5;

    var hash = window.location.hash;
    var menuIndex = 0;

    function initPage(windowWidth){
        chapter.hide();

        if(windowWidth < xsBreakpoint){
            pagerWidth = pagerItemWidth;
        }
        else if(windowWidth < breakpoint){
            pagerWidth = pagerItemWidth * 3;
        }
        else{
            pagerWidth = pagerItemWidth * 5;
        }
        $('#pager').css("width",  + pagerWidth + "px");
        pager.width(pagerCount * pagerItemWidth);
        pager.css("left", "0px");

        if(hash === '' || hash === '#undefined'){
            hash = menuItem.first().attr('href');
            $('.prev').addClass('inactive');
            $('.next').removeClass('inactive');
        }

        $('.profile .chapter' + hash).addClass('active').fadeIn(800);
        setPager(hash);
    }

    function getSlide(){
        hash = $(this).attr('href');
        loadSlide(hash);
        scrollView();
        setPager(hash);
    }

    function loadSlide(hash){
        menuIndex = menuItem.index(this);
        window.location.hash = hash;
        $('.profile .chapter').removeClass('active').hide();
        $('.profile .chapter' + hash).addClass('active').fadeIn(800);
        return false;
    }

    function setPager(hash){
        var selected = null;

        pagerItem.removeClass('selected');

        pagerItem.each(function(index){
           if($(this).children().attr('href') === hash){
               $(this).addClass('selected');
               selected = $(this);
               position = index;
           }
        });
    }

    function getPagerPosition(){
        var position = null;

        pagerItem.each(function(index){
           if($(this).hasClass('selected')){
               hash = $(this).children().attr('href');
               position = index;
           }
        });

        return {
            pagerHash : hash,
            pagerIndex : position
        };
    }

    function scrollView() {
      $('html,body').animate({
          scrollTop: $('.profile').offset().top
      }, 1000);
        return false;
    }

    /*  Activate selected slider and set pager */
     $(document).ready(function (e) {

        initPage();
        menuItem.on('click tap', getSlide);
        pagerItemLink.on('click tap', getSlide);


        $('.prev').click(function () {
            $('.next').removeClass('inactive');

            if(!($('.prev').hasClass('inactive'))) {
                $('#pager ul').animate({left: '+=' + pagerItemWidth}, 500);
                if($('#pager ul').css("left") === "-85px"){
                    $('.prev').addClass('inactive');
                }
            }
        });

        $('.next').click(function () {

            $('.prev').removeClass('inactive');
            if(!($('.next').hasClass('inactive'))){
                $('#pager ul').animate({left: '-='+pagerItemWidth}, 500);
                console.log($('#pager ul').css("left"));
                if($('#pager ul').css("left") === "-255px"){
                    $('.next').addClass('inactive');
                }

            }
        });

    });

    $(window).resize(function() {
        windowWidth = $(window).width();
        initPage(windowWidth);
    });

 })(jQuery);

