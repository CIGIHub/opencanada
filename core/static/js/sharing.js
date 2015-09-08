var Sharing = Sharing || {
        Links: {
            initialize: function () {

                function social_setup(){
                    window.fbAsyncInit = function () {
                        FB.init({
                            appId: '1209700165722055',
                            xfbml: true,
                            version: 'v2.4'
                        });
                    };

                    (function (d, s, id) {
                        var js, fjs = d.getElementsByTagName(s)[0];
                        if (d.getElementById(id)) {
                            return;
                        }
                        js = d.createElement(s);
                        js.id = id;
                        js.src = "//connect.facebook.net/en_US/sdk.js";
                        fjs.parentNode.insertBefore(js, fjs);
                    }(document, 'script', 'facebook-jssdk'));

                    $(".facebook-share-link").click(function () {
                        var href = $(this).data('url');
                        FB.ui(
                            {
                                method: 'share',
                                href: href
                            }, function (response) {
                            });
                    });
                }

                if ($(".facebook-share-link").length > 0) {
                    social_setup();
                }
            },
            initializeForWindow: function () {
                if ($("article > .title").children().hasClass("primary-topic")) {

                    if (windowWidth > breakpoint) {
                        $('ul.share-links').addClass("below-topic");
                    }
                    else {
                        $('ul.share-links').removeClass("below-topic");
                    }
                }

            }
        }

    };
