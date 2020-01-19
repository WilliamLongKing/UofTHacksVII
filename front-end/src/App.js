import React from 'react';
import {render} from 'react-dom';
import './App.css';
import BarChart from './BarChart.js';

function App() {
  return (
    <div className="App">
      <BarChart id='BarChart' />
    </div>
  );
}

render(
  <App />,
  document.getElementById('root')
);

export default App;