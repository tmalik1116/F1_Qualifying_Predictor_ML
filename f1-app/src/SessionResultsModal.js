import React from "react";
import "./App.css";

const SessionResultsModal = ({ isOpen, onClose, results }) => {
  return (
    <dialog className="session-results-modal" style="background-colour: #2e2e2e" open={isOpen}>
      <div className="modal-content" style="background-color: #2e2e2e">
        <h2 className="modal-title" style="color: white">Session Results</h2>
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
