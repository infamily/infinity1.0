import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';


export class Goals extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      title: ''
    };
  }

  componentDidMount() {
    this.serverRequest = $.get(this.props.url, function (result) {
      this.setState({title: result.results[0].title});
    }.bind(this));
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    console.log(this.state);
    return (
      <div>
      Hello, {this.state.title}!
      </div>
    )
  }
}

ReactDOM.render(<Goals url="/api/v1/goals/" />, document.querySelector("#goals"));

