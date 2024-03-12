$(document).ready(function() {
    // Function to refresh the temperature
    function refreshTemperature() {
        $.ajax({
            url: '/get_recent_temperature/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data.temperature !== null) {
                    $('#temperature').text(data.temperature + '° C');
                } else {
                    alert('Failed to fetch recent temperature.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error refreshing temperature:', error);
            }
        });
    }

    // Event listener for the refresh button
    $('#refreshButton').click(function() {
        refreshTemperature();
    });
});