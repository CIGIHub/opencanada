jQuery(document).ready(function($){

    $('.fa-camera').click(function(){
        $('.feature-text').fadeToggle();
        $('.feature-image-overlay').fadeToggle();
    });

    //$('a[href^="#feature"]').on('click',function (e) {
	//    e.preventDefault();
    //
	//    var target = this.hash;
	//    var $target = $(target);
    //
	//    $('html, body').stop().animate({
	//        'scrollTop': $target.offset().top
	//    }, 900, 'swing', function () {
	//        window.location.hash = target;
	//    });
	//});

    $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});