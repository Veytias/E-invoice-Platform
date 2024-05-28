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

function InvoiceSend() {
  const [report, setReport] = React.useState();

  const tmp = React.useContext(Credentials);
  const [error, setError] = React.useState();
  
  function handleSubmit(event) {
    event.preventDefault();

    const invoice_id = event.target[0].value;
    const recipientEmail = event.target[2].value;
    if (!invoice_id || !recipientEmail) return;

    const token = tmp.replace(/['"]+/g, '');

    axios.post(`https://h18abrownie.herokuapp.com/invoice/send`, { token, invoice_id, recipientEmail })
    .then((response) => {
      console.log(response.data);
      if (response.data === null) {
        setReport("Invoice has not been sent!");
      } else {
        setReport(JSON.stringify(response.data));
      }
    })
    .catch((err) => { setError("An error has occured. Please try again."); });
    } 

  return(
    <Container component="main" maxWidth="lg">
      <Box boxShadow={1}>
        <Typography component="h1" variant="h2">
          Send invoice to customer
        </Typography>
        {
          <form onSubmit={handleSubmit}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="invoice_id"
              name="invoice_id"
              label="Invoice id"
              type="text"
              autoFocus 
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="recipientEmail"
              name="Recipient Email"
              label="Recipient Email"
              type="email"
              autoFocus 
            />
            <Button type="submit" fullWidth variant="contained" color="primary">
            Submit
            </Button>
            <div className="report">{report ? <p>{report}</p> : <p>{error}</p>}</div>
          </form>

            
        }
      </Box>
    </Container>
  );
}

export default InvoiceSend;
// UploadInvoice.propTypes = {
//   setSelectedFile: PropTypes.func.isRequired
// }

