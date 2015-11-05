var Sharing = Sharing || {
        Links: {
            initialize: function () {
                function ga_track(socialNetwork, socialAction, socialTarget) {
                    window.ga && ga('send', 'social', socialNetwork, socialAction, socialTarget);
                };

                function social_setup() {
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
                        ga_track('facebook', 'share', href);
                        FB.ui(
                            {
                                method: 'share',
                                href: href
                            }, function (response) {
                            });
                    });
                }

                function load_share_counts(page_id) {
                    $.getJSON('/core/share/count/' + page_id, function (data) {
                        $.each(data, function (key, val) {
                            if (val > 0){
                                var social_count = $("." + key + " .count");
                                if (social_count.length > 0) {
                                    social_count.text(val);
                                }
                            }
                        });
                    });
                }

                if ($(".facebook-share-link").length > 0) {
                    social_setup();
                }

                $('.share-links .twitter a').on('click', function(e) {
                  ga_track('twitter', 'share', $('body').data('page-url'));
                });

                var sharables = $(".tweet");
                if (sharables.length > 0){
                    sharables.click(function(){
                        var text = $(this).data('text');
                        var url = $('body').data('page-url');
                        var share_url = "https://twitter.com/share?text=" + text + "&url=" + url;
                        ga_track('twitter', 'share', url);
                        window.open(share_url);
                    });
                }

                var share_links = $(".share-links");
                if (share_links.length > 0) {
                    var page_id = share_links.data('page-id');
                    load_share_counts(page_id);
                }
            },
            initializeForWindow: function () {
                if (($("article").length > 0) && ($(".main-feature").length > 0)) {
                    if ($(window).width() >= breakpoint) {
                        $('ul.share-links').addClass("below-feature");
                    }
                    else {
                        $('ul.share-links').removeClass("below-feature");
                    }
                }

            }

        }

    };
