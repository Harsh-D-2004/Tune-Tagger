import React from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  LinearProgress,
  Paper,
  IconButton,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const Processing: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Reached useeffect of processing page");
    chrome.storage.local.get("processing_status", (result) => {
      console.log("Processing status:", result.processing_status);

      if (chrome.runtime.lastError) {
        console.log("Error occured while retrieving");
        return;
      } else if (result.processing_status === "completed") {
        chrome.storage.local.get("prediction_status", (result) => {
          if (chrome.runtime.lastError) {
            console.log("Error occured while retrieving");
            return;
          } else if (result.prediction_status === "completed") {
            chrome.storage.local.remove(
              ["processing_status", "prediction_status"],
              () => {
                console.log("Cleared storage for fresh start");
              }
            );
            navigate("/results");
          } else if (result.prediction_status === "in_progress") {
            console.log("Prediction is in progress");
            return;
          } else {
            handle_prediction();
          }
        });
      } else if (result.processing_status === "in_progress") {
        console.log("Processing is in progress");
        return;
      } else {
        handle_processing();
      }
    });
  }, []);

  const handle_processing = () => {
    chrome.storage.local.set({ processing_status: "in_progress" }, () => {
      chrome.runtime.sendMessage({ type: "PROCESSING" }, (response) => {
        if (chrome.runtime.lastError) {
          console.error(
            "Error in PROCESSING:",
            chrome.runtime.lastError.message
          );
          return;
        }

        console.log("Message received from bg script for chunking:", response);

        chrome.storage.local.set({ processing_status: "completed" }, () => {
          handle_prediction();
        });
      });
    });
  };

  const handle_prediction = () => {
    chrome.storage.local.set({ prediction_status: "in_progress" }, () => {
      chrome.runtime.sendMessage({ type: "PREDICT" }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error in PREDICT:", chrome.runtime.lastError.message);
          return;
        }
        console.log(
          "Message received from bg script for predictions:",
          response
        );

        chrome.storage.local.set({ prediction_status: "completed" }, () => {
          navigate("/results");
        });
      });
    });
  };

  const handle_going_back = () => {
    chrome.storage.local.remove(
      ["processing_status", "prediction_status"],
      () => {
        console.log("Cleared storage for fresh start");

        chrome.runtime.sendMessage(
          {
            type: "CLEANING",
          },
          (response) => {
            if (chrome.runtime.lastError) {
              console.error(
                "Error in CLEANING:",
                chrome.runtime.lastError.message
              );
              return;
            }
            console.log(
              "Message received from bg script for cleaning:",
              response
            );
            chrome.storage.local.remove(
              ["processing_status", "prediction_status"],
              () => {
                console.log("Cleared storage for fresh start");
                navigate("/");
              }
            );
            navigate("/");
          }
        );
      }
    );
  };

  return (
    <Box
      sx={{
        height: 300,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        bgcolor: "#000",
        color: "#fff",
        textAlign: "center",
      }}
    >
      <IconButton
        sx={{
          position: "absolute",
          top: 16,
          left: 16,
          color: "#ff69b4",
        }}
        onClick={handle_going_back}
      >
        <ArrowBackIcon fontSize="large" />
      </IconButton>

      <Paper
        elevation={6}
        sx={{
          p: 4,
          borderRadius: 2,
          backgroundImage: "linear-gradient(135deg, #ff69b4 30%, #000 90%)",
          color: "#fff",
          maxWidth: 400,
        }}
      >
        <Typography
          variant="h5"
          gutterBottom
          sx={{
            fontFamily: "Poppins, sans-serif",
            fontWeight: 600,
          }}
        >
          Processing Your Video
        </Typography>

        <Typography variant="body1" gutterBottom>
          Please wait while we process your request.
        </Typography>

        <LinearProgress
          sx={{
            mt: 3,
            height: 8,
            borderRadius: 2,
            backgroundColor: "#fff",
            "& .MuiLinearProgress-bar": {
              backgroundColor: "#ff69b4",
            },
          }}
        />
      </Paper>
    </Box>
  );
};

export default Processing;
