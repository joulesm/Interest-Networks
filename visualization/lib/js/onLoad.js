jQuery(document).ready(function() {
    // initialize the dropdown menu js
    $('.dropdown-toggle').dropdown();

    // initialize jqm
    $('.jqmWindow').jqm();
    $('#showprojectinfo').click(function() { $('#projectinfo').jqmShow(); });
    $('#showlegend').click(function() { $('#legend').jqmShow(); });

    $('#projectinfo').jqmShow();

    // get the list of all interests from a json file
    var interests = [];

    $.getJSON('temp/interestslist.json', function(data) {
        $.each(data, function(key, val) {
            interests.push(val);
        });
    });

    // put that list as the suggested terms for the search box
    $('#search').typeahead({
        source: interests
    });

    // what happens when you press enter on the search box
    $("#search").keypress(function(event) {
        // if it was an enter
        if(event.keyCode == 13) {
            // prevent the form from sending itself
            event.preventDefault();

            // find the node associated with that
            var searchValue = $("#search").attr("value");
            var searchedNode = vis.select("g[name='" + searchValue + "']")
            // pretend like you just clicked on it
            onClickNode(searchedNode);
            
            // clear the box
            $("#search").attr("value", "");
        }
    });
});