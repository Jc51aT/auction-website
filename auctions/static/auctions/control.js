// Submit post on submit
$(document).ready(function(){
    $('#watchlist-form').on('submit', function(e){
        event.preventDefault();
        console.log(e);
        update_watchlist();
    });
});

function update_watchlist(){
    console.log("updating watchlist...")  // sanity check
    let watchlist = '{{ watchlist }}';
    let listing = '{{ listing }}';
    //let url = "watchlist_ajax/";
    $.ajax({
        type: "POST",
        url: 'watchlist_ajax/',
        data:{
            watchlist:watchlist,
            lisitng:listing, 
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        datatype:'json',

        // handle a successful response
        success : function(data) {
            if(data['success']){
                $('#watchlist-form').remove();
                let ele = $('<span class="badge badge-pill badge-info"></span>').text("On Watchlist");
                $('#listing_title').append(ele);
                console.log(data); // log the returned json to the console
                console.log("success"); // another sanity check
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}