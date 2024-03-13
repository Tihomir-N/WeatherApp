$(document).ready(function () {
    $('#refreshButton').click(function (e) {
        e.preventDefault();

        if (!window.location.href.includes('city')) {
            window.location.href = window.location.href + '?city=London';
        }
        $.ajax({
            type: 'GET',
            url: window.location.href + '&refresh=true',
            success: function (data) {
                $('.weather .left h2').text(data.temp + '° C');
                $('.weather .left h3').text(data.city);
                $('.weather .condition p:first-child').text(data.description);
                $('.weather .condition p:last-child').text(data.day);
                $('.weather .icon img').attr('src', 'http://openweathermap.org/img/w/' + data.icon + '.png');

                var tbody = $('#weatherTableBody');
                tbody.empty();
                data.recent_weather_stats.forEach(function (weather_stat) {
                    const dateString = formatDateTime(new Date(weather_stat.date));
                    var row = $('<tr>');
                    row.append($('<td>').text(weather_stat.city));
                    row.append($('<td>').text(weather_stat.description));
                    row.append($('<td>').text(weather_stat.temp));
                    row.append($('<td>').text(dateString));
                    tbody.append(row);
                });
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error('Error refreshing weather data:', errorThrown);
            }
        });
    });
});

$(document).ready(function () {
    // Set initial action attribute of the form to the current URL with city parameter
    var currentUrl = window.location.href;
    $('#searchForm').attr('action', currentUrl);

    // Intercept form submission
    $('#searchForm').submit(function (e) {
        // Get the value of the city input
        var city = $('#cityInput').val();
        
        // Update the action attribute with the current city value
        var newUrl = window.location.origin + window.location.pathname + '?city=' + encodeURIComponent(city);
        $(this).attr('action', newUrl);
    });
});

function formatDateTime(date) {
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const ampm = date.getHours() >= 12 ? 'p.m.' : 'a.m.';
    const hour = date.getHours() % 12 || 12;
    const minutes = date.getMinutes().toString().padStart(2, '0');

    return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}, ${hour}:${minutes} ${ampm}`;
}
