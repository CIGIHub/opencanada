var FeatureStyles = FeatureStyles || {
        MainFeatures: {
            initializeForWindow: function (windowHeight) {
                var bodyTag = $('body');
                if ((bodyTag.hasClass('template-home-page'))
                    || (bodyTag.hasClass('template-article-page')
                    || (bodyTag.hasClass('template-chaptered-article-page')
                    )
                    && $('.jumbotron').length)) {

                    //set the Homepage Feature height based on window height
                    var bannerHeight = $('header').height();
                    var gap = 0.15 * windowHeight;
                    var featureHeight = windowHeight - bannerHeight - gap;

                    $('.jumbotron.main-feature').css("height", featureHeight + "px");

                }
            }
        },
        Camera: {
            initialize: function () {
                
                function toggleImage(element){
                    var selected = element;

                    selected.toggleClass('highlighted');
                    var target = selected.closest($('.overlay'));

                    target.find($('.feature-text')).fadeToggle();
                    target.find($('.feature-image-overlay')).fadeToggle();
                }

                $('.camera').hover(function () {
                    toggleImage($(this));
                },
                function () {
                    //user could click, which would flip the toggle. So only toggle back on if its off.
                    if ($(this).hasClass("highlighted")) {
                        toggleImage($(this));
                    }
                });

                $('.template-article-page .fa-camera').hover(function(){
                    $('.feature-text').fadeToggle();
                    $('.feature-image-overlay').fadeToggle();
                });

                $('.camera').click(function () {
                        toggleImage($(this));         
                });

                $('.template-article-page .fa-camera').click(function(){
                    toggleImage($(this));
                });
            }
        },
        FeatureImages: {
            initialize: function () {
                $('.feature-wrapper').hover(function () {
                    $(this).prev().addClass("hover");
                },
                function () {
                    $(this).prev().removeClass("hover");
                });

                
            }
        },
        Arrow: {
            initialize: function(){
                //scroll down arrow
                $('a[href*=#]:not([href=#])').click(function () {
                    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                        if($(this).attr('href') == '#features'){
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
                    }
                });
            }
        },
        RelatedArticles: {
            initialize: function () {
                

                function fadeInContent() {
                   /* Check the location of each desired element */
                    $('.related-articles .row > div, #features .row > div, .readings .row > div, .graphics .row > div').each( function(i){
                        
                        if (!$(this).hasClass("fadedIn")) {
                            $(this).css('opacity', 0); 
                        }
                        var third_of_object = $(this).offset().top + $(this).outerHeight() /3;
                        var bottom_of_window = $(window).scrollTop() + $(window).height();
                        var top_of_object = $(this).offset().top;
                        
                        /* If the object is scrolling to visible in the window, fade it it */
                        if( bottom_of_window > third_of_object  || bottom_of_window > top_of_object + 200){  
                            $(this).animate({'opacity':'1'},400); 
                            $(this).addClass("fadedIn");        
                        }   
                    });  
                }
                /* Every time the window is scrolled ... */
                $(window).scroll( function(){
                    fadeInContent();
                });

                //if you refesh, you could be down the page, and the featured articles would be hidden. 
                //Do a check and display any articles that the user can see.
                jQuery(window).load(function () {
                    fadeInContent();
                });

            }
        },

    };
