(function ($) {

    var breakpoint = 985;
    var xsBreakpoint = 600;
    var chapter = $('.slider .chapter');
    var menuItem = $('#toc li a');
    var pagerItem = $('#nav li a');
    var pagerListItem = $('#nav li');

    var hash = window.location.hash;
    var people = ($('#nav ul li').length) - 1;
    var menuIndex = 0;
    var windowWidth = $(window).width();

    function initPage(){
        pagerListItem.hide();
        chapter.hide();

        if(hash === '' || hash === '#undefined'){
            hash = menuItem.first().attr('href');
            $('.prev').addClass('inactive');
            $('.next').removeClass('inactive');
        }
        $('.slider .chapter' + hash).addClass('active').fadeIn(800);
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
        $('.slider .chapter').removeClass('active').hide();
        $('.slider .chapter' + hash).addClass('active').fadeIn(800);
        return false;
    }

    function setPager(hash){
        var selected = null;
        var position = null;
        var left = 2;
        var right = 2;

        if(windowWidth < xsBreakpoint){
            left = right = 0;
        }
        else if(windowWidth < breakpoint){
            if(position < 1){
                left = 0;
                right = 2;
            }
            else if(position === people){
                right = 0;
                left = 2;
            }
            else{
                left = 1;
                right = 1;
            }
        }
        else if (windowWidth >= breakpoint){
            if(position < 2){
            left = position;
            right = 4 - position;
            }
            else if(position > (people - 2)){
                right = people - position;
                left = 4 - right;
            }
        }

        pagerListItem.hide();
        pagerListItem.removeClass('selected').removeClass('active-slide');

        pagerListItem.each(function(index){
           if($(this).children().attr('href') === hash){
               $(this).addClass('selected');
               selected = $(this);
               position = index;
           }
        });

        $(selected).nextAll(':lt(' + right + ')').addClass('active-slide');
        $(selected).prevAll(':lt(' + left + ')').addClass('active-slide');

    }

    function getPagerPosition(){
        var position = null;

        pagerListItem.each(function(index){
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
          scrollTop: $('.slider').offset().top
      }, 1000);
        return false;
    }

    /*  Activate selected slider and set pager */
     $(document).ready(function () {

        initPage();
        menuItem.on('click tap', getSlide);
        pagerItem.on('click tap', getSlide);

        $('.next').click(function(e){
            $('.prev').removeClass('inactive');

            if(!($('.next').hasClass('inactive'))){
                var currentHash = getPagerPosition().pagerHash;
                var pagerPosition = getPagerPosition().pagerIndex;
                var nextPosition = pagerPosition + 1;
                var newHash = $('#nav li:eq(' + nextPosition + ')').children().attr('href');

                setPager(newHash);

                if(nextPosition === people){
                    $('.next').addClass('inactive');
                }

            }
        });

         $('.prev').click(function(e){
             $('.next').removeClass('inactive');

            if(!($('.prev').hasClass('inactive'))){
                var currentHash = getPagerPosition().pagerHash;
                var pagerPosition = getPagerPosition().pagerIndex;
                var nextPosition = pagerPosition - 1;
                var newHash = $('#nav li:eq(' + nextPosition + ')').children().attr('href');

                setPager(newHash);

                if(nextPosition === 0){
                    $('.prev').addClass('inactive');
                }
            }
        });
    });

    $(window).resize(function() {
        windowWidth = $(window).width();
        initPage();
    });

 })(jQuery);

