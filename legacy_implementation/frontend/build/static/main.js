require("./main.css");
var $3sv40$react = require("react");
var $3sv40$reactdomclient = require("react-dom/client");
var $3sv40$reactjsxruntime = require("react/jsx-runtime");


function $parcel$interopDefault(a) {
  return a && a.__esModule ? a.default : a;
}






function $da11a1101b2a894a$var$DriverButton(props) {
    function handleClick() {
        console.log("Click");
        props.toggleSubmenu("driver");
    }
    return /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("button", {
        onClick: handleClick,
        id: "driver-button",
        className: "main button",
        children: "Driver"
    });
}
function $da11a1101b2a894a$var$SessionButton(props) {
    function handleClick() {
        console.log("Clicked");
        props.toggleSubmenu("session");
    }
    return /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("button", {
        onClick: handleClick,
        id: "session-button",
        className: "main button",
        children: "Session"
    });
}
function $da11a1101b2a894a$var$Submenu(props) {
    const [isOpen, setIsOpen] = (0, $3sv40$react.useState)(false); // state for visibility
    const toggleSubmenu = ()=>{
        setIsOpen(!isOpen);
    };
    let content;
    if (props.type == "driver") content = /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
        children: /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("h1", {
            children: "Driver Menu"
        })
    });
    else content = /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
        children: /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("h1", {
            children: "Session Menu"
        })
    });
    return /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
        id: "submenu-card",
        className: `submenu-card ${isOpen ? "active" : ""}`,
        children: /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsxs)("div", {
            className: "submenu-content",
            children: [
                props.type === "driver" && /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
                    children: content
                }),
                props.type === "session" && /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
                    children: content
                })
            ]
        })
    });
}
function $da11a1101b2a894a$var$App() {
    const [submenuType, setSubmenuType] = (0, $3sv40$react.useState)(null); // state for submenu type (driver/session)
    const toggleSubmenu = (type)=>{
        console.log("toggleSubmenu called"); // not working, investigate
        setSubmenuType(type);
    };
    return /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsxs)("div", {
        className: "App",
        children: [
            /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
                className: "curb left"
            }),
            /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsxs)("div", {
                className: "content",
                children: [
                    /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("h1", {
                        className: "display-1",
                        children: "Formula 1 Qualif-AI"
                    }),
                    /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("p", {
                        style: {
                            marginTop: "5%",
                            marginBottom: "10%"
                        },
                        children: "Predict Result For:"
                    }),
                    /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
                        className: "row"
                    }),
                    /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)($da11a1101b2a894a$var$Submenu, {
                        type: submenuType
                    })
                ]
            }),
            /*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)("div", {
                className: "curb right"
            })
        ]
    });
}
var $da11a1101b2a894a$export$2e2bcd8739ae039 = $da11a1101b2a894a$var$App;



const $4fa36e821943b400$var$root = (0, ($parcel$interopDefault($3sv40$reactdomclient))).createRoot(document.getElementById("root")); // Target the 'root' div in index.html
$4fa36e821943b400$var$root.render(/*#__PURE__*/ (0, $3sv40$reactjsxruntime.jsx)((0, $da11a1101b2a894a$export$2e2bcd8739ae039), {}));


//# sourceMappingURL=main.js.map
