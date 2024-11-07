import React, { useState } from "react";
import CloseButton from "./CloseButton";
import CustomizedSwitch from "./CustomizedSwitches";
import { Switch } from "@mui/material";

export default function DriverMenu(props) {
  const [isChecked, setIsChecked] = useState(true); // State to manage the Switch

  const handleChange = (event) => {
    setIsChecked(event.target.checked);
  };

  return (
    <div>
      <div className="col" id="submenu-column">
        <div className="row" id="driver-submenu-top">
          <label className="input-label-top" for="Driver">
            Driver
          </label>
          <CloseButton closeSubmenu={props.closeSubmenu} />
        </div>
        <input
          type="text"
          id="Driver"
          placeholder="Ex. LEC, SAI"
          className="input-field"
        ></input>
        <div className="vertical-spacer-medium"></div>{" "}
        {/* Make 'spacer' CSS class for a div, can reuse wherever I want */}
        <div className="row" id="driver-submenu-top">
          <label className="input-label" for="Race">
            Race
          </label>
        </div>
        <input
          type="text"
          id="Race"
          placeholder="Ex. Monaco, Bahrain"
          className="input-field"
        ></input>
        <div className="vertical-spacer-medium"></div>
        <div className="row" id="driver-submenu-top">
          <label className="input-label" for="Season">
            Season
          </label>
        </div>
        <input
          type="text"
          id="Season"
          placeholder="Ex. 2024"
          className="input-field"
        ></input>
        <div className="vertical-spacer-medium"></div>
        <div className="row" id="driver-submenu-top">
          <label className="input-label" for="Rain">
            Rain? (On/Off) {isChecked ? "True" : "False"}
          </label>
        </div>
        <div className="switch">
          <CustomizedSwitch
            id="Rain"
            checked={isChecked}
            onChange={handleChange}
            inputProps={{ "ari-label": "controlled" }}
          />
          <Switch
            checked={isChecked}
            onChange={handleChange}
            inputProps={{ "ari-label": "controlled" }}
          />
        </div>
      </div>
    </div>
  );
}
