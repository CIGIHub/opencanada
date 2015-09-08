var breakpoint = 1000;

var windowHeight = $(window).height();
var windowWidth = $(window).width();

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

    FeatureStyles.MainFeatures.initializeForWindow(windowHeight);
    sharing.Links.initializeForWindow();
    header.Structure.toggleHeading();

    header.Positioning.updateHeaderPositioning();

    $("main").click(function () {
        Menu.close();
        Search.Structure.closeBox();
        FeatureStyles.MainFeatures.removeNavigationLock();
    });
}

$(window).resize(function(){
    initForWindow();
    windowHeight = $(window).height();
    windowWidth = $(window).width();
    
});

$(window).scroll(function(){
    header.Positioning.updateHeaderPositioning();
});



