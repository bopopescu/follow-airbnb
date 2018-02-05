import React, { Component } from 'react';
import logo from './airbnb.png';
import './App.css';

import AddRental from './AddRental'
import ViewRentals from './ViewRentals'

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Follow Airbnb Rentals</h1>
        </header>
        <div className="Views">
          <AddRental/>
          <ViewRentals/>
        </div>
      </div>
    );
  }
}

export default App;
