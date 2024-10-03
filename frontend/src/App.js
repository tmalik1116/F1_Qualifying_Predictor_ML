import React from 'react';

function Button() {
  
}

function App(){
  return (
    <div className="App">
        <div className="curb left"></div>


        <div className="content">
            <h1 className="display-1">Formula 1 Qualif-AI</h1>
            <p style={{ marginTop: '5%', marginBottom: '10%' }}>Predict Result For:</p>

            <div className="row">
                <div className="col-6"> 
                    <button id="driver-button" className="main button">Driver</button> 
                </div>

                <div className="col-6">
                    <button id="session-button" className="main button">Session</button> 
                </div>
            </div>

            <div id="submenu-card" className="submenu-card"> 
                <div className="submenu-content">

                </div>
            </div>

        </div>

        <div className="curb right"></div>
    </div>
  );
}

export default App;