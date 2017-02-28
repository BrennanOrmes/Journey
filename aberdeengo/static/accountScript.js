$("#profile").click(function(event) {
    var target = $(this).attr("data");
    $("#main-content").load(target, function() {
         
    });
});

$("#interests").click(function(event) {
    var target = $(this).attr("data");
    $("#main-content").load(target, function() {
        
    });
});

$("#events").click(function(event) {
    var target = $(this).attr("data");
    $("#main-content").load(target, function() {
         
    });
});



$(document).ready(function() {
 var target = $("#profile").attr("data");
    $("#main-content").load(target, function() {
    });
});