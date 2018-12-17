$(function () {
    $("#filter").click(function () {
        let minAge = $("#min_age").val();
        let maxAge = $("#max_age").val();
        let gender = $("#gender").val();
        console.log("min : " + minAge + "\n" + "max : " + maxAge + "\n" + "gender : " + gender + "\n");
        $.ajax({
            url: "/filtering",
            dataType: "json",
            data: {
                minAge: minAge,
                maxAge: maxAge,
                gender: gender
            },
            success: function (data) {
                removeMatches();

                $.each(data, function (index, dict) {
                    let image = dict["image"];
                    let username = dict["username"];
                    let email = dict["email"];
                    let hobbies = dict["hobbies"];
                    let age = dict["age"];
                    let hobbies_list ="";
                    for (x in hobbies){
                        hobbies_list = hobbies_list +  "<li>" + hobbies[x] + "</li>";
                    }
                    $("#list").append(
                        "<div class=\"matched_user row\">\n" +
                        "                <div class=\"user media\" id=\" "+ username + " \">\n" +
                        "                    <img class=\"rounded-circle account-img\" src=\""+ image + "\">\n" +
                        "                </div>\n" +
                        "                    <h3 class=\"account-heading\">"+ username + "</h3>\n" +
                        "                    <h5 class=\"email text-secondary\">"+ email + "</h5>\n" +
                        "                    <ol>\n" + hobbies_list +
                        "                    </ol>\n" +
                        "                    <h6 class=\"age\"> Age : "+ age + "</h6>\n" +
                        "                </div>"
                    );
                });
            },
            error: function () {
                console.log("filter error");
            }
        });
    });
    function removeMatches() {
        $(".matched_user").remove();
    }
});