import React from "react";
import { Route } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";

import Navbar from "./components/navbar";
import Homepage from "./components/homepage";
import About from "./components/about";

const App = () => {
    return (
        <div>
            <Navbar />
            <br />
            <div className="container">
                <Route exact path="/" component={Homepage} />
                <Route exact path="/about" component={About} />
            </div>
            <br />
        </div>
    );
};

export default App;