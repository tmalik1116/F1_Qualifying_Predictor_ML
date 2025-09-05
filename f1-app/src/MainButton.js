import React, { useState, useRef, useEffect } from "react";
import DriverMenu from "./DriverMenu";
import SessionMenu from "./SessionMenu";

export default function MainButton(props) {
  const [isAnimating, setIsAnimating] = useState(false);
  const [maxHeight, setMaxHeight] = useState("0px");
  const [isOverflowHidden, setIsOverflowHidden] = useState(true); // Starts with overflow hidden
  const contentRef = useRef(null); // Reference to the submenu content
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

  useEffect(() => {
    if (props.isActive) {
      // When activating, get the natural height of the content
      const scrollHeight = contentRef.current.scrollHeight;
      // Set max-height with additional space for mobile to ensure content fits
      setMaxHeight(isMobile ? `${scrollHeight + 30}px` : `${scrollHeight}px`);
      setIsAnimating(true);
      setIsOverflowHidden(true); // disable overflow during animation for proper visual effect
    } else {
      setMaxHeight("0px");
      setIsOverflowHidden(true); // enable overflow after animation for proper shadow appearance on button
      setTimeout(() => setIsAnimating(false), 200); // play with value to get smooth visual (fallback to 200)
    }
  }, [props.isActive, isMobile]);

  // After animation make overflow visible
  useEffect(() => {
    if (props.isActive) {
      const timeout = setTimeout(() => setIsOverflowHidden(true), 500);
      return () => clearTimeout(timeout); // clean up timeout
    }
  });

  function closeSubmenu() {
    props.toggleSubmenu(props.type);
  }

  function handleButtonClick() {
    if (!props.isActive) {
      var delayInMilliseconds = 0; //0.15 seconds

      setTimeout(function() {
        setIsOverflowHidden(true);
        props.toggleSubmenu(props.type);
        
      }, delayInMilliseconds);
    }
  }

  return (
    <div className={isMobile ? "col-12" : "col-6"}>
      <button
        id={props.type.toLowerCase() + "-button"}
        className={`main button ${props.isActive ? "expanded" : ""}`}
        onClick={handleButtonClick}
      >
        <div className="button-content">
          {props.isActive || isAnimating ? (
            <div
              ref={contentRef}
              className="submenu-content"
              style={{
                maxHeight: maxHeight,
                overflow: isOverflowHidden ? "hidden" : "visible",
                transition: "max-height 0.3s ease", // go back to 0.3 if desired
                width: isMobile ? "100%" : "auto"
              }}
            >
              {props.type === "Driver" && (
                <DriverMenu closeSubmenu={closeSubmenu} />
              )}
              {props.type === "Session" && (
                <SessionMenu closeSubmenu={closeSubmenu} />
              )}
            </div>
          ) : (
            <h2>{props.type}</h2>
          )}
        </div>
      </button>
    </div>
  );
}