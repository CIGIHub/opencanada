var breakpoint = 1000;

//var features = FeatureStyles;
var sharing = Sharing;
var header = Header;
var search = Search;

jQuery(document).ready(function() {

    initForWindow();

    FeatureStyles.Camera.initialize();
    FeatureStyles.Arrow.initialize();
    FeatureStyles.FeatureImages.initialize();
    FeatureStyles.RelatedArticles.initialize();

    search.Structure.initialize();

    sharing.Links.initialize();

    Menu.initialize();
    
});

//initialize window based on width and height
function initForWindow(){

    var windowHeight = $(window).height();
    var windowWidth = $(window).width();

    FeatureStyles.MainFeatures.initializeForWindow(windowHeight);
    sharing.Links.initializeForWindow(windowWidth);
    header.Structure.toggleHeading(windowWidth);

    header.Positioning.updateHeaderPositioning();

    $("main").click(function () {
        Menu.close();
        Search.Structure.closeBox();
        FeatureStyles.MainFeatures.removeNavigationLock();
    });
}

$(window).resize(function(){
    initForWindow();
});

$(window).scroll(function(){
    header.Positioning.updateHeaderPositioning();
});



