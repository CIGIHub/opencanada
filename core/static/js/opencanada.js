var fullScreen = 992;

jQuery(document).ready(function($) {

    initForWindow();

    $('.fa-camera').click(function () {
        $('.feature-text').fadeToggle();
        $('.feature-image-overlay').fadeToggle();
    });

    //scroll down arrow
    $('a[href*=#]:not([href=#])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            var bannerHeight = $('header').height();
            var scrollDestination = target.offset().top - bannerHeight;
            if (target.length) {
                $('html,body').animate({
                    scrollTop: scrollDestination
                }, 1000);
                return false;
            }
        }
    });

    //drop cap on articles
    $('.story p').first().html(function (index, html) {
        return '<span class="dropcap">' + html.slice(0, 1) + '</span>' + html.slice(1);
    });

    //slide out menu
    $('html').on('touchstart click', function (e) {
        toggleMenu(e);
    });


});

//initialize window based on width and height
function initForWindow(){
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();

    setBodyPadding(windowWidth);
    if($('body').hasClass('template-home-page')){
        setFeatureHeight(windowHeight);
    }

    toggleHeading(windowWidth);

}

//toggle menu in mobile/small window width view
function toggleMenu(e){
    var selected = $(e.target);
    var menu = $('#main-menu');

    console.log(selected);
    if(selected.parent().data("target") == '#main-menu' ){
        if(!(menu.is(':visible'))){
            menu.show().css("left", "-400px").animate({"left":"0px"}).addClass('mobile-menu');
        }
    }
    else{
        menu.animate({"left":"-400px"});
    }
}

//set the Homepage Feature height based on window height
function setFeatureHeight(windowHeight){
    var bannerHeight = $('header').height();
    var featureHeight = windowHeight - bannerHeight;

    $('.jumbotron.feature').css("height", featureHeight + "px");
}

//set the body padding based on banner height
function setBodyPadding(){
    var bannerHeight = $('header').height();
    $('body').css("padding-top", bannerHeight + "px");
}

//toggle Banner heading based on window width and page type
function toggleHeading(windowWidth){

    var offset = $('header').height();

    function fullHeader(scrolled){

        $('header').removeClass('collapsed');
        $('.banner').removeClass('container-fluid').addClass('container');
        $('.logo').addClass('col-md-5').removeClass('col-md-10');
        //$('body').removeClass('article-scroll');
    }

    function collapsedHeader(){
        $('header').addClass('collapsed');
        $('.banner').addClass('container-fluid').removeClass('container');
        $('.logo').removeClass('col-md-5').addClass('col-md-10');
        //if($('#article-page').length){
        //    $('body').addClass('article-scroll');
        //}
    }

    if(windowWidth > fullScreen){

        if(!($('header').hasClass('collapsed'))){
            fullHeader();
        }

        $(window).on("scroll touchmove", function () {
            $('header').toggleClass('collapsed scrolled', $(document).scrollTop() > offset);

            if($('header').hasClass('collapsed')){
                collapsedHeader();
            }
            else{
                fullHeader();
            }
        });
    }
    else{

        collapsedHeader();

        $(window).on("scroll touchmove", function () {
             $('header').toggleClass('scrolled', $(document).scrollTop() > offset);
        });

    }
}

$(window).resize(function(){
    initForWindow()

});


