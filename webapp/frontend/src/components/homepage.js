import React, { Component } from "react";
import SearchAddress from "./searchaddress";

export default class Homepage extends Component{
    render(){
        return(
            <div>
                <h1>GALID</h1>
                <p className="lead">Lorem ipsum dolor sit amet</p>
                <hr />
                <SearchAddress />
            </div>
        )
    }
}