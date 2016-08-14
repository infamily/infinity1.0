import React from 'react';
import $ from 'jquery';
import Paper from 'material-ui/Paper';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Badge from 'material-ui/Badge';
import RaisedButton from 'material-ui/RaisedButton';
import RefreshIndicator from 'material-ui/RefreshIndicator';
import LinearProgress from 'material-ui/LinearProgress';
import AppBar from 'material-ui/AppBar';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';

// Include component styles
require("./list.css")


class Goal extends React.Component {
  render() {
    let is_link = (()=> {
      if (this.props.isLink) {
        return (
          <div>
          <Badge badgeContent="Link" primary={true} />
          <a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})
          </div>
        )
      } else {
        return (<div><a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})</div>)
      }
    })();

    return (
      <Card>
        <CardHeader
          title={is_link}
          subtitle={this.props.shortContent}
        />
      </Card>
    )
  }
}


class Plan extends React.Component {
  render() {
    let is_link = (()=> {
      if (this.props.isLink) {
        return (
          <div>
          <Badge badgeContent="Link" primary={true} />
          <a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})
          </div>
        )
      } else {
        return (<div><a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})</div>)
      }
    })();

    return (
      <Card>
        <CardHeader
          title={is_link}
          subtitle={this.props.shortContent}
        />
      </Card>
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
          <a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})
          </div>
        )
      } else {
        return (<div><a href={this.props.detailUrl}>{this.props.title}</a> ({this.props.commentsCount})</div>)
      }
    })();

    return (
      <Card>
        <CardHeader
          title={is_link}
          subtitle={this.props.shortContent}
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
      description: '',
      loading: true,
      types: {}
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

      this.setState({goals: goals, description: result.description, loading: false, types: result.types});

    }.bind(this));
  }

  componentDidMount() {
    this.getGoals();
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    const style = {
      container: {
        position: 'relative',
      },
      refresh: {
        display: 'inline-block',
        position: 'relative',
        marginLeft: '50%'
      },
    };

    let goals = (
      <div>
      <center><h3>{this.state.description}</h3></center>
      {this.state.goals}
      </div>
    )

    let refreshIndicator = (
      <RefreshIndicator
      size={50}
      left={-20}
      top={0}
      loadingColor={"#FF9800"}
      status="loading"
      style={style.refresh}
      />
    )

    if (this.state.loading) {
      return refreshIndicator;
    } else {
      return goals;
    }
  }
}

class PlansList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      plans: [],
      description: '',
      loading: true,
      types: {}
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

      this.setState({plans: plans, description: result.description, loading: false, types: result.types});

    }.bind(this));
  }

  componentDidMount() {
    this.getPlans();
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    const style = {
      container: {
        position: 'relative',
      },
      refresh: {
        display: 'inline-block',
        position: 'relative',
        marginLeft: '50%'
      },
    };
    let plans = (
      <div>
      <center><h3>{this.state.description}</h3></center>
      {this.state.plans}
      </div>
    )

    let refreshIndicator = (
      <RefreshIndicator
      size={50}
      left={-20}
      top={0}
      loadingColor={"#FF9800"}
      status="loading"
      style={style.refresh}
      />
    )

    if (this.state.loading) {
      return refreshIndicator;
    } else {
      return plans;
    }
  }

}

class IdeasList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ideas: [],
      description: '',
      loading: true,
      types: {}
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

      this.setState({ideas: ideas, description: result.description, loading: false, types: result.types});

    }.bind(this));
  }

  componentDidMount() {
    this.getIdeas();
  }

  componentWillUnmount() {
    this.serverRequest.abort();
  }

  render() {
    const style = {
      container: {
        position: 'relative',
      },
      refresh: {
        display: 'inline-block',
        position: 'relative',
        marginLeft: '50%'
      },
    };

    let ideas = (
      <div>
      <center><h3>{this.state.description}</h3></center>
      {this.state.ideas}
      </div>
    )

    let refreshIndicator = (
      <RefreshIndicator
      size={50}
      left={-20}
      top={0}
      loadingColor={"#FF9800"}
      status="loading"
      style={style.refresh}
      />
    )

    if (this.state.loading) {
      return refreshIndicator;
    } else {
      return ideas;
    }
  }

}

class ItemsList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      default_component: <GoalsList url="/api/v1/goals/" />,
      plans_is_active: false,
      goals_is_active: true,
      ideas_is_active: false,
      types: {}
    };

    this.showGoals = this.showGoals.bind(this);
    this.showIdeas = this.showIdeas.bind(this);
    this.showPlans = this.showPlans.bind(this);

    this.serverRequest = $.get("/api/v1/goals/", function (result) {
      this.setState({types: result.types});
    }.bind(this));
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
        return "btn btn-primary";
      }
      return "btn";
    }

    if (menu_item == "goals") {
      if (this.state.goals_is_active) {
        return "btn btn-primary";
      }
      return "btn";
    }

    if (menu_item == "ideas") {
      if (this.state.ideas_is_active) {
        return "btn btn-primary";
      }

      return "btn";
    }
  }

  render() {
    const style = {
        margin: 0,
        top: 'auto',
        right: 20,
        bottom: 20,
        left: 'auto',
        position: 'fixed',
    };

    let create_link = (()=>{
      if (this.state.goals_is_active) {
        return (
          <FloatingActionButton style={style} href="/goal-create/">
          <ContentAdd />
          </FloatingActionButton>
        )
      }

      if (this.state.ideas_is_active) {
        return (
          <FloatingActionButton style={style} href="/idea-create/">
          <ContentAdd />
          </FloatingActionButton>
        )
      }

      if (this.state.plans_is_active) {
        return (
          <FloatingActionButton style={style} href="/plan-create/">
          <ContentAdd />
          </FloatingActionButton>
        )
      }
    })();

    return(
      <div>
        <div className="btn-group btn-group-justified btn-group-raised" role="group">
          <a href="#" onClick={this.showGoals} className={this.isActive("goals")}>{this.state.types.problem}</a>
          <a href="#" onClick={this.showIdeas} className={this.isActive("ideas")}>{this.state.types.solution}</a>
          <a href="#" onClick={this.showPlans} className={this.isActive("plans")}>{this.state.types.project}</a>
        </div>

        {this.state.default_component}
        {create_link}

      </div>
    )
  }
}

export default ItemsList;
