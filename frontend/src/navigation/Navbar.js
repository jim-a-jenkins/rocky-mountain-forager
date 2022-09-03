import React from "react"
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import '../scss/custom.scss';

const NavigationBar = () => {
    return (
        <>
        <Navbar bg="primary" variant="dark">
            <Navbar.Brand href="#home">Rocky Mountain Forager</Navbar.Brand>
            <Nav className="me-auto">
                <Nav.Link href="#Library">Library</Nav.Link>
                <Nav.Link href="#Features">Flashcards</Nav.Link>
                <Nav.Link href="#Account">Account</Nav.Link>
                <Nav.Link href="#Logout">Logout</Nav.Link>
            </Nav>
        </Navbar>
        </>
    );
};

export default NavigationBar;
