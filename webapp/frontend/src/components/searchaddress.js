import React, { useState, useEffect } from "react";
import axios from 'axios';
import { withRouter } from "react-router";
import { Autocomplete, GoogleMap, LoadScript } from "@react-google-maps/api";
import { useForm, useFormState } from "react-hook-form";


const libs = ['places']
const search_keys = ['geometry.location', 'formatted_address']
const MAPS_API_KEY = "API KEY HERE"

const bounds = {
    south: 41.3451778,
    north: 41.469615,
    east: 2.2285723,
    west: 2.0768881
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
                    <form className="row" input='submit' onSubmit={handleSubmit(onSubmit)}>
                        <div className="col-10 form-group" >
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
                        <div className="col-2">
                            <button type='submit' className="btn btn-lg btn-outline-success mb-3">Search</button>
                        </div>
                        <div classname='row'>
                        <p className="lead">Quality of Life Priorites</p>
                            <div class="form-check form-check-inline">
                                <input {...register('restCheck')} class="form-check-input" type="checkbox" id="inlineCheckbox1" value="option1" />
                                <label class="form-check-label" for="inlineCheckbox1">Restaurants & Cafés</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input {...register('nightCheck')} class="form-check-input" type="checkbox" id="inlineCheckbox2" value="option2" />
                                <label class="form-check-label" for="inlineCheckbox2">Bars & Nightlife</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input {...register('playCheck')} class="form-check-input" type="checkbox" id="inlineCheckbox3" value="option3" />
                                <label class="form-check-label" for="inlineCheckbox3">Playgrounds & Parks</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input {...register('seeCheck')} class="form-check-input" type="checkbox" id="inlineCheckbox3" value="option3" />
                                <label class="form-check-label" for="inlineCheckbox3">Closeness to Sea</label>
                            </div>

                        </div>
                    </form>
                </div>
                <GoogleMap
                    id="circle-example"
                    mapContainerStyle={{
                        height: "400px",
                        width: "800px"
                    }}
                    zoom={15}
                    center={current_center}
                />
            </LoadScript>
        </>
    );
}

export default withRouter(SearchAddress);