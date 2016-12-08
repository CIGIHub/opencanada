jQuery(document).ready(function() {

  // Animate menu

    $( ".mNav" ).on('touchstart click', this, function() {
        $( ".mNav-menu" ).toggleClass( "closed" );
        $( this ).toggleClass( "hover" );
    });

    $( ".mNav-menu ol a" ).each(function() {
        $(this).on('touchstart click', this, function() {
            $( ".mNav-menu" ).toggleClass( "closed" );
            $( this ).toggleClass( "hover" );
        });
    });
});