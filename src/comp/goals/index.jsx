import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';


class Goal extends React.Component {
  render() {
    return (
      <div>
      <a href={this.props.detailUrl}>{this.props.title}</a>
      </div>
    )
  }
}


export class GoalsList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      goals: []
    };
  }

  componentDidMount() {
    this.serverRequest = $.get(this.props.url, function (result) {
      let goals = result.results.map((item)=>{
        return (
          <Goal
          title={item.title}
          detailUrl={item.detail_url}
          createdAt={item.created_at}
          commentsCount={item.comments_count}
          isLink={item.is_link}
          isHistorical={item.is_historical}
          shortContent={item.short_content}
          />
        )
      });

      this.setState({goals: goals});

    }.bind(this));
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    return (
      <div>
      {this.state.goals}
      </div>
    )
  }
}

ReactDOM.render(<GoalsList url="/api/v1/goals/" />, document.querySelector("#goals"));

