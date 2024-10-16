import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "../build/static/styles.css";

const root = ReactDOM.createRoot(document.getElementById("root")); // Target the 'root' div in index.html

root.render(<App />);
