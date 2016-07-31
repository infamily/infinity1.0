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

      this.setState({goals: goals});

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
      {this.state.goals}
      </div>
    )
  }
}


class IdeasList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ideas: []
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

      this.setState({ideas: ideas});

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
      {this.state.ideas}
      </div>
    )
  }

}

class ItemsList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      default_component: <GoalsList url="/api/v1/goals/" />,
      is_idea: false,
      is_goal: true,
      is_plan: false
    };

    this.showGoals = this.showGoals.bind(this);
    this.showIdeas = this.showIdeas.bind(this);
  }

  showGoals() {
    this.setState({
      default_component: <GoalsList url="/api/v1/goals/" />,
      is_idea: false,
      is_goal: true,
      is_plan: false
    });
  }

  showIdeas() {
    this.setState({
      default_component: <IdeasList url="/api/v1/ideas/" />,
      is_idea: true,
      is_goal: false,
      is_plan: false
    });
  }

  showPlans() {}

  render() {
    return(
      <div>
      <a href="#" clasName={this.state.is_goal ? "active":"inactive"} onClick={this.showGoals}>Goals</a>
      <a href="#" onClick={this.showIdeas}>Ideas</a>
      <a href="#" onClick={this.showPlans}>Plans</a>

      {this.state.default_component}
      </div>
    )
  }
}

export default ItemsList;
