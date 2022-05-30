import React, { useState } from "react";
import axios from 'axios';
import { Polygon } from "@react-google-maps/api";
import BarrioWindow from './barriowindow'

import barrioinfo from "../json/barrioinfo.json"

const scoreToColor = (score) => {
    if(score === "---"){
        return '#ffffff'
    } else {
        if (score > 4) return '#009900'
        else if (score > 3) return '#80ff00'
        else if (score > 2) return '#ffff00'
        else if (score > 1) return '#ff9900'
        else return '#ff0000'
    }
}

function PolyBarrio(key, paths, barrioScore){
    const [modalShow, setModalShow] = useState(false);

    const [barrioData, setBarrioData] = useState(barrioinfo);

    const options = {
        fillColor: scoreToColor(barrioScore.score),
        strokeOpacity: 1,
        strokeWeight: 1,
        clickable: true,
        draggable: false,
        editable: false,
        geodesic: false,
        zIndex: 1
    }

    const clickHandler = () => {
        axios
            .get('https://dcfsiax4ti.execute-api.eu-west-1.amazonaws.com/test/Hoods-backend', {params: {id: key-1}})
            .then((res) => {
                if (res.data) {
                    setBarrioData(res.data);
                    setModalShow(true);
                }
            });
    }

    return(
        <>
            <Polygon
                key={key}
                paths={paths}
                options={options}
                onClick={clickHandler}
            ></Polygon>
            <BarrioWindow 
                key={key+100}
                barrioscore={barrioScore}
                barriodata={barrioData}
                show={modalShow}
                onHide={() => setModalShow(false)}
            />
        </>
    )
}

export default PolyBarrio;