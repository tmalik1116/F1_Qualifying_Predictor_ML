import React from "react";

export default function EnterButton({className, onClick, disabled}) {
  return <button className={`internal-button ${disabled ? "loading" : ""}`} onClick={onClick}>
    {disabled ? (
    <div className="loading-spinner"></div> // Placeholder for loading spinner
  ) : (
    "Calculate!"
  )}</button>;
}
