import React from 'react';
import $ from 'jquery';
import Paper from 'material-ui/Paper';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Badge from 'material-ui/Badge';
import RaisedButton from 'material-ui/RaisedButton';

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
      <hr></hr>
      {is_link}<a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})
      <p>{this.props.shortContent}</p>
      </div>
    )
  }
}


class Plan extends React.Component {
  render() {
    let is_link = (()=> {
      if (this.props.isLink) {
        return <span className="badge">link</span>
      }
    })();

    return (
      <div>
      <hr></hr>
      {is_link}<a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})
      <p>{this.props.shortContent}</p>
      </div>
    )
  }
}


class Idea extends React.Component {
  render() {
    let is_link = (()=> {
      if (this.props.isLink) {
        return (
          <div>
          <Badge badgeContent="Link" primary={true} />
          {this.props.title}
          </div>
        )
      } else {
        return (<div>{this.props.title}</div>)
      }
    })();

    let get_content = (()=>{
      return (
        <div>
          <p>{this.props.shortContent}</p>
          <RaisedButton
            label={this.props.commentsCount}
            href={this.props.detailUrl}
          />
        </div>
      )
    })();

    return (
      <Card>
        <CardHeader
          title={is_link}
          subtitle={get_content}
        />
      </Card>
    )
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

class PlansList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      plans: [],
      description: ''
    };
  }

  getPlans() {
    this.serverRequest = $.get(this.props.url, function (result) {
      let plans = result.results.map((item)=>{
        return (
          <Plan
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

      this.setState({plans: plans, description: result.description});

    }.bind(this));
  }

  componentDidMount() {
    this.getPlans();
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    return (
      <div>
      <center><h2>{this.state.description}</h2></center>
      {this.state.plans}
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
          detailUrl={item.detail_url}
          createdAt={item.created_at}
          commentsCount={item.comments_count}
          isLink={item.is_link}
          isHistorical={item.is_historical}
          shortContent={item.short_content}
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
      default_component: <GoalsList url="/api/v1/goals/" />,
      plans_is_active: false,
      goals_is_active: true,
      ideas_is_active: false
    };

    this.showGoals = this.showGoals.bind(this);
    this.showIdeas = this.showIdeas.bind(this);
    this.showPlans = this.showPlans.bind(this);
  }

  showGoals() {
    this.setState({
      default_component: <GoalsList url="/api/v1/goals/" />,
      plans_is_active: false,
      goals_is_active: true,
      ideas_is_active: false
    });
  }

  showIdeas() {
    this.setState({
      default_component: <IdeasList url="/api/v1/ideas/" />,
      plans_is_active: false,
      goals_is_active: false,
      ideas_is_active: true
    });
  }

  showPlans() {
    this.setState({
      default_component: <PlansList url="/api/v1/plans/" />,
      plans_is_active: true,
      goals_is_active: false,
      ideas_is_active: false
    });
  }

  isActive(menu_item) {
    if (menu_item == "plans") {
      if (this.state.plans_is_active) {
        return "btn btn-default active";
      }
      return "btn btn-default";
    }

    if (menu_item == "goals") {
      if (this.state.goals_is_active) {
        return "btn btn-default active";
      }
      return "btn btn-default";
    }

    if (menu_item == "ideas") {
      if (this.state.ideas_is_active) {
        return "btn btn-default active";
      }

      return "btn btn-default";
    }
  }

  render() {
    return(
      <div>
      <center>
      <div className="btn-group btn-group-lg" role="group">
        <a href="#" onClick={this.showGoals} className={this.isActive("goals")}>Goals</a>
        <a href="#" onClick={this.showIdeas} className={this.isActive("ideas")}>Ideas</a>
        <a href="#" onClick={this.showPlans} className={this.isActive("plans")}>Plans</a>
      </div>
      <h2>{this.state.description}</h2>
      </center>

      {this.state.default_component}
      </div>
    )
  }
}

export default ItemsList;
