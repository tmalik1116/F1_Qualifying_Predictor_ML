import React from "react";

export default function MainButton(props) {
  return (
    <div className="col-6">
      <button
        id={props.type.toLowerCase() + "-button"}
        className={`main button ${props.isActive ? "expanded" : ""}`} // Use isActive prop for expansion
        onClick={() => props.toggleSubmenu(props.type)}
      >
        <div className="button-content">
          {/* Conditionally render content based on isActive */}
          {/* {props.isActive ? ( 
            // Expanded content (Driver or Session menu)
            <div className="submenu-content">
              {props.type === "Driver" && (
                <div>
                  Driver
                </div>
              )}
              {props.type === "Session" && (
                <div>
                  <h1>{props.type}</h1>
                </div>
              )}
            </div>
          ) : (
            // Collapsed content (just the button label)
            props.type
          )} */}
          {props.type}
        </div>
      </button>
    </div>
  );
}