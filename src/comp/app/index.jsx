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

ReactDOM.render(<App/>, document.querySelector("#app"));

