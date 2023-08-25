import './App.css';
import './components/navbar'
import axios from "axios";
import NavBar from './components/navbar';
import { Component } from 'react';
import Table from 'react-bootstrap/Table';
import ListGroup from 'react-bootstrap/ListGroup';


class App extends Component{

  state = {
    data: [],
    DataisLoaded: false
  }

  getData = () => {
    axios.get("http://localhost:3001/player/2190714")
      .then(data => {
        this.setState({data,DataisLoaded: true});
      })
  }

  translateSeason = (season) => {
      if (season === 2) return "21/22"
      if (season === 3) return "20/21"
      if (season === 4) return "19/20"
      if (season === 5) return "18/19"
      if (season === 6) return "17/18"
      if (season === 7) return "16/17"
      if (season === 8) return "15/16"
      if (season === 9) return "14/15"
      if (season === 10) return "13/14"
      if (season === 11) return "12/13"
      if (season === 12) return "11/12"
      if (season === 13) return "10/11"
      if (season === 14) return "09/10"
      if (season === 15) return "08/09"
      if (season === 16) return "07/08"
      if (season === 17) return "06/07"
      if (season === 18) return "05/06"
      if (season === 19) return "04/05"
      if (season === 20) return "03/04"
      if (season === 21) return "02/03"
      if (season === 22) return "01/02"
      if (season === 23) return "00/01"
      if (season === 24) return "99/00"
      if (season === 25) return "98/99"
      if (season === 26) return "97/98"
      if (season === 27) return "96/97"
      if (season === 28) return "95/96"
      if (season === 29) return "94/95"
      if (season === 30) return "93/94"

  }


  translateMinutes = (minutes,games) => {
    if (games === 0) return 0.00
    const minutesgame = minutes / games;
    return ((minutesgame/60).toFixed(2))
  }
  
  translateAge = (age) => {
    return age.substring(0,10)
  }
  
  render() {
    
    const { data, DataisLoaded } = this.state;
    const logo = require('./img.jpg');
    const court = require('./court.png');

    if (!DataisLoaded){
      this.getData()
    }

    else if (DataisLoaded){
      const array = data.data;

      return(
        <div className="App">
          <nav>
            <NavBar className="NavBar"> </NavBar>
          </nav>
          <header className="App-header">
          
            <main>
              <img className="foto caja1" src={logo} />
              <img className="court" src={court}/>
              <ListGroup className="datos">
                <ListGroup.Item variant="light"> {array[0].name} </ListGroup.Item>
                <ListGroup.Item variant="light"> {array[0].nationality} </ListGroup.Item>
                <ListGroup.Item variant="light"> {this.translateAge(array[0].age)} </ListGroup.Item>
                <ListGroup.Item variant="light"> {array[0].height} </ListGroup.Item>
                <ListGroup.Item variant="light"> {array[0].gender} </ListGroup.Item>
              </ListGroup>

            <section>
              <Table striped  bordered hover className= "stats caja3">
                <tbody>
                <tr>
                  <th>Team</th>
                  <th>Season</th>
                  <th>Phase</th>
                  <th>League</th>
                  <th>GP</th>
                  <th>MIN/P</th>
                  <th>PTS</th>
                  <th>2PA</th>
                  <th>3PA </th>
                  <th>FGA</th>
                  <th>FTA</th>
                  <th>2PM</th>
                  <th>3PM</th>
                  <th>FGM</th>
                  <th>FTM</th>
                  <th>OREB</th>
                  <th>DREB</th>
                  <th>TREB </th>
                  <th>AST</th>
                  <th>STL</th>
                  <th>TOV</th>
                  <th>BLK +</th>
                  <th>BLK -</th>
                  <th>DNK</th>
                  <th>PF +</th>
                  <th>PF -</th>
                  <th>VA</th>
                  

                </tr>
               {array.map((item) => ( 
                <tr>
                  <td> { item.teamname }</td> 
                  <td>  { this.translateSeason(item.seasonid) } </td> 
                  <td>  { item.phase }</td> 
                  <td>  { item.league }</td> 
                  <td>  { item.games }</td> 
                  <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                  <td>  { item.pt }</td> 
                  <td>   { item.t2t }</td> 
                  <td> { item.t3t }</td> 
                  <td>  { item.tct} </td> 
                  <td>  { item.tlt} </td> 
                  <td>  { item.t2s} </td> 
                  <td>  { item.t3s} </td> 
                  <td>  { item.tcs} </td> 
                  <td>  { item.tls} </td> 
                  <td>  { item.ro} </td> 
                  <td>  { item.rd} </td> 
                  <td>  { item.rt} </td> 
                  <td>  { item.asst} </td> 
                  <td>  { item.br} </td> 
                  <td>  { item.bp} </td> 
                  <td>  { item.tf} </td> 
                  <td>  { item.tc} </td> 
                  <td>  { item.mt} </td> 
                  <td>  { item.fc} </td> 
                  <td>  { item.fr} </td> 
                  <td>  { item.va} </td> 
                  
               </tr>
                ))} 
                
                </tbody>
                
              </Table>

            </section>
          
          
            
          </main>
            
          </header>
        </div>
      )



    }
    

    
  } 

}

export default App;