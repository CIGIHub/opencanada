var Header = Header || {
        Structure: {
            //toggle Banner heading based on window width and page types. This function should only get called when the user scrolls the page and on page load.
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

                if ($(document).scrollTop() >= offset) {

                    //transition from large header to smaller header
                    $('#main-menu').addClass("quickclose");
                    setTimeout(function(){$('#main-menu').removeClass("quickclose") }, 500);
                    collapseHeaderOn();

                } else {
                    collapseHeaderOff();
                }

                if ($('header').hasClass('collapsed')) {
                    Header.Positioning.transparencyOff();
                } else if ($('.jumbotron').length && !$("body").hasClass("template-home-page")) {
                     Header.Positioning.transparencyOn();
                }

                function collapseHeaderOn() {
                    if ($('#article-page').length) {
                        $('header').addClass('article-scroll');
                    } else {
                       $('header').addClass('keep-wordmark');
                    }

                    $('header').addClass('collapsed');
                   
                }

                function collapseHeaderOff() {
                    if ($('#article-page').length) {
                        $('header').removeClass('article-scroll');
                    } else {
                         $('header').removeClass('keep-wordmark');
                    }

                    $('header').removeClass('collapsed');
                    $('#main-menu').removeClass("quickclose");
                }
            }
        }, 
        Positioning: {
            updateHeaderPositioning: function(){
                //set the body padding based on banner height
                var bannerHeight = $('header').height();
                Search.Structure.setOffset(bannerHeight);
                
                if ($('header').hasClass("collapsed") || $(window).width() < breakpoint) {
                    Menu.setOffset(bannerHeight);
                } else {
                    Menu.setOffset(0);
                }
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
