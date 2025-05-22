import axios from "axios";

const inputProcess = async (inputUrl : string) => {

    const res = await axios.post("http://localhost:8000/preprocessing/youtube_video/" , {'video_file_link' : inputUrl});

    if(res.status != 201){
        console.log("Error in processing video");
        return; 
    } 
    
    console.log(res.data);

    if(res.data == null){
        console.log("Error in processing video");
        return;
    }

    chrome.storage.local.set({vid : res.data.id} , () => {
        if(chrome.runtime.lastError){
            console.log("Error occured while storing")
        }else{
            console.log("Id stored successfully")
        }
    });
}


chrome.runtime.onMessage.addListener((message , _sender , response) =>{

    if(message.type === "PROCESS_URL"){
        console.log("message received");

        console.log("Received Url : " + message.inputUrl);

        inputProcess(message.inputUrl).then(() => {
            response({status : true});}).catch((error) => {
                console.error("Error in processing video:", error);
                response({ success: false, error: error.message });
              });

        return true;
    } 
});

chrome.runtime.onMessage.addListener((message , _sender , _response) =>{
    if(message.type === "DETECT_VIDEO_URL"){
        console.log("message received for detecting video url");
        console.log("Received Url : " + message.videoURL);



        chrome.storage.local.set({video_url : message.videoURL} , () => {
            if(chrome.runtime.lastError){
                console.log("Error occured while storing")
            }else{
                console.log("Video url stored successfully")
            }
        });
    
        return true;
    }
});

const chunking_call = async() =>{

    const vid = await new Promise<string>((resolve , reject) => {
        chrome.storage.local.get("vid" , (result) =>{
            if(chrome.runtime.lastError){
                console.log("Error occured while retrieving")
                reject(chrome.runtime.lastError)
            }
            else if(!result.vid){
                console.log("No video id in storage")
                reject("No video id in storage")
            }
            else{
                console.log("Id retireved successfully")
                resolve(result.vid)
            }
        })
    })
    const res = await axios.post("http://localhost:8000/chunking/audio-chunks/" , {video : vid})
    
    if(res.status != 201){
        console.log("Error in creating chunks");
        await axios.delete("http://localhost:8000/chunking/audio-chunks/delete/")
        return; 
    }

    console.log(res.data)
}

chrome.runtime.onMessage.addListener((message , _sender , response) =>{

    if(message.type === "PROCESSING"){
        console.log("message received for processing page");

        chunking_call().then(() => {
            response({status : true});}).catch((error) => {
                console.error("Error in creating chunks:", error);
                response({ success: false, error: error.message });
              });

        return true;
    } 
});


const predict_call = async() =>{

    const res = await axios.post("http://localhost:8000/model/song-predictions/")

    console.log(res.data)
    
    if(res.status != 201){
        console.log("Error in creating predictions");
        await axios.delete("http://localhost:8000/chunking/audio-chunks/delete/")
        return; 
    }

    console.log(res.data)
}

chrome.runtime.onMessage.addListener((message , _sender , response) =>{

    if(message.type === "PREDICT"){
        console.log("message received for processing page");

        predict_call().then(() => {
            response({status : true});}).catch((error) => {
                console.error("Error in predicting chunks:", error);
                response({ success: false, error: error.message });
              });

        return true;
    } 
});


const results_call = async () => {
    try {
      const res = await axios.get("http://localhost:8000/model/song-predictions/");
  
      if (res.status !== 200) {
        console.log("Error in getting predictions");
        await axios.delete("http://localhost:8000/chunking/audio-chunks/delete/");
        await axios.delete("http://localhost:8000/model/song-predictions/");
        throw new Error("Failed to fetch predictions.");
      }
  
      console.log("Predictions data:", res.data);
      return res.data; 
    } catch (error: any) {
      console.error("Error in results_call:", error.message || error);
      throw error; 
    }
  };

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message.type === "GET_RESULTS") {
      console.log("Message received for results page");
  
      results_call()
        .then((data) => {

          sendResponse({ success: true, data });
        })
        .catch((error) => {
          console.error("Error in getting results:", error);
          sendResponse({ success: false, error: error.message || "Unknown error occurred" });
        });
  
      return true; 
    }
  });

  const cleaning_call = async() =>{

    try{
        const res1 = await axios.delete("http://localhost:8000/chunking/audio-chunks/delete/")
        const res2 = await axios.delete("http://localhost:8000/model/song-predictions/")
        const res3 = await axios.delete("http://localhost:8000/preprocessing/videos/")
    
        if(res1.status != 200 || res2.status != 200 || res3.status != 200){
            console.log("Error in cleaning");
            return; 
        }

    }catch(error){
        console.log("Error in cleaning");
        return;
    }

  }

  chrome.runtime.onMessage.addListener((message , _sender , response) =>{

      if(message.type === "CLEANING"){
          console.log("message received for cleaning");

          cleaning_call().then(() => {
              response({status : true});}).catch((error) => {
                  console.error("Error in cleaning:", error);
                  response({ success: false, error: error.message });
                });

          return true;
      } 
  });

  chrome.runtime.onSuspend.addListener(() => {
    chrome.storage.local.remove(["processing_status", "prediction_status"], () => {
      console.log("Cleared storage for fresh start on extension exit.");
    });
  });
  