(function ($) {

    var breakpoint = 985;
    var smBreakpoint = 600;
    var xsBreakpoint = 480;
    var windowWidth = $(window).width();

    var chapter = $('.profile .chapter');
    var menuItem = $('#toc li a');

    var pager = $('#pager ul');
    var pagerItem = $('#pager ul li');
    var pagerItemLink = $('#pager ul li a');

    var pagerCount = pagerItem.length;
    var indexCount = pagerCount - 1;

    var pagerItemWidth = pagerItem.width();
    var pagerWidth = pagerItemWidth * 5;
    var fullPagerWidth = pagerCount * pagerItemWidth;

    var pagerDisplayLimit = 5;

    var selectedIndex = 0;
    var selectedItem = null;
    var animating = false;

    function initPage(windowWidth){
        chapter.hide();

        if(windowWidth < xsBreakpoint){
           pagerDisplayLimit = 2;
        }
        else if(windowWidth < smBreakpoint){
            pagerDisplayLimit = 3;
        }
        else{
            pagerDisplayLimit = 5;
        }

        pagerWidth = pagerItemWidth * pagerDisplayLimit;
        $('#pager').css("width",  + pagerWidth + "px");
        pager.width(fullPagerWidth);
        pager.css("left", "0px");

        if(window.location.hash === '' || window.location.hash === '#undefined'){
            selectedItem = menuItem.first().attr('href');
        }
        else{
            selectedItem = window.location.hash;
        }
        loadSlide(selectedItem);
    }

    function getSlide(){

        selectedItem = $(this).attr('href');
        loadSlide(selectedItem);
        scrollView($('.profile'));
    }

    function loadSlide(selectedItem){

        chapter.removeClass('active').hide();
        $('.profile .chapter' + selectedItem).addClass('active').fadeIn(800);
        selectedIndex = getSelectedIndex(selectedItem);
        setPagerPosition(selectedIndex);
        window.location.hash = selectedItem;
        return false;
    }

    function getSelectedIndex(selectedItem) {

        pagerItem.removeClass('selected');
        pagerItem.each(function (index) {
            if ($(this).children().attr('href') === selectedItem) {
                $(this).addClass('selected');
                selected = $(this);
                selectedIndex = index;
            }
        });
        return selectedIndex;
    }

    function setPagerPosition(selectedIndex){
        var pagerPosition = 0;

        if(pagerDisplayLimit === 2){
            if(selectedIndex === indexCount){
                pagerPosition = -(selectedIndex * pagerItemWidth - pagerItemWidth);
            }
            else{
                pagerPosition = -(selectedIndex * pagerItemWidth);
            }
        }
        else if(pagerDisplayLimit === 3){
            if(selectedIndex === 0 ){
                pagerPosition = -(selectedIndex * pagerItemWidth);
            }
            else if(selectedIndex === indexCount){
                pagerPosition = -(selectedIndex * pagerItemWidth - 2 * pagerItemWidth);
            }
            else{
                pagerPosition = -(selectedIndex * pagerItemWidth - pagerItemWidth);
            }
        }
        else if(pagerDisplayLimit === 5){
            if(selectedIndex < 2 ){
                pagerPosition = -((selectedIndex * pagerItemWidth) - (selectedIndex * pagerItemWidth));
            }
            else if(selectedIndex >  indexCount - 2){
                pagerPosition = -(selectedIndex * pagerItemWidth - (pagerDisplayLimit - 1 - (indexCount - selectedIndex)) * pagerItemWidth);
            }
            else{
                pagerPosition = -(selectedIndex * pagerItemWidth - 2 * pagerItemWidth);
            }
        }

        $('#pager ul').css({left: pagerPosition});
        setPagerArrow();

    }

    function setPagerArrow(){
        var sliderPosition = null;
        sliderPosition = parseInt(($('#pager ul').css("left")).replace(/px/, ''));

        if(sliderPosition >= 0){
            $('.prev').addClass('inactive');
        }
        else if(sliderPosition === (-(fullPagerWidth - pagerDisplayLimit * pagerItemWidth))){
            $('.next').addClass('inactive');
        }
        else{
            $('.prev').removeClass('inactive');
            $('.next').removeClass('inactive');
        }
    }

    function scrollView(target) {
      $('html,body').animate({
          scrollTop: target.offset().top
      }, 1000);
        return false;
    }

    /*  Activate selected slider and set pager */
     $(document).ready(function (e) {

        initPage(windowWidth);

        menuItem.on('click tap', getSlide);
        pagerItemLink.on('click', getSlide);

         $('.top-link').click(function(){
             scrollView($('.story'));
         })

    });

    //control pager
    $(document).on("click", ".next", function () {
        if(parseInt(pager.css("left")) >= -fullPagerWidth + (pagerDisplayLimit + 1)*85) {
            animating = true;
            pager.animate({left: '-='+pagerItemWidth}, 500, function(){ animating = false;});
        }
        setPagerArrow();
    });

    $(document).on("click", ".prev", function () {
        if(parseInt(pager.css("left")) < 0) {
           animating = true;
           pager.stop().animate({left: '+=' + pagerItemWidth}, 500, function(){ animating = false;});
        }
        setPagerArrow();
    });

    $(".next, .prev").click(function () {
        if (animating) {
            return false;
        }
    });

    //reset variables on window resize
    $(window).resize(function() {
        windowWidth = $(window).width();
        initPage(windowWidth);
    });

 })(jQuery);

