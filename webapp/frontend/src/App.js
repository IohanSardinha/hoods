import React from "react";
import { Route } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";

import Navbar from "./components/navbar";
import Homepage from "./components/homepage";

const App = () => {
    return (
        <div>
            <Navbar />
            <br />
            <div className="container">
                <Route exact path="/" component={Homepage} />
            </div>
            <br />
        </div>
    );
};

export default App;