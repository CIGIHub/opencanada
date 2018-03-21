jQuery(document).ready(function() {
	
	// This hides the header before the user gets to the bottom
	// As the header overlaps on top of the footer
	$(window).on('scroll', function(){
		if ($(window).scrollTop()  > $(document).height() / 2) {
			$('.heading').hide();
		} else {
			$('.heading').show();
		}
	});
});

