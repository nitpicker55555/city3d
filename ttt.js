navigator.geolocation.getCurrentPosition(
    function (position) {
        console.log("Latitude: " + position.coords.latitude);
        console.log("Longitude: " + position.coords.longitude);
    },
    function (error) {
        console.error(error);
    },
    {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    }
);

if (navigator.permissions) {
    navigator.permissions.query({ name: 'geolocation' }).then(function (result) {
        if (result.state === 'granted' || result.state === 'prompt') {
            navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
        } else if (result.state === 'denied') {
            console.log('Geolocation permission denied');
        }
        result.onchange = function () {
            console.log(result.state);
        }
    });
}

function successCallback(position) {
    console.log('Your current position is:');
    console.log(`Latitude : ${position.coords.latitude}`);
    console.log(`Longitude: ${position.coords.longitude}`);
    console.log(`More or less ${position.coords.accuracy} meters.`);
}

function errorCallback(error) {
    console.warn(`ERROR(${error.code}): ${error.message}`);
}
