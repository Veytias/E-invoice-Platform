import React from 'react';
import './wrapper.css';
import PropTypes from 'prop-types';
import axios from 'axios';
import {
  Box,
  Button,
  Container,
  Grid,
  Link,
  TextField,
  Typography,
} from '@material-ui/core';


function Login({ setCredentials, ...props }) {
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState();
  // const [error, setError]

  function handleSubmit(event) {
    event.preventDefault();
    const email = event.target[0].value;
    const password = event.target[2].value;
    if (!email || !password ) return;

    // setLoading(true);
  
    axios.post(`https://h18abrownie.herokuapp.com/auth/login`, { email, password })
      .then((response) => {
        console.log(response);
        setCredentials(response.data);
        props.history.push('/dashboard');
      })
      .catch((err) => { setError("Login failed. Please try again!"); })
      .finally(() => setLoading(false));
  }

  return(
    <Container component="main" maxWidth="sm">
      <Box boxShadow={1}>
        <Typography component="h1" variant="h2">
          Login
        </Typography>
        {
          loading
            ? <div className="wrapper">{<p>{error}</p>}</div>
            : <form noValidate onSubmit={handleSubmit}>
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email"
                name="email"
                type="text"
                autoFocus
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
              />
             
              <Button type="submit" fullWidth variant="contained" color="primary">
                Sign In
                </Button>
                <div className="loading">{error ? <p>{error}</p> : null}</div>
              <Grid container direction="column" alignItems="center">
                <Grid item>
                  <br />
                  <Link href="/register" variant="body1">
                    {"Don't have an account? Register"}
                  </Link>
                </Grid>
              </Grid>
            </form>
        }
      </Box>
    </Container>
  );
}
export default Login;

Login.propTypes = {
  setCredentials: PropTypes.func.isRequired
}
 
