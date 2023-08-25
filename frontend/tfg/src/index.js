import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom'
import RanksOro from './components/ranks/oro'
import RanksPlata from './components/ranks/plata'
import RanksEba from './components/ranks/eba'
import RanksLF1 from './components/ranks/lf1'
import RanksLF2 from './components/ranks/lf2'
import RanksLFChall from './components/ranks/lfchall'
import StatsOro from './components/stats/oro'
import StatsPlata from './components/stats/plata'
import StatsEba from './components/stats/eba'
import StatsLF1 from './components/stats/lf1'
import StatsLF2 from './components/stats/lf2'
import StatsLFChall from './components/stats/lfchall'


const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(

  <Router>
    <Routes>
      <Route path='/' element={<App/>}></Route>
      <Route path='/ranks/oro' element={<RanksOro/>}></Route>
      <Route path='/ranks/plata' element={<RanksPlata/>}></Route>
      <Route path='/ranks/eba' element={<RanksEba/>}></Route>
      <Route path='/ranks/lf1' element={<RanksLF1/>}></Route>
      <Route path='/ranks/lf2' element={<RanksLF2/>}></Route>
      <Route path='/ranks/lfchall' element={<RanksLFChall/>}></Route>

      <Route path='/stats/oro' element={<StatsOro/>}></Route>
      <Route path='/stats/plata' element={<StatsPlata/>}></Route>
      <Route path='/stats/eba' element={<StatsEba/>}></Route>
      <Route path='/stats/lf1' element={<StatsLF1/>}></Route>
      <Route path='/stats/lf2' element={<StatsLF2/>}></Route>
      <Route path='/stats/lfchall' element={<StatsLFChall/>}></Route>
    </Routes>
  </Router>

);


