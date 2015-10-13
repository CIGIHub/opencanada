var Menu = Menu || {
        initialize: function () {

            $("#main-menu").show(); //show main menu after everthing is loaded 
            $("#toggle-mobile").click(function () {
                Menu.toggle();
            });
        },
        close: function(){
            var menu = $('#main-menu');
            if (menu.hasClass('open')) {
                menu.removeClass('open');
                $("#toggle-mobile").removeClass("open");
            }
        },
        open: function() {
            var menu = $('#main-menu');

            if (!(menu.hasClass('open'))) {
                Search.Structure.closeBox();
                menu.addClass('open');
                $("#toggle-mobile").addClass("open");
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
        noAnimation: function() {
            $('#main-menu').addClass("noAnimation");
            setTimeout(function(){$('#main-menu').removeClass("noAnimation") }, 500);
        }
    };
