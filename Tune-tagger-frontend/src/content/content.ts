
chrome.runtime.onMessage.addListener((message , _sender , response) =>{

    if(message.type === "GET_VIDEO_URL"){
        console.log("message received for getting video url");
        const videoURL = window.location.href;
        response({videoURL});
    }
    return true;
});


  