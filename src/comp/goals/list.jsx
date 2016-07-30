import React from 'react';
import $ from 'jquery';


class Goal extends React.Component {
  render() {
    let is_link = (()=> {
      if (this.props.isLink) {
        return <span className="badge">link</span>
      }
    })();

    return (
      <div>
      {is_link}<a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount} comments)
      <p>{this.props.shortContent}</p>
      </div>
    )
  }
}


class GoalsList extends React.Component {
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


export default GoalsList;
