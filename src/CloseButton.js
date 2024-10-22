import React from 'react';
import arrowImage from "./images/arrow1.png";

export default function (props){

    function handleClick(){
        props.closeSubmenu()
    }

    return (
        <img src={arrowImage} className="back-image" onClick={handleClick}/>
    )
}