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

    const [isLoading, setIsLoading] = useState(false);

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

      setIsLoading(true);
    
      fetch("https://tmalik1116.pythonanywhere.com/submitSession", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
        .then((response) => response.json())
        .then((data) => {
          // Format the data into an array of objects with driver and time
          const formattedResults = Object.entries(data)
            .map(([driver, time]) => {
              // Convert time string to total milliseconds for sorting
              const [minutes, seconds] = time.split(":").map(parseFloat);
              const totalMilliseconds = minutes * 60 * 1000 + seconds * 1000;
    
              return { driver, time, totalMilliseconds };
            })
            .sort((a, b) => a.totalMilliseconds - b.totalMilliseconds) // Sort by totalMilliseconds
            .map(({ driver, time }) => ({ driver, time })); // Remove `totalMilliseconds` for clean data
    
          // Update state with formatted results
          setCrossData(formattedResults);
    
          // Open the session results modal
          setIsSessionResultsOpen(true);
          setIsLoading(false);
        })
        .catch((error) => {
          setIsLoading(false);
          console.error("Error submitting data:", error);
          setResponseMsg("An error occurred while processing your request.");
          nullRef.current.showModal(); // Show the error dialog
        });
    };
    
    

    const closeDialog = (event) => {
      nullRef.current.close();
    };

  return (
    <div>

      <SessionResultsModal
        className="modal"
        isOpen={isSessionResultsOpen}
        onClose={() => setIsSessionResultsOpen(false)}
        results={crossData}
      />
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
              className={`switch${isSessionResultsOpen ? "-hidden" : ""}`}
              color="default"
              defaultChecked={false}
              checked={rain}
              onChange={handleRainChange}
            />
            <h6 className="switch-label">{rain ? "Wet" : "Dry"}</h6>
          </div>
          <div className="vertical-spacer-medium"></div>
          <EnterButton className="enter-button" onClick={submitData} disabled={isLoading}/>
        </div>
      </div>

      

      <dialog ref={nullRef}>
        <h2>Error
        </h2>
        <p>{responseMsg}</p>
        <button onClick={closeDialog} className="dialog-button">Close</button>
      </dialog>
    </div>
  );
}
