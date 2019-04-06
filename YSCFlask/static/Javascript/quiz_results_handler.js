$("#quizForm").on("submit", function(event){
   event.preventDefault(); //this prevents the form to use default submit

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

   $.ajax({
        method: "POST",
        url: $(this).attr("action"), //this will use the form's action attribute
        data: JSON.stringify(weight_list, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(responseData){
        //do something here with responseData
            console.log(responseData)
     }
   });
});