// Submit post on submit
$(document).ready(function(){
    $('#watchlist-form').on('submit', function(e){
        event.preventDefault();
        console.log(e);
        update_watchlist();
    });
    $('#comment-form').on('submit', function(){
        event.preventDefault();
        add_comment();
    });
});

function update_watchlist(){
    console.log("updating watchlist...");  // sanity check
    let watchlist = '{{ watchlist }}';
    let listing = '{{ listing }}';
    

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

function add_comment(){
    console.log("adding comment...")  // sanity check
    let watchlist = '{{ watchlist }}';
    let listing = '{{ listing }}';
    let comment = $.trim($("#comment").val());
    

    $.ajax({
        type: "POST",
        url: 'comment_ajax/',
        data:{
            watchlist:watchlist,
            lisitng:listing,
            comment: comment, 
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        datatype:'json',

        // handle a successful response
        success : function(data) {
            if(data['success']){
                let ele = $('<div class=""></div>').text(`${data['user_name']} says: ${comment}`);
                let date_ele = $('<div class=""></div>').text(`${data['current_date']}`);
                $('#comment-form').append(ele).append(date_ele);
                $('#comment').val('');
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