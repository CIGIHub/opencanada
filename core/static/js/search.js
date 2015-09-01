var Search = Search || {
        Structure: {
            initialize: function () {
                $('.search-form input[type=text]').keydown(function () {
                    if ($(this).val() != '') {
                        $('.clear-button').show();
                    }
                });
                $('.clear-button').click(function () {
                    $('.search-form input[type=text]').val('');
                    $('.clear-button').hide();
                    Search.Structure.focusInput();
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
                }
            },
            openBox: function() {
                var search = $('#search-box');

                if (!(search.hasClass('open'))) {
                    Menu.close();
                    search.addClass('open');
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
                }
                else {
                    Search.Structure.openBox();
                    Search.Structure.focusInput();
                }
            }
        }


    };

