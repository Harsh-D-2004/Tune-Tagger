import { useEffect } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  Card,
  CardContent,
  List,
  ListItem,
  IconButton,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const Results: React.FC = () => {
  const [_results, setResults] = useState<
    { id: string; start_time: number; song_name: string; artist_name: string }[]
  >([]);

  const navigate = useNavigate();

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes === 0) {
      return `${remainingSeconds}s`;
    }

    if (remainingSeconds === 0) {
      return `${minutes}m`;
    }

    return `${minutes}m ${remainingSeconds}s`;
  };

  useEffect(() => {
    chrome.runtime.sendMessage(
      {
        type: "GET_RESULTS",
      },
      (response) => {
        if (chrome.runtime.lastError) {
          console.error(
            "Error in GET_RESULTS:",
            chrome.runtime.lastError.message
          );
          return;
        }
        console.log("Message received from bg script for results:", response);
        console.log("Ass seen on Results page");
        console.log(response.data);

        if (response.data == null) {
          console.log("No results found");
        }
        setResults(response.data);

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
          }
        );
      }
    );
  }, []);

  const handle_going_back = () => {
    chrome.storage.local.remove(
      ["processing_status", "prediction_status"],
      () => {
        console.log("Cleared storage for fresh start");
        navigate("/");
      }
    );
    
  };

  let Results = [
    {
      id: 1,
      start_time: 60,
      song_name: "Aliza",
      artist_name: "Craze",
    },
    {
      id: 2,
      start_time: 80,
      song_name: "Aliza jdjdnnnnnnd",
      artist_name: "Craze kddddddd",
    },
    {
      id: 3,
      start_time: 90,
      song_name: "Aliza jdjdnnnnnnd",
      artist_name: "Craze kddddddd",
    },
  ];

  return (
    <Box
      sx={{
        bgcolor: "#000",
        color: "#fff",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        py: 0,
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

      <Typography
        variant="h4"
        sx={{
          mb: 3,
          fontWeight: "bold",
          fontFamily: "Poppins, sans-serif",
          color: "#ff69b4",
          py: 5,
        }}
      >
        Tunes
      </Typography>

      {Results.length > 0 ? (
        <List sx={{ width: "90%", maxWidth: 600 }}>
          {Results.map((item) => (
            <ListItem key={item.id} sx={{ mb: 2 }}>
              <Card
                sx={{
                  bgcolor: "#121212",
                  color: "#fff",
                  width: "100%",
                  border: "1px solid #ff69b4",
                  boxShadow: "0px 4px 10px rgba(255, 105, 180, 0.4)",
                  borderRadius: 2,
                }}
              >
                <CardContent>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                      mb: 1,
                      fontFamily: "Poppins, sans-serif",
                      color: "#ff69b4",
                    }}
                  >
                    {item.song_name}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 0.5 }}>
                    <strong>Artist Name:</strong> {item.artist_name}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Start Time:</strong> {formatTime(item.start_time)}
                  </Typography>
                </CardContent>
              </Card>
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography variant="body1" sx={{ color: "#fff" }}>
          No results found.
        </Typography>
      )}
    </Box>
  );
};

export default Results;
