var Header = Header || {
        Structure: {
            //toggle Banner heading based on window width and page types
            toggleHeading: function (windowWidth) {

                var offset = $('header').height();

                var bodyTag = $('body');

                function fullHeader() {
                    $('header').removeClass('collapsed');
                    //$('#search-box').removeClass('small-header');
                    $('.toggle-mobile').hide();
                    $('nav').removeClass('mobile-menu open');
                    bodyTag.removeClass('article-scroll');

                    if ($('.template-home-page').length) {
                        $('.tagline').show();
                    }
                }

                function collapsedHeader() {

                    $('header').addClass('collapsed');
                    //$('#search-box').addClass('small-header');
                    $('.toggle-mobile').show();

                    $('nav').addClass('mobile-menu');

                    if ($('#article-page').length && bodyTag.hasClass('article-scroll') && windowWidth <= breakpoint) {
                        bodyTag.removeClass('article-scroll');
                    }
                    if ($('.template-home-page').length) {
                        $('.tagline').hide();
                    }
                }

                function fullScroll() {
                    $('header, #search-box').toggleClass('collapsed scrolled', $(document).scrollTop() > offset);

                    var headerRow = $('header .header-row');
                    if ($('header').hasClass('collapsed')) {
                        //$('#main-menu').hide();
                        collapsedHeader();

                        if ($('#article-page').length) {
                            bodyTag.addClass('article-scroll');
                            headerRow.removeClass('col-md-4');
                        }
                    }
                    else {
                        //$('#main-menu').show();

                        if (!(headerRow.hasClass('col-md-4'))) {
                            headerRow.addClass('col-md-4');
                        }
                        fullHeader();

                    }
                }

                function collapsedScroll() {
                    collapsedHeader();
                    $('header').toggleClass('scrolled', $(document).scrollTop() > offset);
                }

                if (windowWidth >= breakpoint) {

                    if (bodyTag.hasClass('small-article')) {
                        bodyTag.removeClass('small-article');
                    }

                    if ($(document).scrollTop() > offset) {
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

                }
            }
        }


    };
