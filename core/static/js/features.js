var FeatureStyles = FeatureStyles || {
        MainFeatures: {
            gap_size: {"value": 0.15},
            setSize: function(percentage){
                if (percentage > 0) {
                    FeatureStyles.MainFeatures.gap_size.value = (100 - percentage) / 100.0;
                } else {
                    return 0;
                }
            },
            initializeForWindow: function (windowHeight) {
                var bodyTag = $('body');
                if ((bodyTag.hasClass('template-home-page')
                    || bodyTag.hasClass('template-article-page')
                    || bodyTag.hasClass('template-chaptered-article-page')
                    || bodyTag.hasClass('template-series-page')
                    )
                    && $('.jumbotron').length) {

                    //set the Homepage Feature height based on window height
                    var bannerHeight = $('header').height();
                    var gap = FeatureStyles.MainFeatures.gap_size.value * windowHeight;
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

                    if ( !target.length ) {
                        //not found, so we might be on an template-article-page. Try again.
                        target = selected.closest($('main')).find(".overlay");
                    }
                    
                    target.find($('.feature-text')).fadeToggle();
                    target.find($('.feature-image-overlay')).fadeToggle();
                }

                $('.fa-camera').mouseover(function () {
                    if (!$(this).hasClass("highlighted")) {
                        toggleImage($(this));
                    }
                });

                $('.fa-camera').mouseout(function () {
                    if ($(this).hasClass("highlighted")) {
                        toggleImage($(this));
                    }
                });

                //mobile toggling
                $('.fa-camera').on('touchstart', function (e) {
                        toggleImage($(this));       
                });
            }
        },
        FeatureImages: {
            initialize: function () {
                $('.feature-wrapper').hover(function () {
                    $(this).prev().toggleClass("hover");
                     $(this).toggleClass("hover");
                });
                $('.feature-image').hover(function () {
                    $(this).next().toggleClass("hover");
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
                    $('.related-articles .row > div, #features .row > div, .items .row > div, .graphics .row > div').each( function(i){
                        
                        if (!$(this).hasClass("fadedIn")) {
                            $(this).css('opacity', 0); 
                        }
                        var fifth_of_object = $(this).offset().top + $(this).outerHeight() /5;
                        var bottom_of_window = $(window).scrollTop() + $(window).height();
                        var top_of_object = $(this).offset().top;
                        
                        /* If the object is scrolling to visible in the window, fade it it */
                        if( bottom_of_window > fifth_of_object  || bottom_of_window > top_of_object + 100){  
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
                $(window).load(function () {
                    fadeInContent();
                });

                $(window).resize(function () {
                    fadeInContent();
                });

            }
        },

    };
