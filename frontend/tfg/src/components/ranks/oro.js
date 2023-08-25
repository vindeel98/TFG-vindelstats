import axios from "axios";
import NavBar from '../../components/navbar';
import { Component } from 'react';
import Table from 'react-bootstrap/Table';
import { bool } from "prop-types";



class RanksOro extends Component{

  state = {
    dataPT: [],
    dataT2: [],
    dataT3: [],
    dataRT: [],
    dataASST: [],
    dataBR: [],
    dataTF: [],
    dataMT: [],
    dataPTisLoaded: false,
    dataT2isLoaded: false,
    dataT3isLoaded: false,
    dataRTisLoaded: false,
    dataASSTisLoaded: false,
    dataBRisLoaded: false,
    dataTFisLoaded: false,
    dataMTisLoaded: false,
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
  


  getData = () => {
    axios.get("http://localhost:3001/oro/rank/pt")
      .then(dataPT => {
        this.setState({dataPT,dataPTisLoaded:true});
      })
     axios.get('http://localhost:3001/oro/rank/t2s')
      .then(dataT2=>{
        this.setState({dataT2,dataT2isLoaded:true});
      } )
      axios.get('http://localhost:3001/oro/rank/t3s')
      .then(dataT3=>{
        this.setState({dataT3,dataT3isLoaded:true});
      } )
      axios.get('http://localhost:3001/oro/rank/rt')
      .then(dataRT=>{
        this.setState({dataRT,dataRTisLoaded:true});
      } )
      axios.get('http://localhost:3001/oro/rank/asst')
      .then(dataASST=>{
        this.setState({dataASST,dataASSTisLoaded:true});
      } )
      axios.get('http://localhost:3001/oro/rank/br')
      .then(dataBR=>{
        this.setState({dataBR,dataBRisLoaded:true});
      } )
      axios.get('http://localhost:3001/oro/rank/tf')
      .then(dataTF=>{
        this.setState({dataTF,dataTFisLoaded:true});
      } )
      axios.get('http://localhost:3001/oro/rank/mt')
      .then(dataMT=>{
        this.setState({dataMT,dataMTisLoaded:true});
      } )
      


  }



  render() {

    const { dataPT, dataT2,dataT3,dataRT,dataASST,dataBR,dataTF,dataMT,dataPTisLoaded, dataT2isLoaded,dataT3isLoaded, dataRTisLoaded,   dataASSTisLoaded,
        dataBRisLoaded,
        dataTFisLoaded,
        dataMTisLoaded,
      }  = this.state;
    
     const DataisLoaded  = dataPTisLoaded&& dataT2isLoaded&& dataT3isLoaded &&dataRTisLoaded && dataASSTisLoaded&&dataBRisLoaded &&dataTFisLoaded &&dataMTisLoaded;
    if (!DataisLoaded){
        this.getData()
      }
    
    else if (DataisLoaded){
        const arrayPT = dataPT.data;
        const arrayT2 = dataT2.data;
        const arrayT3 = dataT3.data;
        const arrayRT = dataRT.data;
        const arrayASST = dataASST.data;
        const arrayBR = dataBR.data;
        const arrayTF = dataTF.data;
        const arrayMT = dataMT.data;

        return(
            <div className="RanksOro">
              <nav>
                <NavBar className="NavBar"> </NavBar>
              </nav>
              <header className="App-header">
              
              <main>
                <Table striped  bordered hover className= "stats caja3">
                        <tbody>
                        <tr>
                            <th>TOP SCORERS</th>
                        </tr>
                        <tr>
                            <th>Player Name</th>
                            <th>Team</th>
                            <th>Season</th>
                            <th>Phase</th>
                            <th>League</th>
                            <th>GP</th>
                            <th>MIN/P</th>
                            <th>PTS</th>
                            
        
                        </tr>
                        {arrayPT.map((item) => ( 
                        <tr>
                            <td> { item.name }</td> 
                            <td> { item.teamname }</td> 
                            <td>  { this.translateSeason(item.seasonid) } </td> 
                            <td>  { item.phase }</td> 
                            <td>  { item.league }</td> 
                            <td>  { item.games }</td> 
                            <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                            <td>  { item.pt }</td> 
                        
                        </tr>
                        ))} 
                        
                        </tbody>
                        
                </Table>
                <Table striped  bordered hover className= "stats caja3">
                    <tbody>
                    <tr>
                            <th>TOP T2 SCORERS</th>
                        </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Team</th>
                        <th>Season</th>
                        <th>Phase</th>
                        <th>League</th>
                        <th>GP</th>
                        <th>MIN/P</th>
                        <th>PT2S</th>
                        
    
                    </tr>
                    {arrayT2.map((item) => ( 
                    <tr>
                        <td> { item.name }</td> 
                        <td> { item.teamname }</td> 
                        <td>  { this.translateSeason(item.seasonid) } </td> 
                        <td>  { item.phase }</td> 
                        <td>  { item.league }</td> 
                        <td>  { item.games }</td> 
                        <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                        <td>  { item.t2s }</td> 

                    
                    </tr>
                    ))} 
                    
                    </tbody>
                    
                </Table>
                <Table striped  bordered hover className= "stats caja3">
                    <tbody>
                    <tr>
                            <th>TOP T3 SCORERS</th>
                        </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Team</th>
                        <th>Season</th>
                        <th>Phase</th>
                        <th>League</th>
                        <th>GP</th>
                        <th>MIN/P</th>
                        <th>PT3S</th>

                        
    
                    </tr>
                    {arrayT3.map((item) => ( 
                    <tr>
                        <td> { item.name }</td> 
                        <td> { item.teamname }</td> 
                        <td>  { this.translateSeason(item.seasonid) } </td> 
                        <td>  { item.phase }</td> 
                        <td>  { item.league }</td> 
                        <td>  { item.games }</td> 
                        <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                        <td>  { item.t3s }</td> 

                    
                    </tr>
                    ))} 
                    
                    </tbody>
                    
                </Table>
                <Table striped  bordered hover className= "stats caja3">
                    <tbody>
                    <tr>
                            <th>TOP REBOUNDERS</th>
                        </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Team</th>
                        <th>Season</th>
                        <th>Phase</th>
                        <th>League</th>
                        <th>GP</th>
                        <th>MIN/P</th>
                        <th>RT</th>
                        
    
                    </tr>
                    {arrayRT.map((item) => ( 
                    <tr>
                        <td> { item.name }</td> 
                        <td> { item.teamname }</td> 
                        <td>  { this.translateSeason(item.seasonid) } </td> 
                        <td>  { item.phase }</td> 
                        <td>  { item.league }</td> 
                        <td>  { item.games }</td> 
                        <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                        <td>  { item.rt }</td> 
                    
                    </tr>
                    ))} 
                    
                    </tbody>
                    
                </Table>
                <Table striped  bordered hover className= "stats caja3">
                    <tbody>
                    <tr>
                            <th>TOP ASSISTANTS</th>
                        </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Team</th>
                        <th>Season</th>
                        <th>Phase</th>
                        <th>League</th>
                        <th>GP</th>
                        <th>MIN/P</th>
                        <th>ASST</th>
                        
    
                    </tr>
                    {arrayASST.map((item) => ( 
                    <tr>
                        <td> { item.name }</td> 
                        <td> { item.teamname }</td> 
                        <td>  { this.translateSeason(item.seasonid) } </td> 
                        <td>  { item.phase }</td> 
                        <td>  { item.league }</td> 
                        <td>  { item.games }</td> 
                        <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                        <td>  { item.asst }</td> 
                    
                    </tr>
                    ))} 
                    
                    </tbody>
                    
                </Table>
                <Table striped  bordered hover className= "stats caja3">
                    <tbody>
                    <tr>
                            <th>TOP STEALERS</th>
                        </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Team</th>
                        <th>Season</th>
                        <th>Phase</th>
                        <th>League</th>
                        <th>GP</th>
                        <th>MIN/P</th>
                        <th>STL</th>
                        
    
                    </tr>
                    {arrayBR.map((item) => ( 
                    <tr>
                        <td> { item.name }</td> 
                        <td> { item.teamname }</td> 
                        <td>  { this.translateSeason(item.seasonid) } </td> 
                        <td>  { item.phase }</td> 
                        <td>  { item.league }</td> 
                        <td>  { item.games }</td> 
                        <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                        <td>  { item.br }</td> 
                    
                    </tr>
                    ))} 
                    
                    </tbody>
                    
                </Table>
                <Table striped  bordered hover className= "stats caja3">
                    <tbody>
                    <tr>
                            <th>TOP BLOCKERS</th>
                        </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Team</th>
                        <th>Season</th>
                        <th>Phase</th>
                        <th>League</th>
                        <th>GP</th>
                        <th>MIN/P</th>
                        <th>BLCK</th>
                        
    
                    </tr>
                    {arrayTF.map((item) => ( 
                    <tr>
                        <td> { item.name }</td> 
                        <td> { item.teamname }</td> 
                        <td>  { this.translateSeason(item.seasonid) } </td> 
                        <td>  { item.phase }</td> 
                        <td>  { item.league }</td> 
                        <td>  { item.games }</td> 
                        <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                        <td>  { item.tf }</td> 
                    
                    </tr>
                    ))} 
                    
                    </tbody>
                    
                </Table>
                <Table striped  bordered hover className= "stats caja3">
                    <tbody>
                    <tr>
                            <th>TOP DUNKERS</th>
                        </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Team</th>
                        <th>Season</th>
                        <th>Phase</th>
                        <th>League</th>
                        <th>GP</th>
                        <th>MIN/P</th>
                        <th>DKN</th>
                        
    
                    </tr>
                    {arrayMT.map((item) => ( 
                    <tr>
                        <td> { item.name }</td> 
                        <td> { item.teamname }</td> 
                        <td>  { this.translateSeason(item.seasonid) } </td> 
                        <td>  { item.phase }</td> 
                        <td>  { item.league }</td> 
                        <td>  { item.games }</td> 
                        <td>  { this.translateMinutes(item.mnt,item.games) }</td> 
                        <td>  { item.mt }</td> 
                    
                    </tr>
                    ))} 
                    
                    </tbody>
                    
                </Table>
              </main>
                
              </header>
            </div>
          )
    }
    
  } 

}

export default RanksOro;