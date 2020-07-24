import React from 'react';
import logo from './logo.svg';
import './App.css';
import Chatbot from './Components/Chatbot';
import Chatmodule from './Components/Chatmodule';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";


function App() {
  return (
      <Router>
      <div id="App" className="App">
        {/* <Header />   */}
        {/* <SideBar pageWrapId={"page-wrap"} outerContainerId={"App"} /> */}
        {/* <div id="page-wrap"> */}
        <div className="container d-flex align-items-center flex-column">
          <Switch>
            <Route path="/" exact={true}>
              <Chatbot />
            </Route>
            <Route path="/chatmodule" exact={true}>
              <Chatmodule />
            </Route>
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;
