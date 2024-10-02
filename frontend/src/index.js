import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';


const root = ReactDOM.createRoot(document.getElementById('root')); // Target the 'root' div in index.html

const buttons = document.querySelectorAll('.main-button');
const driverButton = document.getElementById('driver-button');
const sessionButton = document.getElementById('session-button');
const submenuCard = document.getElementById('submenu-card');
const submenuContent = document.querySelector('.submenu-content'); 


root.render(<App />);


driverButton.addEventListener('click', () => {
    console.log('Driver click')
    submenuContent.innerHTML = ''; // Clear previous content

    // Add driver-specific submenu items here:
    submenuContent.innerHTML = '<h2>Driver Submenu</h2>';
    // ... (Add your form or input elements for driver predictions) 

    submenuCard.classList.add('active');
    submenuContent.classList.add('active');
});

sessionButton.addEventListener('click', () => {
    console.log('Session click')
    submenuContent.innerHTML = ''; // Clear previous content

    // Add session-specific submenu items here:
    submenuContent.innerHTML = '<h2>Session Submenu</h2>';
    // ... (Add your form or input elements for session predictions) 

    submenuCard.classList.add('active');
    submenuContent.classList.add('active');
});

// Add an event listener to close the card when clicking outside of it 
window.addEventListener('click', (event) => {
  if (!submenuCard.contains(event.target) && !event.target.classList.contains('main')) { 
    submenuCard.classList.remove('active'); 
    submenuContent.classList.remove('active');
  }
});