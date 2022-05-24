import React, { Component } from "react";
import SearchAddress from "./searchaddress";

export default class Homepage extends Component{
    render(){
        return(
            <div>
                <h1>HOODS</h1>
                <p className="lead">HOusing Open Data Survey (or just a bad Google Maps implementation)</p>
                <hr />
                <SearchAddress />
            </div>
        )
    }
}