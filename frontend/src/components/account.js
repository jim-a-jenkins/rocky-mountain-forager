import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import FlashcardsDataService from '../services/flashcards-service';

const Account = props => {
    const[scores, setScores] = useState([]);

    useEffect(() =>{
        retrieveScores();
    }, [props.token]);

    const retrieveScores = () => {
        FlashcardsDataService.getAllScores(props.token)
        .then(response => {
            setScores(response.data);
        })
        .catch(e => {
            console.log(e);
        })
    }

    return(
        <div>
            <header className='App-header'>
                <h1>Account</h1>
                <h2>Previous Scores</h2>
            </header>
            <div className='Scores-table'>
                <Table striped bordered hover size='sm'>
                    <thead>
                    <tr>
                        <th>#</th>
                        <th>Score</th>
                        <th>Date</th>
                    </tr>
                    </thead>
                    <tbody>
                    {scores.map(function(score){
                        return (
                            <tr>
                                <td>{score.id}</td>
                                <td>{score.score}</td>
                                <td>{score.date}</td>
                            </tr>
                        )
                    })}
                    </tbody>
                </Table>
            </div>
        </div>
    );
}

export default Account;
