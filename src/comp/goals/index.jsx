import React from 'react';
import ReactDOM from 'react-dom';

import GoalsList from './list';

ReactDOM.render(<GoalsList url="/api/v1/goals/" />, document.querySelector("#goals"));

