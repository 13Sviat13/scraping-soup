$(document).ready(function () {
    $('scrape_movies_btn').click(function () {
        $.ajax({
            url: '/scrape-shows/',
            type: 'GET',
            success: function (data) {
                alert("Scrapped successfully.");
            },
            error: function (){
                alert('An error occurred while scraping the data.');
            }
        });
    });
});