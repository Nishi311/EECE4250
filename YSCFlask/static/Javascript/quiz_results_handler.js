
$(document).on("click", "#submit_quiz", function() {
    var attribute_list = "walkability, " + "public_trans, " + "biking, " + "pop_density, " + "city_size, " + "prop_crime, " +
                         "violent_crime, " + "air_pol, " +  "car_traffic, " + "sunshine";

    var weight_list =  $("#walkability").val() + ", " +
                       $("#public_trans").val() + ", " +
                       $("#biking").val() + ", " +
                       $("#pop_density").val() + ", " +
                       $("#city_size").val() + ", " +
                       $("#prop_crime").val() + ", " +
                       $("#violent_crime").val() + ", " +
                       $("#air_pol").val() + ", " +
                       $("#car_traffic").val() + ", " +
                       $("#sunshine").val();

    var list_of_cities = []
    $.get("/handle_quiz_submission",{'attribute_list[]': attribute_list, 'weight_list[]': weight_list}, function(returned_data){
          var test = returned_data;


    });

});