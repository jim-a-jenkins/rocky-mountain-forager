import React, { Component } from "react";
import './App.css';
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import NavigationBar from "./navigation/Navbar";


class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      treesList: [],
      shrubsList: [],
      herbsList: [],
      lichensList: [],
      poisonousList: [],
    };
  }

  componentDidMount() {
    this.fetchPlants();
  }

  fetchPlants = () => {
    axios
      .get("/api/v1/plants?group=Trees")
      .then((res) => this.setState({ treesList: res.data }))
      .catch((err) => console.log(err));
    axios
      .get("/api/v1/plants?group=Shrubs")
      .then((res) => this.setState({ shrubsList: res.data }))
      .catch((err) => console.log(err));
    axios
      .get("/api/v1/plants?group=Herbs")
      .then((res) => this.setState({ herbsList: res.data }))
      .catch((err) => console.log(err));
    axios
      .get("/api/v1/plants?group=Lichens")
      .then((res) => this.setState({ lichensList: res.data }))
      .catch((err) => console.log(err));
    axios
      .get("/api/v1/plants?poisonous=True")
      .then((res) => this.setState({ poisonousList: res.data }))
      .catch((err) => console.log(err));
  };
  
  render() {
    return (
      <div className='App'>
        <div>
          <NavigationBar />
        </div>
        <div>
          <header className='App-header'>
            <h1>Table of Contents</h1>
            <h2>Trees</h2>
            <List
                list={this.state.treesList}
            />
            <h2>Shrubs</h2>
            <List
                list={this.state.shrubsList}
            />
            <h2>Herbs</h2>
            <List
                list={this.state.herbsList}
            />
            <h2>Lichens</h2>
            <List
                list={this.state.lichensList}
            />
            <h2>Poisonous Look-Alikes</h2>
            <List
                list={this.state.poisonousList}
            />
          </header>
        </div>
      </div>
    );
  }
}

const List = ({ list }) => (
  <ul>
      {list.map((item) => (
          <Item
              key={item.objectID}
              item={item}
          />
      ))}
  </ul>
);

const Item = ({item}) => (
  <li className='item'>
    <span style={{ width: '30%' }}>{item.name}</span>
  </li>
);

// Components
// 1. Navbar (navbar + sidebar for library)
// 2. Table of contents
// 3. Plant
// 4. Game Setup
// 5. Flashcard (single card) 
// 6. Account Details
// 7. Create Account
// 8. Forgot password
// 9. Cookies warning modal

export default App;
