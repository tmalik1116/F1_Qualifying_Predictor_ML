import React, { useState, useRef, useEffect } from "react";
import DriverMenu from "./DriverMenu";
import SessionMenu from "./SessionMenu";

export default function MainButton(props) {
  const [isAnimating, setIsAnimating] = useState(false);
  const [maxHeight, setMaxHeight] = useState("0px");
  const [isOverflowHidden, setIsOverflowHidden] = useState(true); // Starts with overflow hidden
  const contentRef = useRef(null); // Reference to the submenu content

  useEffect(() => {
    if (props.isActive) {
      const scrollHeight = contentRef.current.scrollHeight; // Get the natural height of the content
      setMaxHeight(`${scrollHeight}px`); // Set it as max-height
      setIsAnimating(true);
      setIsOverflowHidden(true); // disable overflow during animation for proper visual effect
    } else {
      setMaxHeight("0px");
      setIsOverflowHidden(true); // enable overflow after animation for proper shadow appearance on button
      setTimeout(() => setIsAnimating(false), 200); // play with value to get smooth visual (fallback to 200)
    }
  }, [props.isActive]);

  // After animation make overflow visible
  useEffect(() => {
    if (props.isActive) {
      const timeout = setTimeout(() => setIsOverflowHidden(true), 500);
      return () => clearTimeout(timeout); // clean up timeout
    }
  });

  function closeSubmenu() {
    // setIsOverflowVisible(false);
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
    <div className="col-6">
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
