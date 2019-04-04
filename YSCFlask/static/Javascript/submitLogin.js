$("#loginForm").on("submit", function(event) {

    var obj = $('#loginForm').serializeArray();

    $.ajax({
        type: "POST",
        url: "http://localhost:5000/login",
        data: JSON.stringify(obj),
        contentType : "application/json",
        success: function(data) {
            alert(data);
        }
    });

   return false;
});