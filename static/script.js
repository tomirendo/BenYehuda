var app = angular.module('StarterApp', ['ngMaterial']);

app.controller('AppCtrl', ['$scope', '$mdSidenav', "$http","$window",'$mdDialog',function($scope, $mdSidenav,$http,$window,$mdDialog){
  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };
  $scope.messages = [
       { date : "2015-02-10",
    title : "פתיחת האתר החדש של פרויקט בן יהודה",
    text : "ברוכים הבאים לאתר החדש של פרויקט בן יהודה.\nיש חיפוש חדש ועוד המון דברים מגניבים!"},
   { date : "2015-02-10",
    title : "פתיחת האתר החדש של פרויקט בן יהודה",
    text : "ברוכים הבאים לאתר החדש של פרויקט בן יהודה.\nיש חיפוש חדש ועוד המון דברים מגניבים!"},
   { date : "2015-02-10",
    title : "פתיחת האתר החדש של פרויקט בן יהודה",
    text : "ברוכים הבאים לאתר החדש של פרויקט בן יהודה.\nיש חיפוש חדש ועוד המון דברים מגניבים!"},
   { date : "2015-02-10",
    title : "פתיחת האתר החדש של פרויקט בן יהודה",
    text : "ברוכים הבאים לאתר החדש של פרויקט בן יהודה.\nיש חיפוש חדש ועוד המון דברים מגניבים!"},
   { date : "2015-02-10",
    title : "פתיחת האתר החדש של פרויקט בן יהודה",
    text : "ברוכים הבאים לאתר החדש של פרויקט בן יהודה.\nיש חיפוש חדש ועוד המון דברים מגניבים!"},
   { date : "2015-02-10",
    title : "פתיחת האתר החדש של פרויקט בן יהודה",
    text : "ברוכים הבאים לאתר החדש של פרויקט בן יהודה.\nיש חיפוש חדש ועוד המון דברים מגניבים!"},
    { date : "2015-02-10",
    title : "פתיחת האתר החדש של פרויקט בן יהודה",
    text : "ברוכים הבאים לאתר החדש של פרויקט בן יהודה.\nיש חיפוש חדש ועוד המון דברים מגניבים!"}];
var show_nothing = function(){
    $scope.show_news = false;
    $scope.show_creators = false;
    $scope.show_translators = false;
    $scope.show_piece= false;
    $scope.show_pieces= false;
    $scope.show_single_creator= false;
    $scope.search_bar = "";
    hide_piece();
}
function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}
var hide_piece = function(){
        $scope.piece_show_side_nav = false;
        $scope.piece_show_progress_bar = true;
        $scope.current_chapter = "";
    $scope.current_chapters = [];
}
var check_chapters_status = function(){
    console.log($scope.current_chapters.length == $scope.current_piece.chapters.length);
    if ($scope.current_chapters.length == $scope.current_piece.chapters.length){
        sortByKey($scope.current_chapters,"index");
        $scope.piece_show_progress_bar = false;
        $scope.piece_show_side_nav = true;
        $scope.current_chapter = $scope.current_chapters[0];
    } else{
    }
};

$scope.present_news = function(){
    show_nothing();
    $scope.show_news = true;
};
$scope.present_creators = function(){
    show_nothing();
    $scope.show_creators = true;
    $mdSidenav('left').toggle()
};
$scope.present_translators = function(){
    show_nothing();
    $scope.show_translators = true;
    $mdSidenav('left').toggle()
};
$scope.present_pieces = function(){
    show_nothing();
    $scope.show_pieces = true;
    $mdSidenav('left').toggle()
};
$scope.present_piece= function(){
    show_nothing();
    $scope.show_piece= true;
};
$scope.present_single_creator = function(){
    show_nothing();
    $scope.show_single_creator = true;
};
$scope.open_piece = function(piece){
    hide_piece();
    $scope.current_piece = piece;
    $scope.current_piece.chapters.forEach(function (chapter_url){
        console.log("Chapter : " + chapter_url)
        $http.get(chapter_url).
             success(function(data, status, headers, config) {
                $scope.current_chapters.push(data);
                check_chapters_status();
              }).
            error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
    $scope.present_piece();
    });

};

$scope.show_chapter = function(chapter){
    $scope.current_chapter = chapter;
    $mdSidenav('left').toggle()
};

$scope.present_news();
$scope.current_piece = null;
$scope.current_chapters = [];
$scope.translators = [];
$scope.creators = [];
$scope.pieces= [];
$scope.piece_show_progress_bar= true;
$scope.current_chapter = "";
$scope.piece_show_side_nav = false;
$scope.search_bar = "";
$scope.pop_up_search_bar = "asdkjadkj";
$scope.selected_creator = null;

$scope.select_creator = function(creator){
    console.log("Selecting Creator : " + creator)
    if (creator.id){
      creator.pk = creator.id;
    }
    $scope.selected_creator = {creator : creator, pieces : [],scope : $scope};
    $http.get('/api/piece/?creator='+creator.pk+'&format=json').
  success(function(data, status, headers, config) {
    $scope.selected_creator.pieces = data;
    // this callback will be called asynchronously
    // when the response is available
  }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });
    $scope.present_single_creator();
};

$http.get('/api/translator/?format=json').
  success(function(data, status, headers, config) {
    $scope.translators = data;
    // this callback will be called asynchronously
    // when the response is available
  }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

$http.get('/api/creator/?format=json').
  success(function(data, status, headers, config) {
    $scope.creators = data;
    // this callback will be called asynchronously
    // when the response is available
  }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });
$http.get('/api/piece/?format=json').
  success(function(data, status, headers, config) {
    $scope.pieces= data;
    // this callback will be called asynchronously
    // when the response is available
  }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

$scope.open_url = function(url){

    $window.open(url);
};
var global_scope=$scope; //Alias for inside other objects
$scope.showAdvanced = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: 'search_dialog.html',
      targetEvent: ev,
    })
    .then(function(answer) {
    //
    }, function() {
    //
    });
  };
function DialogController($scope, $mdDialog) {
  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
  $scope.search_bar = global_scope.search_bar;
  $scope.global_scope = global_scope;
  $scope.results = [];

  $scope.submit = function(search_term){
    $scope.results = [];
    $scope.show_load_bar = true;
    global_scope.search_bar = $scope.search_bar;

    $http.get("/api/search_solr/"+search_term+"/").
    success(function(data, status, headers, config) {
    $scope.results= data.response.docs;
    $scope.show_load_bar = false;

    // this callback will be called asynchronously
    // when the response is available
    }).
    error(function(data, status, headers, config) {
    $scope.show_load_bar = false;
    // called asynchronously if an error occurs
    // or server returns response with an error status.
    });
  };

  $scope.submit($scope.search_bar);
};
}]).directive("singleCreator",function(){
    return {
        restrict : "E",
        scope : {
            creator_info : "=info"
        },
        templateUrl : "creator-view.html",

    };
});