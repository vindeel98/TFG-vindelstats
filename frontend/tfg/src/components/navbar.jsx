import React from "react";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Container from 'react-bootstrap/Container';
import NavLink from "react-bootstrap/esm/NavLink";

const NavBar = () => {

    return (

    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand href="/">Vindel Stats</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
          <NavDropdown title="LEB ORO" id="basic-nav-dropdown">
          <NavDropdown.Item href="/ranks/oro">Ranking</NavDropdown.Item>
              <NavDropdown.Item href="/stats/oro">Stats</NavDropdown.Item>
 
            </NavDropdown>
            <NavDropdown title="LEB PLATA" id="basic-nav-dropdown">
            <NavDropdown.Item href="/ranks/plata">Ranking</NavDropdown.Item>
              <NavDropdown.Item href="/stats/plata">Stats</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="EBA" id="basic-nav-dropdown">
              <NavDropdown.Item href="/ranks/eba">Ranking</NavDropdown.Item>
              <NavDropdown.Item href="/stats/eba">Stats</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="LF1" id="basic-nav-dropdown">
            <NavDropdown.Item href="/ranks/lf1">Ranking</NavDropdown.Item>
              <NavDropdown.Item href="/stats/lf1">Stats</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="LF CHALLENGE" id="basic-nav-dropdown">
            <NavDropdown.Item href="/ranks/lfchall">Ranking</NavDropdown.Item>
              <NavDropdown.Item href="/stats/lfchall">Stats</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="LF2" id="basic-nav-dropdown">
            <NavDropdown.Item href="/ranks/lf2">Ranking</NavDropdown.Item>
              <NavDropdown.Item href="/stats/lf2">Stats</NavDropdown.Item>
            </NavDropdown>
            
          </Nav>
        </Navbar.Collapse>
      </Container>
      <Container >
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav"/>
            <Nav.Link href="#home">Stats </Nav.Link>
            <Nav.Link href="stats">About Us</Nav.Link>

      </Container>
    </Navbar>
    );
  }



export default NavBar;