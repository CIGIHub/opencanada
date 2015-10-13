var Search = Search || {
        Structure: {
            initialize: function () {
                $("#search-box").show(); //show search dropdown (offscreen) after everthing is loaded 
            
                $('.search-form input[type=text]').keydown(function () {
                    setTimeout(function() {
                        if ($('.search-form input[type=text]').val() == '') {
                            $('.clear-button').hide();
                        }else {
                            $('.clear-button').show();
                        }
                    }, 100);
                });
                $('.clear-button').click(function () {
                    $('.search-form input[type=text]').val('');
                    $('.clear-button').hide();
                    Search.Structure.focusInput();
                });

                $("#search-box-toggle").click(function () {
                    Search.Structure.toggleBox();
                });

            },
            setOffset: function (offset) {
                $('#search-box').css("top", offset + "px");
            },
            //toggle menu in mobile/small window width view
            closeBox: function(){
                var search = $('#search-box');
                
                if (search.hasClass('open')) {
                    search.removeClass('open');
                    $(".search .button i").removeClass("fa-times").addClass("fa-search");
                }
            },
            openBox: function() {
                var search = $('#search-box');
                
                if (!(search.hasClass('open'))) {
                    Menu.close();
                    search.addClass('open');
                    $(".search .button i").removeClass("fa-search").addClass("fa-times");
                }
            },
            isOpen: function(){
                return $('#search-box').hasClass('open');
            },
            focusInput: function(){
                $('#search-box input').focus();
            },
            toggleBox: function () {
                if (Search.Structure.isOpen()) {
                    Search.Structure.closeBox();
                    $("#search-box-toggle").removeClass("open");
                }
                else {
                    Search.Structure.openBox();
                    Search.Structure.focusInput();
                    $("#search-box-toggle").addClass("open");
                }
            }
        }
    };

