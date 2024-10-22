import React from "react";
import CloseButton from "./CloseButton"

export default function DriverMenu(props){


    return (
        <div>
            <div className="col" id="submenu-column">
                <div className="row" id="driver-submenu-top">
                    <label className="input-label" for="Driver">Driver</label>
                    <CloseButton closeSubmenu={props.closeSubmenu}/>
                </div>
                
                <input type="text" id="Driver" placeholder="Ex. LEC, SAI" className="input-field"></input>
            </div>
        </div>
    )
}