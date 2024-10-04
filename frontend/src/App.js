import React, {useState} from 'react';
import ReactDOM from 'react-dom/client';

function DriverButton(props) {
    return (
        <div className="col-6"> 
            <button onClick={() => props.toggleSubmenu('driver')} id="driver-button" className="main button">Driver</button> 
        </div>
    )
}

function SessionButton(props) {
    return (
        <div className="col-6">
            <button onClick={() => props.toggleSubmenu('session')} id="session-button" className="main button">Session</button> 
        </div>
    )
}

function Submenu(props) {
    const [isOpen, setIsOpen] = useState(false); // state for visibility

    const toggleSubmenu = () => {
        setIsOpen(!isOpen);
    }

    
    return (
        <div id="submenu-card" className={`submenu-card ${isOpen ? 'active' : ''}`}> 
            <div className="submenu-content">
                {props.type === 'driver' && (

                    <div>
                        <h1>Driver Menu</h1>
                    </div>
                    // put driver UI here 
                    // INPUT: driver, track, year
                    // OUTPUT: predicted qualifying time
                )}
                {props.type === 'session' && (

                    <div>
                        <h1>Session Menu</h1>
                    </div>
                    // put session UI here
                    // INPUT: track, year, weather (optional)
                    // OUTPUT: predicted qualifying grid - times and positions
                )}
            </div>
        </div>
    )
}

function App(){

    const [submenuType, setSubmenuType] = useState(null); // state for submenu type (driver/session)

    const toggleSubmenu = (type) => {
        console.log("toggleSubmenu called"); // not working, investigate
        setSubmenuType(type);
    };
    
  return (
    <div className="App">
        <div className="curb left"></div>


        <div className="content">
            <h1 className="display-1">Formula 1 Qualif-AI</h1>
            <p style={{ marginTop: '5%', marginBottom: '10%' }}>Predict Result For:</p>

            <div className="row">
                <DriverButton toggleSubmenu={toggleSubmenu} />
                <SessionButton toggleSubmenu={toggleSubmenu} />
            </div>

            <Submenu type={submenuType}/>
        </div>
        <div className="curb right"></div>
    </div>
  );
}

export default App;