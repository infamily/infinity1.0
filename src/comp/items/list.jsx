import React from 'react';
import $ from 'jquery';

// Include component styles
require("./list.css")


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


class Idea extends React.Component {
  render() {
    return (
      <div>
      {this.props.title}
      </div>
    );
  }
}


class GoalsList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      goals: [],
      description: ''
    };
  }

  getGoals() {
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

      this.setState({goals: goals, description: result.description});

    }.bind(this));
  }

  componentDidMount() {
    this.getGoals();
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    return (
      <div>
      <center><h2>{this.state.description}</h2></center>
      {this.state.goals}
      </div>
    )
  }
}


class IdeasList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ideas: [],
      description: ''
    };
  }

  getIdeas() {
    this.serverRequest = $.get(this.props.url, function (result) {
      let ideas = result.results.map((item)=>{
        return (
          <Idea
          title={item.title}
          />
        )
      });

      this.setState({ideas: ideas, description: result.description});

    }.bind(this));
  }

  componentDidMount() {
    this.getIdeas();
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    return (
      <div>
      <center><h2>{this.state.description}</h2></center>
      {this.state.ideas}
      </div>
    )
  }

}

class ItemsList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      default_component: <GoalsList url="/api/v1/goals/" />
    };

    this.showGoals = this.showGoals.bind(this);
    this.showIdeas = this.showIdeas.bind(this);
  }

  showGoals() {
    this.setState({
      default_component: <GoalsList url="/api/v1/goals/" />
    });
  }

  showIdeas() {
    this.setState({
      default_component: <IdeasList url="/api/v1/ideas/" />
    });
  }

  showPlans() {}

  render() {
    return(
      <div>
      <center>
      <div className="btn-group btn-group-lg" role="group" aria-label="Large button group">
        <a href="#" onClick={this.showGoals} className="btn btn-default">Goals</a>
        <a href="#" onClick={this.showIdeas} className="btn btn-default">Ideas</a>
        <a href="#" onClick={this.showPlans} className="btn btn-default">Plans</a>
      </div>
      <h2>{this.state.description}</h2>
      </center>

      {this.state.default_component}
      </div>
    )
  }
}

export default ItemsList;
