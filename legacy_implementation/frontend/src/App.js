import React, {useState} from 'react';
import ReactDOM from 'react-dom/client';

function DriverButton(props) {
    function handleClick() {
        console.log('Click');
        props.toggleSubmenu('driver');
    }
    
    return (
        <button onClick={handleClick} id="driver-button" className="main button">Driver</button> 
    )
}

function SessionButton(props) {
    function handleClick() {
        console.log('Clicked');
        props.toggleSubmenu('session');
    }
    
    return (
        <button onClick={handleClick} id="session-button" className="main button">Session</button> 
    )
}

function Submenu(props) {
    const [isOpen, setIsOpen] = useState(false); // state for visibility

    const toggleSubmenu = () => {
        setIsOpen(!isOpen);
    }

    let content;
    if (props.type == 'driver') {
        content = <div><h1>Driver Menu</h1></div>;
    }else{
        content = <div><h1>Session Menu</h1></div>;
    }

    
    return (
        <div id="submenu-card" className={`submenu-card ${isOpen ? 'active' : ''}`}> 
            <div className="submenu-content">
                {props.type === 'driver' && (

                    <div>{content}</div>
                    // put driver UI here 
                    // INPUT: driver, track, year
                    // OUTPUT: predicted qualifying time
                )}
                {props.type === 'session' && (

                    <div>{content}</div>
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
                {/* <DriverButton toggleSubmenu={toggleSubmenu} /> */}
                {/* <SessionButton toggleSubmenu={toggleSubmenu} /> */}
            </div>

            <Submenu type={submenuType}/>
        </div>
        <div className="curb right"></div>
    </div>
  );
}

export default App;