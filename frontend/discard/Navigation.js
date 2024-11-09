import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <Navbar bg='primary' variant='dark' expand='lg' className='mb-3'>
      <Container>
        <Navbar.Brand as={Link} to='/'>
          Statsball
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default Navigation;
