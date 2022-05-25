import React, { useState, useEffect } from "react";
import axios from 'axios';
import { withRouter } from "react-router";
import { Autocomplete, GoogleMap, Polygon, LoadScript } from "@react-google-maps/api";
import { useForm, useFormState } from "react-hook-form";
import { Dropdown, Modal } from 'react-bootstrap';

import polys from '../json/polys.json'
import lambda_response from '../json/lambda_response.json'


const libs = ['places']
const search_keys = ['geometry.location', 'formatted_address']
const MAPS_API_KEY = ''


const bounds = {
    south: 41.3451778,
    north: 41.469615,
    east: 2.2285723,
    west: 2.0768881
}

const fillColors = ['#ff0000', '#ff9900', '#ffff00', '#80ff00', '#009900']

const scoreToColor = (score) => {
    if (score >= 4.5) return '#009900'
    else if (score >= 3.5) return '#80ff00'
    else if (score >= 2.5) return '#ffff00'
    else if (score >= 1) return '#ff9900'
    else return '#ff0000'
}

function BarrioWindow(props) {
    return (
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Barrio {props.barrioId} Info
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            This barrio is nice!
          </p>
        </Modal.Body>
      </Modal>
    );
}

function PolyBarrio(key, paths, polyBounds, fillColor){
    const [modalShow, setModalShow] = useState(false);

    const options = {
        fillColor: fillColor,
        strokeOpacity: 1,
        strokeWeight: 1,
        clickable: true,
        draggable: false,
        editable: false,
        geodesic: false,
        zIndex: 1
    }

    const computeCenter = () => {
        return {
            lat: (polyBounds.top + polyBounds.bottom) / 2,
            lng: (polyBounds.left + polyBounds.right) / 2,
        }
    }

    const clickHandler = () => {
        setModalShow(true)
        //console.log(computeCenter())
    }

    return(
        <>
            <Polygon
                key={key}
                paths={paths}
                options={options}
                onClick={clickHandler}
            />
            <BarrioWindow 
                barrioId={key}
                show={modalShow}
                onHide={() => setModalShow(false)}
            />
        </>
    )
}

function SearchAddress() {

    const { register, handleSubmit, trigger, formState: { errors } } = useForm({ reValidateMode: 'onChange' });

    const [address, setAddress] = useState("")

    const [autocomplete, setAutoComplete] = useState(null)

    const [current_center, setCenter] = useState({ lat: 41.3874, lng: 2.1686 })

    //useEffect(() => {
    //    const triggerValid = async () => await trigger()
    //    triggerValid()
    //    
    //})

    let i = 0;

    const onLoadComplete = (ac) => {
        setAutoComplete(ac)
    }

    const onChangeAddress = (e) => {
        setAddress(e.target.value);
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
        //setAddress(autocomplete.getPlace().formatted_address)
        setCenter({ lat: autocomplete.getPlace().geometry.location.lat(), lng: autocomplete.getPlace().geometry.location.lng() })
        axios
            .get('http://localhost:8000/test/')
            .then((res) => {
                if (res.data) {

                }
            });
    }

    return (
        <>
            <LoadScript libraries={libs} googleMapsApiKey={MAPS_API_KEY}>
                <div>
                    <form className="row mb-3" input='submit' onSubmit={handleSubmit(onSubmit)}>
                        <div className="col-7 form-group" >
                            <Autocomplete fields={search_keys} onLoad={onLoadComplete} onPlaceChanged={autoCompleteDone}>
                                <input
                                    {...register('addressField', { validate: validateInBarcelona, required: true })}
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
                            <Dropdown>
                                <Dropdown.Toggle className="w-100" variant="success" id="dropdown-basic">
                                    Priorities
                                </Dropdown.Toggle>

                                <Dropdown.Menu>
                                    <div className="px-2">
                                        <div className="form-check form-check-inline">
                                            <input {...register('restCheck')} className="form-check-input" type="checkbox" id="inlineCheckbox1" value="option1" />
                                            <label className="form-check-label" htmlFor="inlineCheckbox1">Restaurants & Cafés</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input {...register('nightCheck')} className="form-check-input" type="checkbox" id="inlineCheckbox2" value="option2" />
                                            <label className="form-check-label" htmlFor="inlineCheckbox2">Bars & Nightlife</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input {...register('playCheck')} className="form-check-input" type="checkbox" id="inlineCheckbox3" value="option3" />
                                            <label className="form-check-label" htmlFor="inlineCheckbox3">Playgrounds & Parks</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input {...register('seeCheck')} className="form-check-input" type="checkbox" id="inlineCheckbox4" value="option4" />
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
                <GoogleMap
                    id="circle-example"
                    mapContainerStyle={{
                        height: "400px",
                        width: "100%"
                    }}
                    zoom={14}
                    center={current_center}
                    clickableIcons={false}
                    heading={false}
                    keyboardShortcuts={false}
                >
                    {polys.map((poly) => {
                        i = i + 1;
                        return PolyBarrio(i, poly.points, poly.bounds, scoreToColor(lambda_response.body[i-1].score))
                    })}
                </GoogleMap>
            </LoadScript>
        </>
    );
}

export default withRouter(SearchAddress);