import React, { Component } from 'react';
import './App.css'
import Logout from './Logout/Logout';
import Login from './Login/Login';

class App extends Component {
    constructor(props) {
      super(props);
      this.state = {
        isLoggedIn: false
      };
      this.login = this.login.bind(this);
      this.logout = this.logout.bind(this);
    }

    login() {
        this.setState({isLoggedIn: true});
      }
      logout() {
        this.setState({isLoggedIn: false});
      }

      render() {
        if(this.state.isLoggedIn) {
          return this.renderLogin();
        }
        return this.renderLogout();
      }

      renderLogin() {
        return (
          <div>
            <Login />
            <button onClick={this.login}>Login</button>
          </div>
        ); 
      }
    
      renderLogout() {
        return (
          <div>
            <Logout />
              <button onClick={this.logout}>Logout</button>
          </div>
        );
      }
    }