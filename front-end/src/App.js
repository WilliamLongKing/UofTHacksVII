import React from 'react';
import {render} from 'react-dom';
import './App.css';
import ApexChart from './BarChart.js';

function App() {
  return (
    <div className="App">
      <ApexChart/>
    </div>
  );
}

render(
  <App />,
  document.getElementById('root')
);

export default App;