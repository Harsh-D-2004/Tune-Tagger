import { useNavigate } from "react-router-dom";
import React, { useState , useEffect } from "react";
import {
  Box,
  // TextField,
  Button,
  Typography,
  Container,
  Paper,
} from "@mui/material";

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [_url, setUrl] = useState<string>("");

  useEffect(() => {
    // chrome.storage.local.remove(["processing_status", "prediction_status"], () => {
    //   console.log("Cleared storage for fresh start");
    // });
    chrome.storage.local.get(
      ["processing_status", "prediction_status"],
      (result) => {
        if (chrome.runtime.lastError) {
          console.log("Error occured while retrieving");
          return;
        } else if (
          result.processing_status === "in_progress" ||
          result.processing_status === "completed" ||
          result.prediction_status === "in_progress" ||
          result.prediction_status === "completed"
        ) {
          navigate("/processing");
        }
      }
    );
  }, []);

  // const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  //   setUrl(event.target.value);
  // };

  const handleClick = () => {
    chrome.runtime.sendMessage({ type: "GET_VIDEO_URL" }, (response) => {
      if (chrome.runtime.lastError) {
        console.error("Error communicating with content script:", chrome.runtime.lastError.message);
        return;
      }
  
      const videoURL = response?.videoURL;
      if (!videoURL) {
        console.error("No video URL received.");
        return;
      }
  
      console.log("Received video URL:", videoURL);
  
      // Continue processing with the video URL
      setUrl(videoURL);
      chrome.runtime.sendMessage({ type: "PROCESS_URL", inputUrl: videoURL }, (processResponse) => {
        if (chrome.runtime.lastError) {
          console.error("Error communicating with background script:", chrome.runtime.lastError.message);
          return;
        }
  
        console.log("Processing response:", processResponse);
        handlenavigation();
      });
    });
  };
  

  function handlenavigation() {
    navigate("/processing");
  }

  return (
    <Container
      maxWidth="sm"
      sx={{
        bgcolor: "#000",
        color: "#fff",
        borderRadius: 2,
        py: 4,
        px: 3,
        boxShadow: "0 8px 15px rgba(0, 0, 0, 0.5)",
      }}
    >
      <Paper
        elevation={6}
        sx={{
          p: 4,
          borderRadius: 2,
          backgroundImage: "linear-gradient(135deg, #ff69b4 30%, #000 90%)",
          color: "#fff",
        }}
      >
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{
            fontFamily: "Poppins, sans-serif",
            fontWeight: 600,
            letterSpacing: 1.5,
            color: "#fff",
          }}
        >
          TuneTagger
        </Typography>

        <Box sx={{ mt: 3, display: "flex", flexDirection: "column", gap: 3 }}>
          {/* <TextField
            label="YouTube Video URL"
            variant="filled"
            placeholder="Enter YouTube video URL"
            onChange={handleChange}
            fullWidth
            InputProps={{
              style: {
                backgroundColor: "#fff",
                borderRadius: 4,
              },
            }}
            InputLabelProps={{
              style: {
                color: "#ff69b4",
              },
            }}
          /> */}

          <Button
            variant="contained"
            size="large"
            onClick={handleClick}
            sx={{
              backgroundColor: "#ff69b4",
              color: "#fff",
              fontWeight: "bold",
              "&:hover": {
                backgroundColor: "#ff1493",
              },
              borderRadius: 3,
              py: 1.5,
              boxShadow: "0 5px 10px rgba(255, 105, 180, 0.5)",
            }}
          >
            Process Video
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Home;
