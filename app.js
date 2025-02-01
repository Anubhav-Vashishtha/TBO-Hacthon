import express from "express";
import axios from "axios";
import { makeAuthenticatedRequest } from "./Helper Function/authen.js";

const app = express();

// Middleware
app.set("view engine", "pug");
app.set("views", "./views");
app.use(express.static("public"));
app.use(express.json());
app.use(express.urlencoded({ extended: true })); // Parse form data

// Routes
app.get("/", (req, res) => {
  res.render("send", { title: "Hotel Search" });
});

app.post("/hotel", async (req, res) => {
  const { query, top_k } = req.body;

  // Ensure query is provided
  if (!query) {
    return res.send("Query is required!");
  }

  try {
    const response = await axios.post("http://localhost:5005/search", {
      query: query,
      top_k: top_k || 6,
    });

    console.log(response.data[0])
    res.render("results", {
      title: "Hotel Search Results",
      hotels: response.data,
    });
  } catch (error) {
    console.error("Error contacting the Flask API:", error);
    res.send("An error occurred while fetching the results.");
  }
});

app.get("/hotel/:Id", async (req, res) => {
  let responsedata = await makeAuthenticatedRequest("/HotelDetails", "post", {
    Hotelcodes: req.params.Id,
    Language: "EN",
  });

  res.render("hotel", {
    title: "Hotel Search Results",
    hotel: responsedata.HotelDetails[0],
  });
});

// Start Server
const PORT = process.env.PORT;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
