import React, { Component } from "react";
import axios from 'axios';
import { withRouter } from "react-router";

const Alert = () => (
    <div className="alert alert-success" role="alert">
        Response received!
    </div>
)

class SearchAddress extends Component {
    constructor(props){
        super(props);

        this.onChangeAddress = this.onChangeAddress.bind(this);
        this.onSubmit = this.onSubmit.bind(this);

        this.state = {
            address: "",
            alertVisible: false,
        };
    }

    onChangeAddress(e){
        this.setState({
            address: e.target.value,
        });
    }

    onSubmit(e){
        e.preventDefault();

        axios
            .get('http://localhost:8000/test/')
            .then((res) => {
                if(res.data){
                    this.setState({
                        alertVisibile: true,
                    });
                    setTimeout(() => {
                        this.setState({
                            alertVisibile: false,
                        })
                    }, 3000);
                }
            });
    }

    render(){
        return (
            <div>
                <h1 className="display-6">Search an address</h1>
                <form className="row" onSubmit={this.onSubmit}>
                    <div className="col-10">
                        <input 
                            type="text" 
                            className="form-control form-control-lg" 
                            placeholder="Address" 
                            value={this.state.address}
                            onChange={this.onChangeAddress}
                        />                    
                    </div>
                    <div className="col-2">
                        <button type="submit" className="btn btn-lg btn-outline-success mb-3">Search</button>
                    </div>
                </form>
                {this.state.alertVisibile ? <Alert /> : null}
            </div>
        );
    }
}

export default withRouter(SearchAddress);