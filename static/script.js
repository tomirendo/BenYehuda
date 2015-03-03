var app = angular.module('StarterApp', ['ngMaterial']);

app.controller('AppCtrl', ['$scope', '$mdSidenav', "$http","$window",function($scope, $mdSidenav,$http,$window){
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
$scope.open_piece = function(piece){
    hide_piece();
    $scope.current_piece = piece;
    $scope.current_piece.chapters.forEach(function (chapter_url){
        console.log("Chapter : " + chapter_url)
        $http.get(chapter_url).
             success(function(data, status, headers, config) {
                console.log("Got data " + data);
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

$scope.show_search_bar = function(){
    return $scope.show_translators || $scope.show_creators || $scope.show_pieces;
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


$http.get('http://localhost:8000/api/translator/?format=json').
  success(function(data, status, headers, config) {
    $scope.translators = data;
    // this callback will be called asynchronously
    // when the response is available
  }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

$http.get('http://localhost:8000/api/creator/?format=json').
  success(function(data, status, headers, config) {
    $scope.creators = data;
    // this callback will be called asynchronously
    // when the response is available
  }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });
$http.get('http://localhost:8000/api/piece/?format=json').
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
}]);