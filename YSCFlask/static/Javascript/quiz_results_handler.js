
$(document).on("click", "#submit_quiz", function() {
    var attribute_list = "walkability, " + "bikeability, " + "transit, "+ "traffic, " + "metro_pop, " + "pop_density, " +
                         "prop_crime, " + "violent_crime, " + "air_pollution, " +  "sunshine";

    var weight_list =  $("#walkability").val() + ", " +
                       $("#bikeability").val() + ", " +
                       $("#transit").val() + ", " +
                       $("#traffic").val() + ", " +
                       $("#metro_pop").val() + ", " +
                       $("#pop_density").val() + ", " +
                       $("#prop_crime").val() + ", " +
                       $("#violent_crime").val() + ", " +
                       $("#air_pollution").val() + ", " +
                       $("#sunshine").val();

    var list_of_cities = []
    $.get("/handle_quiz_submission",{'attribute_list[]': attribute_list, 'weight_list[]': weight_list}, function(returned_data){
          var test = returned_data;
          var test2 = "Doing this for the break point"

    });

});