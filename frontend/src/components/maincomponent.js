import React, { useState } from "react";
import axios from 'axios';
import { withRouter } from "react-router";
import { Autocomplete, GoogleMap, Marker, LoadScript } from "@react-google-maps/api";
import { useForm } from "react-hook-form";
import { Dropdown } from 'react-bootstrap';
import PolyBarrio from './polybarrio'

import polys from '../json/polys.json'
import lambda_response from '../json/lambda_response.json'

const libs = ['places']
const search_keys = ['geometry.location', 'formatted_address']

const center = { lat: 41.3874, lng: 2.1686 }

const bounds = {
    south: 41.3451778,
    north: 41.469615,
    east: 2.2285723,
    west: 2.0768881
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

function MainComponent() {

    const { register, handleSubmit, formState: { errors } } = useForm({ reValidateMode: 'onChange' });

    const [MAPS_API_KEY, setAPIKey] = useState(process.env.REACT_APP_MAPS_API_KEY)

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

    const validateInBarcelona = async () => {

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

export default withRouter(MainComponent);