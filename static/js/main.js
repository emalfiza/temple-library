$(document).ready(function () {
    /* Mobile Navigation Class */
    $('.sidenav').sidenav();
});

     // searching for book info using ISBN
        $(function(){
            $('#searchIsbn').click(function(){

                // disable the button until response
                $(this).attr("disabled", "disabled");

                $.ajax({
                    url: '/search_isbn',
                    data: $('form').serialize(),
                    type: 'POST',
                    success: function(response){

                        if(response !== "null") {
                            // convert the response to a valid JSON Object
                            let bookInfo = JSON.parse(response);
                            $("#book_name").val(bookInfo["volumeInfo"]["title"]);
                            $("#book_writer").val(bookInfo["volumeInfo"]["authors"]);
                            $("#book_genre").val(bookInfo["volumeInfo"]["categories"]);
                            $("#description").val(bookInfo["volumeInfo"]["description"]);
                            $("#book_cover").val(bookInfo["volumeInfo"]["imageLinks"]["thumbnail"]);

                        } else {
                            // display the error message
                            alert("Sorry, no data were found!");
                        }

                        // enable the button again
                        $('#searchIsbn').removeAttr("disabled");
                    },
                    error: function(error){

                        // display the error message
                        alert(error);

                        // enable the button again
                        $('#searchIsbn').removeAttr("disabled");
                    }
                });

            });
        });