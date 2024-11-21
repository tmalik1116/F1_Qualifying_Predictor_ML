import React, { useState } from "react";
import CloseButton from "./CloseButton";
import CustomizedSwitch from "./CustomizedSwitches";
import { Switch } from "@mui/material";

export default function SessionMenu(props) {
  const [isChecked, setIsChecked] = useState(true); // State to manage the Switch

  const handleChange = (event) => {
    setIsChecked(event.target.checked);
  };

  return (
    <div>
      <div className="col" id="submenu-column">
        <div className="row" id="driver-submenu-top">
          <label className="input-label-top" for="Race">
            Race
          </label>
          <CloseButton closeSubmenu={props.closeSubmenu} />
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
            Rain?
          </label>
        </div>
        <div>
          <div className="row">
            <Switch
              className="switch"
              color="default"
              checked={isChecked}
              onChange={handleChange}
            />
            <h6 className="switch-label">{isChecked ? "On" : "Off"}</h6>
          </div>
        </div>
      </div>
    </div>
  );
}
