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
    if (props.isActive && contentRef.current) {
      // When activating, recalculate height after a short delay to ensure content is rendered
      setTimeout(() => {
        const scrollHeight = contentRef.current ? contentRef.current.scrollHeight : 0;
        // Set a reasonable max height that won't exceed viewport
        const viewportHeight = window.innerHeight;
        const maxHeightValue = Math.min(scrollHeight, viewportHeight * 0.8);
        
        setMaxHeight(`${maxHeightValue}px`);
      }, 50);
      
      setIsAnimating(true);
      setIsOverflowHidden(true);
    } else {
      setMaxHeight("0px");
      setIsOverflowHidden(true);
      setTimeout(() => setIsAnimating(false), 200);
    }
  }, [props.isActive]);

  // After animation make overflow visible for scrolling if needed
  useEffect(() => {
    if (props.isActive) {
      // After animation completes, allow overflow for scrolling if content is tall
      const timeout = setTimeout(() => setIsOverflowHidden(false), 500);
      return () => clearTimeout(timeout);
    }
  }, [props.isActive]);

  function closeSubmenu() {
    props.toggleSubmenu(props.type);
  }

  function handleButtonClick() {
    if (!props.isActive) {
      var delayInMilliseconds = 0;
      
      setTimeout(function() {
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
        style={{
          // Ensure consistent height when collapsed
          height: props.isActive ? "auto" : (isMobile ? "60px" : "auto")
        }}
      >
        <div className="button-content">
          {props.isActive || isAnimating ? (
            <div
              ref={contentRef}
              className="submenu-content"
              style={{
                maxHeight: maxHeight,
                overflow: isOverflowHidden ? "hidden" : "auto", // Change to auto to allow scrolling
                transition: "max-height 0.4s ease-in-out", 
                width: "100%",
                boxSizing: "border-box"
              }}
            >
              {props.type === "Driver" && (
                <DriverMenu closeSubmenu={closeSubmenu} isMobile={isMobile} />
              )}
              {props.type === "Session" && (
                <SessionMenu closeSubmenu={closeSubmenu} isMobile={isMobile} />
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