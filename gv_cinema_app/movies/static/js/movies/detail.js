$(document).ready(function () {

    var getMovieDetail = function (movieId) {
        var url = '/api/movies/' + movieId;
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (res) {
                $(".movie-name").html(res['name']);
                $(".movie-mpaa").html('(' + res['mpaa_rating']['type'] + ': ' + res['mpaa_rating']['label'] + ')');
                $(".movie-detail").html(renderMovieDetails(res));
            },
            error: function (xhr, ajaxOptions, thrownError) {
                if (xhr.status == 404) {
                    $(".movie-name").html('<h2>No Movie Found!</h2>');
                    $(".movie-mpaa").html('');
                    $(".movie-detail").html('');
                    $(".photo-container").html('');
                }
            }
        });
    }

    var renderMovieDetails = function (movieData) {
        var html = '<p><b>Details</b></p>\n' +
            '            <p><span>Genre: </span> <span> ' + movieData['genre'] + '</span></p>\n' +
            '            <p><span>Language: </span> <span> ' + movieData['language'] + '</span></p>\n' +
            '            <p><span>Duration: </span> <span> ' + movieData['duration'] + '</span> min</p>\n' +
            '            <p><span>User Rating: </span> <span> ' + movieData['user_rating'] + '</span></p>\n' +
            '            <p><b>Synopsis</b></p>\n' +
            '            <p>' + movieData['description'] + '</p>';
        return html;

    }

    var movieId = window.location.href.split('/detail/')[1].replace("/", "");
    ;

    getMovieDetail(movieId);
});