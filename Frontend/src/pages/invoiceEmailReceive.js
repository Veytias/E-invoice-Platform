import React, { useState } from 'react';
import './wrapper.css';
import axios from 'axios';
import './wrapper.css';

import Credentials from '../Credentials';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
} from '@material-ui/core';

function InvoiceEmailReceive() {
  const [report, setReport] = React.useState();
  const [error, setError] = React.useState();

  const tmp = React.useContext(Credentials);
  
  function handleSubmit(event) {
    event.preventDefault();

    const report_type = event.target[0].value;
    if (!report_type) return;

    const formData = new FormData();
    const token = tmp.replace(/['"]+/g, '');

    axios.post(`https://h18abrownie.herokuapp.com/invoice/upload/IMAP`, { token, report_type })
    .then((response) => {
      console.log(response.data);
      if (response.data === null) {
        setReport("No new invoices received!");
      } else {
        setReport(JSON.stringify(response.data));
      }
    })
    .catch((err) => { 
      setError("An error has occurred. Please try again!");
      console.log(err);
    });
  } 

  return(
    <Container component="main" maxWidth="lg">
      <Box boxShadow={1}>
        <Typography component="h1" variant="h2">
          Receive email
        </Typography>
        {
          <form onSubmit={handleSubmit}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="report_type"
              name="Report Type"
              label="Report Type"
              type="text"
              autoFocus 
            />
            <Button type="submit" fullWidth variant="contained" color="primary">
            Submit
            </Button>
            <div className="report">{report ? <p>{report}</p> : <p>{error} </p>}</div>
          </form>

            
        }
      </Box>
    </Container>
  );
}

export default InvoiceEmailReceive;
// UploadInvoice.propTypes = {
//   setSelectedFile: PropTypes.func.isRequired
// }

