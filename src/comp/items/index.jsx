import React from 'react';
import ReactDOM from 'react-dom';

import ItemsList from './list';

let elem = document.getElementById("items");
if (elem) ReactDOM.render(<ItemsList />, elem);
