import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';


export class App extends React.Component {
  render() {
    return (
      <div>
      Hello, Test!
      </div>
    )
  }
}

let elem = document.getElementById("app");
if (elem) ReactDOM.render(<App/>, elem);
