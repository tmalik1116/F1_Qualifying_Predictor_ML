import React, { useState, useRef, useEffect } from "react";
import DriverMenu from "./DriverMenu";
import SessionMenu from "./SessionMenu";

export default function MainButton(props) {
  const [isAnimating, setIsAnimating] = useState(false);
  const [maxHeight, setMaxHeight] = useState("0px");
  const [isOverflowVisible, setIsOverflowVisible] = useState(false);
  const contentRef = useRef(null); // Reference to the submenu content

  useEffect(() => {
    if (props.isActive) {
      const scrollHeight = contentRef.current.scrollHeight; // Get the natural height of the content
      setMaxHeight(`${scrollHeight}px`); // Set it as max-height
      setIsAnimating(true);
      setIsOverflowVisible(false); // disable overflow during animation for proper visual effect
    } else {
      setMaxHeight("0px");
      setIsOverflowVisible(true); // enable overflow after animation for proper shadow appearance on button
      setTimeout(() => setIsAnimating(false), 200); // play with value to get smooth visual
    }
  }, [props.isActive]);

  // After animation make overflow visible
  useEffect(() => {
    if (props.isActive) {
      const timeout = setTimeout(() => setIsOverflowVisible(true), 200);
      return () => clearTimeout(timeout); // clean up timeout
    }
  });

  function closeSubmenu() {
    props.toggleSubmenu(props.type);
  }

  function handleButtonClick() {
    if (!props.isActive) {
      props.toggleSubmenu(props.type);
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
                overflow: isOverflowVisible ? "visible" : "hidden",
                transition: "max-height 0.3s ease",
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
