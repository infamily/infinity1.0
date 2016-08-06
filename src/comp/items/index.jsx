import React from 'react';
import ReactDOM from 'react-dom';
import injectTapEventPlugin from 'react-tap-event-plugin';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';


import ItemsList from './list';

let elem = document.getElementById("items");

const App = () => (
  <MuiThemeProvider>
    <ItemsList />
  </MuiThemeProvider>
);

if (elem) ReactDOM.render(<App />, elem);
injectTapEventPlugin();
