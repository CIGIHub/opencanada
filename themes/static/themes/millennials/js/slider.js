jQuery(document).ready(function() {


    var chapter = $('.slider .chapter');
    var menuItem = $('#toc li a');
    var pagerItem = $('#nav li a');
    var pagerListItem = $('#nav li');

    var hash = window.location.hash;
    var people = ($('#nav ul li').length) - 1;
    var menuIndex = 0;

    initPage();

    function initPage(){
        pagerListItem.hide();
        chapter.hide();

        if(hash === '' || hash === '#undefined'){
            hash = menuItem.first().attr('href');
        }
        loadSlide(hash);
        setPager(hash);
    }

    function getSlide(){
        hash = $(this).attr('href');
        loadSlide(hash);
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
        pagerListItem.hide();
        pagerListItem.removeClass('active');

        pagerListItem.each(function(index){

           if($(this).children().attr('href') === hash){
               $(this).addClass('active').show();
               selected = $(this);
               position = index;
           }
        });

        // console.log(selected);
        // console.log(position);

        //set pager for 5 items
        var left = 2;
        var right = 2;

        if(position < 2){
            left = position;
            right = 4 - position;
        }
        else if(position > (people - 2)){
            right = people - position;
            left = 4 - right;

        }

        $(selected).nextAll(':lt(' + right + ')').show();
        $(selected).prevAll(':lt(' + left + ')').show();

    }

    function getPagerPosition(){
        var position = null;

        pagerListItem.each(function(index){
           if($(this).hasClass('active')){
               hash = $(this).children().attr('href');
               position = index;
           }
        });

        return {
            pagerHash : hash,
            pagerIndex : position
        };
    }

    menuItem.on('click tap', getSlide);
    pagerItem.on('click tap', getSlide);


    $('.next').click(function(e){

        if(!($('.next').hasClass('inactive'))){
            var currentHash = getPagerPosition().pagerHash;
            var pagerPosition = getPagerPosition().pagerIndex;
            var nextPosition = pagerPosition + 1;
            var newHash = $('#nav li:eq(' + nextPosition + ')').children().attr('href');

            loadSlide(newHash);
            setPager(newHash);

            if(nextPosition === people){
                $('.next').addClass('inactive');
            }
        }

    });

     $('.prev').click(function(e){

        if(!($('.prev').hasClass('inactive'))){
            var currentHash = getPagerPosition().pagerHash;
            var pagerPosition = getPagerPosition().pagerIndex;
            var nextPosition = pagerPosition - 1;
            var newHash = $('#nav li:eq(' + nextPosition + ')').children().attr('href');

            loadSlide(newHash);
            setPager(newHash);

            if(nextPosition === 0){
                $('.prev').addClass('inactive');
            }
        }

    });


    // function scrollView() {
    //   return this.each(function () {
    //     $('html, body').animate({
    //       scrollTop: $(this).offset().top
    //     }, 1000);
    //   });
    // }
});

