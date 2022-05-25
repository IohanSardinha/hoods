import React, { Component } from "react";

export default class About extends Component{
    render(){
        return(
            <div>
                <div className="row">
                    <div className="col-2">
                        <img src={`${process.env.PUBLIC_URL}/hoods.png`}></img>
                    </div>
                    <div className="col">
                        <h1 className="display-3">HOODS</h1>
                        <p className="lead">HOusing Open Data Survey (or just a bad Google Maps implementation)</p>
                    </div>
                </div>
                <hr />
                <h3>How does this work?</h3>
                <p>Enter the address of your workplace in the search bar, select your interests if any and press search. Our sophisticated system will compute which areas of Barcelona better suit your needs!</p>
                <h3>About us</h3>
                <p>We are a team of dedicated students with the goal of helping people moving to their city of dreams!</p>
                <h3>I don't like this application!</h3>
                <p>You are free to use <a href="https://www.google.com/maps">Google Maps</a> (which is probably better btw)</p>
            </div>
        )
    }
}