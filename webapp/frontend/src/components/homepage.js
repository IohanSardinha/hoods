import React, { Component } from "react";
import SearchAddress from "./searchaddress";

export default class Homepage extends Component{
    render(){
        return(
            <div>
                <img src={`${process.env.PUBLIC_URL}/hoods.png`}></img>
                <h1>HOODS</h1>
                <p className="lead">HOusing Open Data Survey (or just a bad Google Maps implementation)</p>
                <hr />
                <SearchAddress />
            </div>
        )
    }
}