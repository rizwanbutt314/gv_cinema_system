$(document).ready(function () {

    $('.search-term').keyup(function () {
        getMovies(this.value);
    });


    var getMovies = function (searchVal) {
        var url = '/api/movies';
        if (searchVal)
            url += '?search=' + searchVal;

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (res) {
                var allCardsHtml = '';
                if (res['count'] < 1) {
                    $(".cards-container").html('<h2>No Movie Found!</h2>');
                } else {
                    $.each(res['results'], function (index, cardData) {
                        allCardsHtml += renderMovieCard(cardData);
                    });

                    $(".cards-container").html(allCardsHtml);
                }

            }
        });
    };

    var renderMovieCard = function (data) {
        var cardHtml = '<div class="movie-card">\n' +
            '                <img src="/static/images/default.jpg">\n' +
            '                <p class="movie-title"><a href="/detail/' + data['id'] + '">' + data['name'] + '</a></p>\n' +
            '                <p class="movie-duration"><span class="duration-num">' + data['duration'] + '</span> min</p>\n' +
            '                <p class="movie-rating"><span>User Rating: </span> <span class="rating-num"> ' + data['user_rating'] + '</span></p>\n' +
            '            </div>';
        return cardHtml;

    };

    getMovies();
});