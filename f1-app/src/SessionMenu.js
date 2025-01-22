import React, { useRef, useState } from "react";
import CloseButton from "./CloseButton";
import EnterButton from "./EnterButton";
import { Switch } from "@mui/material";
import SessionResultsModal from "./SessionResultsModal";

export default function SessionMenu(props) {
    const [race, setRace] = useState("");
    const [season, setSeason] = useState("");
    const [rain, setRain] = useState(false); // State to manage the Switch
    const [isSessionResultsOpen, setIsSessionResultsOpen] = useState(false);
    const [crossData, setCrossData] = useState([]);

    const nullRef = useRef(null);
    const [responseMsg, setResponseMsg] = useState("");
    
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
      })
      .then((response) => response.json())
      .then((data) => {
        for (var i = 0; i < 20; i++){
          console.log(data[0]);
          crossData.push(data[i]);
        }
        
        setIsSessionResultsOpen(true); // Open the dialog
        // Should probably create new menu for this, will not look good in a popup dialog
      });
    };

    const closeDialog = (event) => {
      nullRef.current.close();
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
            Rain
          </label>
        </div>
        <div>
          <div className="switch-row">
            <Switch
              className="switch"
              color="default"
              defaultChecked={false}
              checked={rain}
              onChange={handleRainChange}
            />
            <h6 className="switch-label">{rain ? "Wet" : "Dry"}</h6>
          </div>
          <div className="vertical-spacer-medium"></div>
          <EnterButton className="enter-button" onClick={submitData}/>
        </div>
      </div>

      <SessionResultsModal isOpen={isSessionResultsOpen} onClose={() => setIsSessionResultsOpen(false)} results={crossData} />

      <dialog ref={nullRef}>
        <h2>Error
        </h2>
        <p>{responseMsg}</p>
        <button onClick={closeDialog} className="dialog-button">Close</button>
      </dialog>
    </div>
  );
}
