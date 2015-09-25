var Menu = Menu || {
        initialize: function () {
            $("#toggle-mobile").click(function () {
                Menu.toggle();
            });
        },
        close: function(){
            var menu = $('#main-menu');
            if (menu.hasClass('open')) {
                menu.removeClass('open');
                //FeatureStyles.MainFeatures.removeNavigationLock();
            }
        },
        open: function() {
            var menu = $('#main-menu');

            if (!(menu.hasClass('open'))) {
                Search.Structure.closeBox();
                menu.addClass('open');
                //FeatureStyles.MainFeatures.addNavigationLock();
            }
        },
        isOpen: function(){
            return $('#main-menu').hasClass('open');
        },
        toggle: function () {
            if (Menu.isOpen()) {
                Menu.close();
            }
            else {
                Menu.open();
            }
        },
        setOffset: function (offset) {
            if (offset == 0) {
                $('#main-menu').css("top", "");
            } else {
                $('#main-menu').css("top", offset + "px");
            }
        },

        quickClose: function() {
            $('#main-menu').addClass("quickclose");
            setTimeout(function(){$('#main-menu').removeClass("quickclose") }, 500);
        },

        quickOpen: function() {
            $('#main-menu').addClass("quickopen");
            setTimeout(function(){$('#main-menu').removeClass("quickopen") }, 500);
        }
    };
