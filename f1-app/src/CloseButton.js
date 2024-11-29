import React from "react";
import arrowImage from "./images/back_button_transparent.png";

export default function (props) {
  function handleClick() {
    props.closeSubmenu();
  }

  return (
    <div className="back-button-container">
      <button className="back-button" onClick={handleClick}>
        <img src={arrowImage} className="back-image" />
      </button>
    </div>
  );
}
