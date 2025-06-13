import React from "react";
import "./App.css";

const SessionResultsModal = ({ isOpen, onClose, results }) => {
  return (
    <dialog className="session-results-modal" open={isOpen} style="padding: 0px;">
      <div className="modal-content" style={{ backgroundColor: "#222", color: "#fff", margin: "0px", borderRadius: "15px" }}>
        <h2 className="modal-title">Session Results</h2>
        <div className="results-table">
          {results.map((result, index) => (
            <div key={index} className="result-row">
              <span className="driver-abbreviation">{result.driver}</span>
              <span className="lap-time">{result.time}</span>
            </div>
          ))}
        </div>
        <button className="dialog-button" onClick={onClose}>
          Close
        </button>
      </div>
    </dialog>
  );
};

export default SessionResultsModal;
