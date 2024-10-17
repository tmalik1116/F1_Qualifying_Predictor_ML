import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div id="body"> 
      <div className="curb left"></div>

      <div className="content">
        
        <h1 className="display-1">Formula 1 Qualif-AI</h1>
        <h3 style={{ marginTop: '5%', marginBottom: '10%' }}>Predict Result For:</h3>

        <div id="buttons">
          <div className="col-6">
            <button id="driver-button" className="main button">Driver</button>
          </div>
          <div className="col-6">
            <button id="session-button" className="main button">Session</button>
          </div>
        </div>

        <div id="submenu-card" className="submenu-card">
          <div className="submenu-content">
            {/* Add your submenu content here */}
          </div>
        </div>
      </div>

      <div className="curb right"></div>
    </div>
  );
}

export default App;
