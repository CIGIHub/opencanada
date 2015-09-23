var Header = Header || {
        Structure: {
            //toggle Banner heading based on window width and page types. This function should only get called when the user scrolls the page.
            toggleHeading: function () {

                /* There are many ways the header needs to be altered after loading
                 *  1.  Start the header loaded for mobile, and use CSS to show/hide depending on screen size
                 *  2.  When the user scrolls down past the big image (or page title if no big image), collapse the header
                 *  3.  On the homepage, there is a tagline which needs to hidden once the header is collapsed 
                 *  4.  Full bleed articles need to hide the header altogether, and just show a transparent OpenCanda.org. When the user
                        scrolls down past the big image, the header needs to reappear in a collapsed state.
                 *  5.  Scrolling down on article pages (on large screens only) need to replace the OpenCanada.org with the article title  
                 *  6.  Change the background from red to black when user scrolls down.
                */
                var offset = Math.max($('header').height(), $('.jumbotron.main-feature').height());

                var bodyTag = $('body');

                if ($(window).width() > breakpoint) {

                }

                /*function fullHeader() {
                    $('header').removeClass('collapsed');
                    $('.toggle-mobile').hide();
                    //$('nav').removeClass('mobile-menu open');
                    bodyTag.removeClass('article-scroll');

                    if ($('.template-home-page').length) {
                        $('.tagline').show();
                    }
                }

                function collapsedHeader() {

                    $('header').addClass('collapsed');
                    if (!$('header').hasClass("transparency")) {
                        $('.toggle-mobile').show();
                    }

                    //$('nav').addClass('mobile-menu');

                    if ($('#article-page').length && bodyTag.hasClass('article-scroll') && $(window).width() <= breakpoint) {
                        bodyTag.removeClass('article-scroll');
                    }
                    if ($('.template-home-page').length) {
                        $('.tagline').hide();
                    }
                }

                function fullScroll() {
                    $('header, #search-box').toggleClass('collapsed scrolled', $(document).scrollTop() >= offset);

                    if ($('header').hasClass('scrolled')) {
                        Header.Positioning.transparencyOff();
                    }else if ($('.jumbotron').length && !$("body").hasClass("template-home-page")) {
                         Header.Positioning.transparencyOn();
                    }

                    var headerRow = $('header .header-row');
                    if ($('header').hasClass('collapsed')) {
                        collapsedHeader();

                        if ($('#article-page').length) {
                            bodyTag.addClass('article-scroll');
                            headerRow.removeClass('col-md-4');
                        }
                    }
                    else {
                        if (!(headerRow.hasClass('col-md-4'))) {
                            headerRow.addClass('col-md-4');
                        }
                        fullHeader();

                    }
                }

                function collapsedScroll() {
                    collapsedHeader();

                    $('header').toggleClass('scrolled', $(document).scrollTop() >= offset);
                    if ($('header').hasClass('scrolled')) {
                        Header.Positioning.transparencyOff();
                    }else if ($('.jumbotron').length && !$("body").hasClass("template-home-page")) {
                         Header.Positioning.transparencyOn();
                    }

                }

                if ($(window).width() >= breakpoint) {

                    if (bodyTag.hasClass('small-article')) {
                        bodyTag.removeClass('small-article');
                    }

                    if ($(document).scrollTop() >= offset) {
                        if ($('#article-page').length) {
                            bodyTag.addClass('article-scroll');
                        }
                        collapsedHeader();
                    }
                    else {
                        fullHeader();
                    }

                    $(window).off("scroll touchmove", collapsedScroll);
                    $(window).on("scroll touchmove", fullScroll);

                }
                else {
                    var articlePage = $('#article-page');
                    if (articlePage.length && bodyTag.hasClass('article-scroll')) {
                        bodyTag.removeClass('article-scroll');
                    }
                    if (articlePage.length) {
                        bodyTag.addClass('small-article');
                    }
                    collapsedHeader();

                    $(window).off("scroll touchmove", fullScroll);
                    $(window).on("scroll touchmove", collapsedScroll);

                }*/
            }
        }, 
        Positioning: {
            updateHeaderPositioning: function(){
                //set the body padding based on banner height
                var bannerHeight = $('header').height();
                Search.Structure.setOffset(bannerHeight);
                Menu.setOffset(bannerHeight);
                $('body').css("padding-top", bannerHeight + "px");
            },

            transparencyOn: function() {
                $('header').addClass("transparency");
                $('#toggle-mobile').hide();
                $('#search-box-toggle').hide();
                $('#main-menu').hide();
            },

            transparencyOff: function() {
                $('header').removeClass("transparency");
                $('#toggle-mobile').show();
                $('#search-box-toggle').show();
                $('#main-menu').show();
            }
        }

    };
