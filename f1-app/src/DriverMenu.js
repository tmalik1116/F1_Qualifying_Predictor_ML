import React, { useState, useRef } from "react";
import CloseButton from "./CloseButton";
import EnterButton from "./EnterButton";
import { Switch } from "@mui/material";
import stopwatchIcon from "./images/istockphoto-1462617826-612x612-removebg.png";
import { use } from "react";

export default function DriverMenu(props) {
  
  const [driver, setDriver] = useState("");
  const [race, setRace] = useState("");
  const [season, setSeason] = useState("");
  const [rain, setRain] = useState(false); // State to manage the Switch

  const [isLoading, setIsLoading] = useState(false);

  const dialogRef = useRef(null);
  const nullRef = useRef(null);
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
    setRain(event.target.checked);
  };

  const submitData = () => {
    const formData = {
      driver,
      race,
      season,
      rain,
    };

    setIsLoading(true);

    if (!driver || !race || !season){
      setResponseMsg("Please fill out all fields and try again.");
      nullRef.current.showModal();
      return;
    }

    fetch("https://tmalik1116.pythonanywhere.com/submitDriver", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData)
    })
    .then((response) => response.json())
    .then((data) => {
      setResponseMsg("Predicted Time: \n" + data);
      setIsLoading(false);
      dialogRef.current.showModal(); // open dialog
    })
    .catch((error) => {
      setResponseMsg("Error sending data to server.");
      dialogRef.current.showModal();
    });
  };

  const closeDialog = (event) => {
    dialogRef.current.close(); // Close the dialog
    nullRef.current.close();
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
          Rain
        </label>
      </div>
      <div className="switch-row">
        <Switch
          className="switch"
          color="default"
          defaultChecked={false}
          checked={rain}
          onChange={handleRainChange}
          // inputProps={{ "aria-label": "controlled" }}
        />
        <h6 className="switch-label">{rain ? "Wet" : "Dry"}</h6>
      </div>
      <div className="vertical-spacer-medium"></div>
      <EnterButton className="enter-button" onClick={submitData} disabled={isLoading}/>

      <dialog ref={dialogRef}>
        <h2>
          Driver Prediction  
          <img src={stopwatchIcon} alt="Ranking icon" className="dialog-image-top"></img>
        </h2>
        
        <p>{responseMsg}</p>
        <button onClick={closeDialog} className="dialog-button">Close</button>
      </dialog>

      <dialog ref={nullRef}>
        <h2>Error
        </h2>
        <p>{responseMsg}</p>
        <button onClick={closeDialog} className="dialog-button">Close</button>
      </dialog>
    </div>
    // {/* </div> */}
  );
}
