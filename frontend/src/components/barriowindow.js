import React from "react";
import Plot from 'react-plotly.js';
import { Modal } from 'react-bootstrap';

const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function BarrioWindow(props) {
    let finalScore;

    if(props.barrioscore.score === "---")
        finalScore = "---";
    else finalScore = parseFloat(props.barrioscore.score).toFixed(1)

    return (
        <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    {capitalizeFirstLetter(String(props.barriodata.Nom_Barri))}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body style={{
                maxHeight: 'calc(100vh - 125px)',
                overflowY: 'auto'
            }}>
                <div className="row">
                    <div className="col-3">
                        <img style={{width: "100%", height: "20vh", objectFit: "cover"}} alt={props.barriodata.Nom_Barri} src={props.barriodata.img}></img>
                    </div>
                    <div className="col">
                        <p>District: <b>{props.barriodata.Nom_Districte}</b></p>
                        <p>
                            {String(props.barriodata.description).substring(0, 300) + " [...]"}
                        </p>
                    </div>
                </div>
                <hr />
                <div className="row">
                    <div className="col">
                        <p className="lead">HOODScore: {finalScore}</p>
                        <ul>
                            <li>Distance from workplace: <b>{props.barrioscore.duration}</b></li>
                            <li>Travel mode: <b>{props.barrioscore.mode}</b></li>
                        </ul>
                        <ul>
                            <li>Restaurants: <b>{props.barriodata.restaurants_num}</b></li>
                            <li>Cafes: <b>{props.barriodata.cafes_num}</b></li>
                            <li>Bars: <b>{props.barriodata.bars_num}</b></li>
                            <li>Parks: <b>{props.barriodata.parks_num}</b></li>
                            <li>Playgrounds: <b>{props.barriodata.playgrounds_num}</b></li>
                            <li>Nightclubs: <b>{props.barriodata.discos_num}</b></li>
                        </ul>
                        <p>Average rent in 2021: <b>{props.barriodata.Preu.y2021}</b></p>
                    </div>
                    <div className="col" style={{borderRight: "1px dashed #333"}}>
                        <Plot
                            data={[
                            {
                                x: [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
                                y: [
                                    props.barriodata.Preu.y2014,
                                    props.barriodata.Preu.y2015,
                                    props.barriodata.Preu.y2016,
                                    props.barriodata.Preu.y2017,
                                    props.barriodata.Preu.y2018,
                                    props.barriodata.Preu.y2019,
                                    props.barriodata.Preu.y2020,
                                    props.barriodata.Preu.y2021,
                                ],
                                type: 'scatter',
                                mode: 'lines',
                                marker: {color: 'blue'},
                            }
                            ]}
                            layout={ {width: 400, height: 300, title: 'Rent price by year'} }
                        />
                    </div>
                </div>
                <hr />
                <h1>News</h1>
                <ul className="list-group">
                    {props.barriodata.news.map((article) => {
                        return (
                            <a href={article.url} className="list-group-item list-group-item-action"><b>{article.title}</b> - {article.date}</a>
                        )
                    })}
                </ul>
            </Modal.Body>
        </Modal>
    );
}

export default BarrioWindow;