var $ltMAx$reactjsxruntime = require("react/jsx-runtime");
require("react");
var $ltMAx$reactdomclient = require("react-dom/client");


function $parcel$interopDefault(a) {
  return a && a.__esModule ? a.default : a;
}





function $da11a1101b2a894a$var$App() {
    return /*#__PURE__*/ (0, $ltMAx$reactjsxruntime.jsx)("div", {
        children: /*#__PURE__*/ (0, $ltMAx$reactjsxruntime.jsx)("h1", {
            children: "Formula 1 Qualif-AI"
        })
    });
}
var $da11a1101b2a894a$export$2e2bcd8739ae039 = $da11a1101b2a894a$var$App;


const $4fa36e821943b400$var$root = (0, ($parcel$interopDefault($ltMAx$reactdomclient))).createRoot(document.getElementById("root")); // Target the 'root' div in index.html
const $4fa36e821943b400$var$buttons = document.querySelectorAll(".main-button");
const $4fa36e821943b400$var$driverButton = document.getElementById("driver-button");
const $4fa36e821943b400$var$sessionButton = document.getElementById("session-button");
const $4fa36e821943b400$var$submenuCard = document.getElementById("submenu-card");
const $4fa36e821943b400$var$submenuContent = document.querySelector(".submenu-content");
$4fa36e821943b400$var$root.render(/*#__PURE__*/ (0, $ltMAx$reactjsxruntime.jsx)((0, $da11a1101b2a894a$export$2e2bcd8739ae039), {}));
$4fa36e821943b400$var$driverButton.addEventListener("click", ()=>{
    console.log("Driver click");
    $4fa36e821943b400$var$submenuContent.innerHTML = ""; // Clear previous content
    // Add driver-specific submenu items here:
    $4fa36e821943b400$var$submenuContent.innerHTML = "<h2>Driver Submenu</h2>";
    // ... (Add your form or input elements for driver predictions) 
    $4fa36e821943b400$var$submenuCard.classList.add("active");
    $4fa36e821943b400$var$submenuContent.classList.add("active");
});
$4fa36e821943b400$var$sessionButton.addEventListener("click", ()=>{
    console.log("Session click");
    $4fa36e821943b400$var$submenuContent.innerHTML = ""; // Clear previous content
    // Add session-specific submenu items here:
    $4fa36e821943b400$var$submenuContent.innerHTML = "<h2>Session Submenu</h2>";
    // ... (Add your form or input elements for session predictions) 
    $4fa36e821943b400$var$submenuCard.classList.add("active");
    $4fa36e821943b400$var$submenuContent.classList.add("active");
});
// Add an event listener to close the card when clicking outside of it 
window.addEventListener("click", (event)=>{
    if (!$4fa36e821943b400$var$submenuCard.contains(event.target) && !event.target.classList.contains("main")) {
        $4fa36e821943b400$var$submenuCard.classList.remove("active");
        $4fa36e821943b400$var$submenuContent.classList.remove("active");
    }
});


//# sourceMappingURL=index.js.map
