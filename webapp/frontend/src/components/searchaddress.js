import React, { useState } from "react";
import axios from 'axios';
import { withRouter } from "react-router";
import { Autocomplete, GoogleMap, Marker, Polygon, LoadScript } from "@react-google-maps/api";
import { useForm } from "react-hook-form";
import { Dropdown, Modal } from 'react-bootstrap';
import Plot from 'react-plotly.js';

import polys from '../json/polys.json'
import lambda_response from '../json/lambda_response.json'
import barrioinfo from "../json/barrioinfo.json"


const libs = ['places']
const search_keys = ['geometry.location', 'formatted_address']
const MAPS_API_KEY = 'AIzaSyCQ48bEnlP5WcNJnsS4Kh9nSwAggf9n7Jg'

const center = { lat: 41.3874, lng: 2.1686 }

const bounds = {
    south: 41.3451778,
    north: 41.469615,
    east: 2.2285723,
    west: 2.0768881
}

const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

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

const LoadingDiv = (props) => {
    return (
        <div style={{position: "absolute", height: "400px", width: "100%", backgroundColor: "gray", opacity: "75%", display: props.show}}>
            <div style={{position: "absolute", top: "50%", left: "49%"}} className="spinner-border text-light" role="status">
                <span className="sr-only"></span>
            </div>
        </div>
    )
}

