import React, { useState } from "react";
import CloseButton from "./CloseButton";
import EnterButton from "./EnterButton";
import { Switch } from "@mui/material";

export default function SessionMenu(props) {
    const [race, setRace] = useState("");
    const [season, setSeason] = useState("");
    const [rain, setrain] = useState(true); // State to manage the Switch
    
    const handleRaceChange = (event) => {
      setRace(event.target.value);
    };
    
    const handleSeasonChange = (event) => {
      setSeason(event.target.value);
    };
    
    const handleRainChange = (event) => {
      setrain(event.target.checked);
    };
  
    const submitData = () => {
      const formData = {
        race,
        season,
        rain,
      };
  
      fetch("/submitSession", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData)
      });
    };

  return (
    <div>
      <div className="col" id="submenu-column">
        <div className="row" id="driver-submenu-top">
          <label className="input-label-top" htmlFor="Race">
            Race
          </label>
          <CloseButton closeSubmenu={props.closeSubmenu} />
        </div>

        <input
          type="text"
          id="Race"
          placeholder="Ex. Monaco, Bahrain"
          className="input-field"
          onChange={handleRaceChange}
        ></input>
        <div className="vertical-spacer-medium"></div>
        <div className="row" id="driver-submenu-top">
          <label className="input-label" htmlFor="Season">
            Season
          </label>
        </div>
        <input
          type="text"
          id="Season"
          placeholder="Ex. 2024"
          className="input-field"
          onChange={handleSeasonChange}
        ></input>
        <div className="vertical-spacer-medium"></div>
        <div className="row" id="driver-submenu-top">
          <label className="input-label" htmlFor="Rain">
            Rain?
          </label>
        </div>
        <div>
          <div className="switch-row">
            <Switch
              className="switch"
              color="default"
              checked={rain}
              onChange={handleRainChange}
            />
            <h6 className="switch-label">{rain ? "On" : "Off"}</h6>
          </div>
          <div className="vertical-spacer-medium"></div>
          <EnterButton className="enter-button" onClick={submitData}/>
        </div>
      </div>
    </div>
  );
}
