import React from "react";
import DriverMenu from "./DriverMenu";
import SessionMenu from "./SessionMenu";

export default function MainButton(props) {
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
        className={`main button ${props.isActive ? "expanded" : ""}`} // Use isActive prop for expansion
        onClick={handleButtonClick}
      >
        <div className="button-content">
          {/* Conditionally render content based on isActive */}
          {props.isActive ? (
            // Expanded content (Driver or Session menu)
            <div className="submenu-content">
              {" "}
              {/* Does not show up because its hidden in CSS, fix that */}
              {props.type === "Driver" && (
                <div>
                  <DriverMenu closeSubmenu={closeSubmenu} />
                </div>
              )}
              {props.type === "Session" && (
                <div>
                  <SessionMenu closeSubmenu={closeSubmenu} />
                </div>
              )}
            </div>
          ) : (
            // Collapsed content (just the button label)
            <h2>{props.type}</h2>
          )}
          {/* {props.type} */}
        </div>
      </button>
    </div>
  );
}
