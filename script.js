let video = document.querySelector('#webcam')
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia( { video: true }).then(function (stream) {
        video.srcObject = stream;
    }).catch(function (error) {
        console.log("Error: Something went wrong")
    })
} else {
    console.log("Error: Unable to retrieve webcam data, getUserMedia unsupported");
}