
$(document).on("click", "#submit_quiz", function() {
    var attribute_list = "walkability, " + "transit, " + "bikeability, " + "pop_density, " + "metro_population, " + "prop_crime, " +
                         "violent_crime, " + "air_pollution, " +  "traffic, " + "sunshine";

    var weight_list =  $("#walkability").val() + ", " +
                       $("#transit").val() + ", " +
                       $("#bikeability").val() + ", " +
                       $("#pop_density").val() + ", " +
                       $("#metro_population").val() + ", " +
                       $("#prop_crime").val() + ", " +
                       $("#violent_crime").val() + ", " +
                       $("#air_pollution").val() + ", " +
                       $("#traffic").val() + ", " +
                       $("#sunshine").val();

    var list_of_cities = []
    $.get("/handle_quiz_submission",{'attribute_list[]': attribute_list, 'weight_list[]': weight_list}, function(returned_data){
          var test = returned_data;


    });

});