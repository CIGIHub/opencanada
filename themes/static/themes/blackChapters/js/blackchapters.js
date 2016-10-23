jQuery(document).ready(function() {

    var windowWidth = $(window).width();
    $(window).on('load resize', function(){
        updateReadingBar();
        updateActiveMenuItem();
        windowWidth = $(window).width();
        if($('.quote').length && windowWidth > 992){
            quoteSize();
        }

    });

    $('#mobile-chapter-links').click(function(e) {
        $('#mobile-chapter-links .chapter-links').slideToggle();
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
    
    if($('.reveal').length){
        $(".reveal").mouseenter(function() {
		 $(".background-photo").css('opacity', '1.0');
        }).mouseleave(function () {
		 $(".background-photo").css('opacity', '0.3');
	 });
    }

    function updateReadingBar() {
        var s = $(window).scrollTop(); // Current scroll mark
        ap = $('#article-page').last();
        s = s - ap.position().top; // Start counting at the top of the article
        d = ap.height(); // The end of the article page element
        c = $(window).height(); // Height of the element
        scrollPercent = (s / (d-c)) * 100;
        if (scrollPercent > 100) scrollPercent = 100;
        else if (scrollPercent < 0) scrollPercent = 0;
        $('.readingbar').width(scrollPercent + '%');
    }

    function updateActiveMenuItem() {
       // Get container scroll position
       var fromTop = $(this).scrollTop()+chapterMenuHeight;
    
       // Get id of current scroll item
       var cur = scrollItems.map(function(){
         if ($(this).offset().top < fromTop)
           return this;
       });
       // Get the id of the current element
       cur = cur[cur.length-1];
       var id = cur && cur.length ? cur[0].id : "";
       // Set/remove active class
       menuItems
         .parent().removeClass("active")
         .end().filter("[href='#"+id+"']").parent().addClass("active");
    }


    // Keeping track of position in article to update active page in menu
    var chapterMenu = $(".chapter-links ul"),
        chapterMenuHeight = chapterMenu.outerHeight(),
        // All list items
        menuItems = chapterMenu.find("a"),
        // Anchors corresponding to menu items
        scrollItems = menuItems.map(function(){
          var item = $($(this).attr("href"));
          if (item.length) { return item; }
        });
    
    console.log(menuItems);

    // Bind click handler to menu items
    // so we can get a fancy scroll animation
    menuItems.click(function(e){
      var href = $(this).attr("href"),
          offsetTop = href === "#" ? 0 : $(href).offset().top-chapterMenuHeight+1;
      $('html, body').stop().animate({ 
          scrollTop: offsetTop
      }, 300);
      e.preventDefault();
    });

    // Bind to scroll
    $(window).scroll(function(){
       updateReadingBar();
       updateActiveMenuItem();
    });

});
