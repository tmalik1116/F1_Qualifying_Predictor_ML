import React, { useEffect, useState } from "react";

const SessionResultsModal = ({ isOpen, onClose, results }) => {
  const [shouldRender, setShouldRender] = useState(false);
  const [animateIn, setAnimateIn] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setShouldRender(true);           // Mount the modal
      setTimeout(() => setAnimateIn(true), 10); // Delay to trigger transition
    } else {
      setAnimateIn(false);             // Trigger exit animation
      setTimeout(() => setShouldRender(false), 500); // Unmount after animation
    }
  }, [isOpen]);

  if (!shouldRender) return null;

  return (
    <div className="session-results-modal-overlay">
      <div className={`session-results-modal ${animateIn ? "open" : "closed"}`}>
        <div className="modal-content">
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
      </div>
    </div>
  );
};


export default SessionResultsModal;
