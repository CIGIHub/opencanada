var Menu = Menu || {
        close: function(){
            var menu = $('#main-menu');
            if (menu.hasClass('open')) {
                menu.removeClass('open');
            }
        },
        open: function() {
            var menu = $('#main-menu');

            if (!(menu.hasClass('open'))) {
                Search.Structure.closeBox();
                menu.addClass('open');
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
        }
    };
