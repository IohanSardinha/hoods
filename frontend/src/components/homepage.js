import React, { Component } from "react";
import SearchAddress from "./searchaddress";

export default class Homepage extends Component{
    render(){
        return(
            <div>
                <div className="row">
                    <div className="col-2">
                        <img src={`${process.env.PUBLIC_URL}/hoods.png`} alt="HOODS Logo"></img>
                    </div>
                    <div className="col">
                        <h1 className="display-3">HOODS</h1>
                        <p className="lead">HOusing Open Data Survey</p>
                    </div>
                </div>
                <hr />
                <SearchAddress />
            </div>
        )
    }
}