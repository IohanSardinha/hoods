import React, { useState } from "react";
import axios from 'axios';
import { withRouter } from "react-router";
import { Autocomplete, GoogleMap, LoadScript } from "@react-google-maps/api";
import { useForm } from "react-hook-form";


const libs = ['places']
const search_keys = ['geometry.location', 'formatted_address']
const MAPS_API_KEY = "<Your API Key here>"

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


    const onLoadComplete = (ac) => {
        setAutoComplete(ac)
    }



    const onChangeAddress = (e) => {
        setAddress(e.target.value);
    }

    const autoCompleteDone = async () => {
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
                    <h1 className="display-6">Search an address</h1>
                    <form className="row" onSubmit={handleSubmit(onSubmit)}>
                        <div className="col-10 form-group" >
                            <Autocomplete fields={search_keys} onLoad={onLoadComplete} onPlaceChanged={autoCompleteDone}>
                                <input
                                    {...register('addressField', { validate: validateInBarcelona, required: true })}
                                    type="text"
                                    className={`form-control ${errors.addressField ? 'is-invalid' : ''}`}
                                    placeholder="Address"
                                    value={address}
                                    onChange={onChangeAddress}
                                >
                                </input>
                            </Autocomplete>
                            <div className="text-danger"><small>{errors.addressField && "Address must be in Barcelona"}</small></div>
                        </div>
                        <div className="col-2">
                            <button onSubmit={onSubmit} type="submit" className="btn btn-lg btn-outline-success mb-3">Search</button>
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