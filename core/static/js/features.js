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
            initializeForWindow: function () {
                var bodyTag = $('body');
                var windowHeight = $(window).height();

                if ((bodyTag.hasClass('template-home-page')
                    || bodyTag.hasClass('template-article-page')
                    || bodyTag.hasClass('template-series-page')
                    )
                    && $('.main-feature').length) {

                    //set the Homepage Feature height based on window height
                    var bannerHeight = $('header').height();
                    var gap = FeatureStyles.MainFeatures.gap_size.value * windowHeight;
                    var featureHeight = windowHeight - gap;

                    $('.main-feature').css("height", featureHeight + "px");

                    $('.main-feature').css("margin-top", -1 * $('header').height());

                    if (bodyTag.hasClass('template-home-page')) {
                        featureHeight = windowHeight - bannerHeight - gap;
                        $('.main-feature').css("height", featureHeight + "px");
                        $('.main-feature').css("margin-top", 0 + "px");
                    }

                }
            },
            addNavigationLock: function() {
                $("body").addClass("navigation-lock");
                $("html").addClass("navigation-lock");
            },
            removeNavigationLock: function() {
                $("body").removeClass("navigation-lock");
                $("html").removeClass("navigation-lock");
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

                    target.find($('.editors-pick-link')).fadeToggle();
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
                $('.overlay-feature .editors-pick-link, .overlay-feature .most-popular').hover(function () {
                    $(this).prev().toggleClass("hover"); //feature-wrapper
                    $(this).prev().prev().toggleClass("hover"); //feature-image
                });

            }
        },
        ImageFeature: {
            initialize: function () {
                //$('.image-feature figure a, .image-feature h3 a, .image-feature .editors-pick-link, .image-feature .most-popular').hover(function () {
                //    $(this).prev(".image-feature").find("figure a").toggleClass("hover");
                //    $(this).closest(".image-feature").find("h3 a").toggleClass("hover");
                //});
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
                    $('main .container .row , main .container-full-bleed .row ').each( function(i){
                        var windowWidth = $(window).width();
                        var windowHeight = $(window).height();
                        var top_of_object = $(this).offset().top; // Get the `top` of this `li`


                        // Check if this element is in the interested viewport
                        if (windowWidth >= breakpoint && !$(this).hasClass("fadedIn")) {
                            if (top_of_object < windowHeight) {
                                $(this).css('opacity', '1');
                                $(this).addClass("fadedIn");
                            }
                            else {
                                $(this).css('opacity', '0');
                            }
                        }else if (windowWidth < breakpoint) {
                            $(this).css('opacity', 1);
                        }

                        var fifth_of_object = $(this).offset().top + $(this).outerHeight() /5;
                        var bottom_of_window = $(window).scrollTop() + $(window).height();

                        //console.log('top offset: ' + $(this).offset().top);
                        //console.log('scrolltop: ' + $(window).scrollTop());

                        /* If the object is scrolling to visible in the window, fade it in */
                        if( bottom_of_window > fifth_of_object  || bottom_of_window > top_of_object + 40){
                            $(this).animate({'opacity':'1'}, 400);
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
        EndNotes:{
            initialize: function(){
                $(".endnote-link").each(function(index, elem){
                    reference_id = $(elem).data("reference");
                    label_text = $("#" + reference_id + " .identifier");
                    $(elem).text(label_text.text());
                })
            }
        }

    };
