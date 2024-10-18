import "./App.css"
import MainButton from "./MainButton"
import React, {useState} from "react";

export default function App() {
  const [activeButton, setActiveButton] = useState(null); // State for active button (null means none)

  const toggleSubmenu = (buttonType) => {
    // If the clicked button is already active, close it
    if (activeButton === buttonType) {
      setActiveButton(null); 
    } else {
      // Otherwise, set the clicked button as active
      setActiveButton(buttonType);
    }
  };


  return (
    <div id="body"> 
      <div className="curb left"></div>

      <div className="content">
        
        <h1 className="display-1">Formula 1 Qualif-AI</h1>
        <h3 style={{ marginTop: '5%', marginBottom: '5%' }}>Predict Result For:</h3>

        <div className="row-6" id="buttons">
          <MainButton type="Driver" isActive={activeButton === 'Driver'} toggleSubmenu={toggleSubmenu}/>
          <MainButton type="Session" isActive={activeButton === 'Session'} toggleSubmenu={toggleSubmenu}/>
        </div>
      </div>

      <div className="curb right"></div>
    </div>
  );
}

