import React, { useState, useRef } from "react";
import CloseButton from "./CloseButton";
import EnterButton from "./EnterButton";
import { Switch } from "@mui/material";

export default function DriverMenu(props) {
  
  const [driver, setDriver] = useState("");
  const [race, setRace] = useState("");
  const [season, setSeason] = useState("");
  const [rain, setrain] = useState(true); // State to manage the Switch

  const dialogRef = useRef(null);
  const [responseMsg, setResponseMsg] = useState("");

  const handleDriverChange = (event) => {
    setDriver(event.target.value);
  };
  
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
      driver,
      race,
      season,
      rain,
    };

    fetch("/submitDriver", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData)
    })
    .then((response) => response.json())
    .then((data) => {
      setResponseMsg("Predicted Time: " + data);
      dialogRef.current.showModal(); // open dialog
    })
    .catch((error) => {
      setResponseMsg("Error sending data to server.");
      dialogRef.current.showModal();
    });
  };

  const closeDialog = () => {
    dialogRef.current.close(); // Close the dialog
  };

  return (
    // <div>
    <div className="submenu-content">
      <div className="row" id="driver-submenu-top">
        <label className="input-label-top" htmlFor="Driver">
          Driver
        </label>
        <CloseButton closeSubmenu={props.closeSubmenu} />
      </div>
      <input
        type="text"
        id="Driver"
        placeholder="Ex. LEC, SAI"
        className="input-field"
        onChange={handleDriverChange}
      ></input>
      <div className="vertical-spacer-medium"></div>{" "}
      {/* Make 'spacer' CSS class for a div, can reuse wherever I want */}
      <div className="row" id="driver-submenu-top">
        <label className="input-label" htmlFor="Race">
          Race
        </label>
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
      <div className="switch-row">
        <Switch
          className="switch"
          color="default"
          checked={rain}
          onChange={handleRainChange}
          // inputProps={{ "aria-label": "controlled" }}
        />
        <h6 className="switch-label">{rain ? "On" : "Off"}</h6>
      </div>
      <div className="vertical-spacer-medium"></div>
      <EnterButton className="enter-button" onClick={submitData}/>

      <dialog ref={dialogRef}>
        <p>{responseMsg}</p>
        <button onClick={closeDialog}>Close</button>
      </dialog>
    </div>
    // {/* </div> */}
  );
}
