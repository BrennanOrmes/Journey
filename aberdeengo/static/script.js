$("#profile").click(function(event) {
    event.preventDefault();
    var target = $(this).attr("data");
    $("#main-content").load(target, function() {
         
    });
});

$("#interests").click(function(event) {
    event.preventDefault();
    var target = $(this).attr("data");
    $("#main-content").load(target, function() {
        
    });
});

$("#events").click(function(event) {
    event.preventDefault();
    var target = $(this).attr("data");
    $("#main-content").load(target, function() {
         
    });
});