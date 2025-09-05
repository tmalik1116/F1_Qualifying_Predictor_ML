import "./App.css"
import MainButton from "./MainButton"
import React, {useState, useEffect} from "react";
// import { Analytics } from "@vercel/analytics/react"

export default function App() {
  const [activeButton, setActiveButton] = useState(null); // State for active button (null means none)
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  
  // Add responsive detection
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    
    // Initial check
    handleResize();
    
    // Add event listener
    window.addEventListener('resize', handleResize);
    
    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

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
        <h2 style={{ marginTop: isMobile ? '3%' : '5%', marginBottom: isMobile ? '3%' : '5%' }}>Predict Result For:</h2>

        <div className={isMobile ? "column" : "row-6"} id="buttons">
          <MainButton type="Driver" isActive={activeButton === 'Driver'} toggleSubmenu={toggleSubmenu}/>
          <MainButton type="Session" isActive={activeButton === 'Session'} toggleSubmenu={toggleSubmenu}/>
        </div>
      </div>

      <div className="curb right"></div>
    </div>
  );
}