function BarrioWindow(props) {
    let finalScore;

    if(props.barrioscore.score === "---")
        finalScore = "---";
    else finalScore = parseFloat(props.barrioscore.score).toFixed(1)

    return (
        <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    {capitalizeFirstLetter(String(props.barriodata.Nom_Barri))}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body style={{
                maxHeight: 'calc(100vh - 125px)',
                overflowY: 'auto'
            }}>
                <div className="row">
                    <div className="col-3">
                        <img style={{width: "100%", height: "20vh", objectFit: "cover"}} alt={props.barriodata.Nom_Barri} src={props.barriodata.img}></img>
                    </div>
                    <div className="col">
                        <p>District: <b>{props.barriodata.Nom_Districte}</b></p>
                        <p>
                            {String(props.barriodata.description).substring(0, 300) + " [...]"}
                        </p>
                    </div>
                </div>
                <hr />
                <div className="row">
                    <div className="col">
                        <p className="lead">HOODScore: {finalScore}</p>
                        <ul>
                            <li>Distance from workplace: <b>{props.barrioscore.duration}</b></li>
                            <li>Travel mode: <b>{props.barrioscore.mode}</b></li>
                        </ul>
                        <ul>
                            <li>Restaurants: <b>{props.barriodata.restaurants_num}</b></li>
                            <li>Cafes: <b>{props.barriodata.cafes_num}</b></li>
                            <li>Bars: <b>{props.barriodata.bars_num}</b></li>
                            <li>Parks: <b>{props.barriodata.parks_num}</b></li>
                            <li>Playgrounds: <b>{props.barriodata.playgrounds_num}</b></li>
                            <li>Nightclubs: <b>{props.barriodata.discos_num}</b></li>
                        </ul>
                        <p>Average rent in 2021: <b>{props.barriodata.Preu.y2021}</b></p>
                    </div>
                    <div className="col" style={{borderRight: "1px dashed #333"}}>
                        <Plot
                            data={[
                            {
                                x: [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
                                y: [
                                    props.barriodata.Preu.y2014,
                                    props.barriodata.Preu.y2015,
                                    props.barriodata.Preu.y2016,
                                    props.barriodata.Preu.y2017,
                                    props.barriodata.Preu.y2018,
                                    props.barriodata.Preu.y2019,
                                    props.barriodata.Preu.y2020,
                                    props.barriodata.Preu.y2021,
                                ],
                                type: 'scatter',
                                mode: 'lines',
                                marker: {color: 'blue'},
                            }
                            ]}
                            layout={ {width: 400, height: 300, title: 'Rent price by year'} }
                        />
                    </div>
                </div>
                <hr />
                <h1>News</h1>
                <ul className="list-group">
                    {props.barriodata.news.map((article) => {
                        return (
                            <a href={article.url} className="list-group-item list-group-item-action"><b>{article.title}</b> - {article.date}</a>
                        )
                    })}
                </ul>
            </Modal.Body>
        </Modal>
    );
}

function PolyBarrio(key, paths, barrioScore){
    const [modalShow, setModalShow] = useState(false);

    const [barrioData, setBarrioData] = useState(barrioinfo);

    // const [showInfo, setShowInfo] = useState(true)

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

    // const computeCenter = () => {
    //     return {
    //         lat: (polyBounds.top + polyBounds.bottom) / 2,
    //         lng: (polyBounds.left + polyBounds.right) / 2,
    //     }
    // }

    const clickHandler = () => {
        axios
            .get('https://dcfsiax4ti.execute-api.eu-west-1.amazonaws.com/test/Hoods-backend', {params: {id: key}})
            .then((res) => {
                if (res.data) {
                    setBarrioData(res.data);
                    setModalShow(true);
                }
            });
        //console.log(barrioData);
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

function SearchAddress() {

    const { register, handleSubmit, formState: { errors } } = useForm({ reValidateMode: 'onChange' });

    const [address, setAddress] = useState("")

    const [commuteTime, setCommuteTime] = useState("")

    const [autocomplete, setAutoComplete] = useState(null)

    const [barrioScores, setBarrioScores] = useState(lambda_response)

    const [current_center, setCenter] = useState(center)

    const [showLoadingDiv, setLoadingDiv] = useState("none")

    const [showMarker, setShowMarker] = useState(false)
    
    const [markerPosition, setMarkerPosition] = useState(center)

    let i = 0;

    const onLoadComplete = (ac) => {
        setAutoComplete(ac)
    }

    const onChangeAddress = (e) => {
        setAddress(e.target.value);
    }

    const onChangeCommuteTime = (e) => {
        setCommuteTime(e.target.value);
    }


    const autoCompleteDone = () => {
        setAddress(autocomplete.getPlace().formatted_address)
    }

    const validateInBarcelona = async (value) => {

        if (autocomplete === null || autocomplete.getPlace().geometry === undefined) return false

        const lat = autocomplete.getPlace().geometry.location.lat()
        const long = autocomplete.getPlace().geometry.location.lng()
        return (long <= bounds['east'] && long >= bounds['west'] && lat >= bounds['south'] && lat <= bounds['north'])

    }

    const onSubmit = async (e) => {
        setCenter(center)
        setShowMarker(false)
        setLoadingDiv("block")
        //console.log(e)
        axios
            .get('https://8z6g2k40mj.execute-api.eu-west-1.amazonaws.com/default/hoods_scores', {params: e})
            .then((res) => {
                if (res.data) {
                    setCenter({ lat: autocomplete.getPlace().geometry.location.lat(), lng: autocomplete.getPlace().geometry.location.lng() })
                    setMarkerPosition({ lat: autocomplete.getPlace().geometry.location.lat(), lng: autocomplete.getPlace().geometry.location.lng() })
                    setShowMarker(true)
                    setLoadingDiv("none")
                    setBarrioScores(res.data)
                    // console.log(res.data)
                }
            });
    }

    return (
        <>
            <div></div>
            <LoadScript libraries={libs} googleMapsApiKey={MAPS_API_KEY}>
                <div>
                    <form className="row mb-3" input='submit' onSubmit={handleSubmit(onSubmit)}>
                        <div className="col-6 form-group" >
                            <Autocomplete fields={search_keys} onLoad={onLoadComplete} onPlaceChanged={autoCompleteDone}>
                                <input
                                    {...register('origin', { validate: validateInBarcelona, required: true })}
                                    className={`form-control ${errors.addressField ? 'is-invalid' : ''}`}
                                    value={address}
                                    placeholder="Search an Address in Barcelona"
                                    type='text'
                                    onChange={onChangeAddress}
                                >
                                </input>
                            </Autocomplete>
                            <div className="text-danger"><small>{errors.addressField && "Address must be in Barcelona"}</small></div>
                        </div>
                        <div className="col">
                            <input
                                {...register('max_commute_time')}
                                className="form-control"
                                value={commuteTime}
                                placeholder="Max commute time (mins)"
                                type='number'
                                onChange={onChangeCommuteTime}
                            >
                            </input>
                        </div>
                        <div className="col">
                            <Dropdown>
                                <Dropdown.Toggle className="w-100" variant="success" id="dropdown-basic">
                                    Priorities
                                </Dropdown.Toggle>

                                <Dropdown.Menu>
                                    <div className="px-2">
                                        <div className="form-check form-check-inline">
                                            <input {...register('restaurants')} className="form-check-input" type="checkbox" id="inlineCheckbox1"/>
                                            <label className="form-check-label" htmlFor="inlineCheckbox1">Restaurants & Cafés</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input {...register('bars')} className="form-check-input" type="checkbox" id="inlineCheckbox2"/>
                                            <label className="form-check-label" htmlFor="inlineCheckbox2">Bars & Nightlife</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input {...register('parks')} className="form-check-input" type="checkbox" id="inlineCheckbox3"/>
                                            <label className="form-check-label" htmlFor="inlineCheckbox3">Playgrounds & Parks</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input className="form-check-input" type="checkbox" id="inlineCheckbox4" value="option4" />
                                            <label className="form-check-label" htmlFor="inlineCheckbox4">Closeness to Sea</label>
                                        </div>
                                    </div>
                                </Dropdown.Menu>
                            </Dropdown>
                        </div>
                        <div className="col-2">
                            <button type='submit' className="btn btn-block btn-outline-success w-100">Search</button>
                        </div>
                    </form>
                </div>
                <div style={{position: "relative"}}>
                    <GoogleMap
                        id="circle-example"
                        mapContainerStyle={{
                            position: "absolute",
                            height: "400px",
                            width: "100%"
                        }}
                        zoom={13.7}
                        center={current_center}
                        clickableIcons={false}
                        heading={false}
                        keyboardShortcuts={false}
                    >
                        <Marker
                            visible={showMarker}
                            position={markerPosition}
                        />
                        {polys.map((poly) => {
                            i = i + 1;
                            return PolyBarrio(i, poly.points, barrioScores[i-1])
                        })}
                    </GoogleMap>
                    <LoadingDiv show={showLoadingDiv}></LoadingDiv>
                </div>
            </LoadScript>
        </>
    );
}

export default withRouter(SearchAddress);