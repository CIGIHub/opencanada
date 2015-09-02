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
                    var gap = 0.05 * windowHeight;
                    var featureHeight = windowHeight - bannerHeight - gap;

                    $('.jumbotron.main-feature').css("height", featureHeight + "px");

                }
            }
        },
        Camera: {
            initialize: function () {
                $('.camera').hover(function () {
                    var selected = $(this);

                    selected.toggleClass('highlighted');
                    var target = selected.closest($('.overlay'));

                    target.find($('.feature-text')).fadeToggle();
                    target.find($('.feature-image-overlay')).fadeToggle();
                });

                $('.template-article-page .fa-camera').hover(function(){
                    $('.feature-text').fadeToggle();
                    $('.feature-image-overlay').fadeToggle();
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
                
                /* Every time the window is scrolled ... */
                $(window).scroll( function(){
                
                    /* Check the location of each desired element */
                    $('.related-articles .row > div').each( function(i){
                        
                        var bottom_of_object = $(this).offset().top + $(this).outerHeight();
                        var bottom_of_window = $(window).scrollTop() + $(window).height();
                        
                        /* If the object is completely visible in the window, fade it it */
                        if( bottom_of_window > bottom_of_object ){  
                            $(this).animate({'opacity':'1'},400);        
                        }   
                    }); 
                });

            }
        },

    };
