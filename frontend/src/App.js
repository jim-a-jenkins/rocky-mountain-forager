import React from "react";
import './App.css';
import "bootstrap/dist/css/bootstrap.min.css";
import Library from "./components/library";
import Flashcards from "./components/flashcards";
import Login from "./components/login";
import Account from "./components/account";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import './scss/custom.scss';
import { Routes, Route, Link } from 'react-router-dom';

function App() {
  
  return (
    <div className='App'>
      <div>
        <Navbar bg="primary" variant="dark">
          <Navbar.Brand href="#home">Rocky Mountain Forager</Navbar.Brand>
          <Nav className="me-auto">
              <Link className="nav-link" to={"/library"}>Library</Link>
              <Link className="nav-link" to={"/flashcards"}>Flashcards</Link>
              <Link className="nav-link" to={"/account"}>Account</Link>
              <Link className="nav-link" to={"/logout"}>Logout</Link>
          </Nav>
        </Navbar>
      </div>

      <div className="container mt-4">
        <Routes>
          <Route path="/library" element={<Library/>} />
          <Route path="/flashcards" element={<Flashcards/>} />
          <Route path="/account" element={<Account/>} />
          <Route path="/logout" element={<Login/>} />
        </Routes>
      </div>
    </div>
  );
}



export default App;
