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

function UploadInvoice() {
  const [selectedFile, setSelectedFile] = React.useState();  
  const [report, setReport] = React.useState();
  const [error, setError] = React.useState();

  const token = React.useContext(Credentials);
  
  function handleSubmit(event) {
    event.preventDefault();

    setSelectedFile(event.target[0].files[0]);
    const file = selectedFile;
    const report_type = event.target[2].value;
    if (!file || !report_type) return;

    const formData = new FormData();

    formData.append('token', token.replace(/['"]+/g, ''));
    formData.append('file', file);
    formData.append('report_type', report_type);
    
    axios({
      method: "post",
      url: `https://h18abrownie.herokuapp.com/invoice/upload/API`,
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    })
      .then((response) => {
        console.log(JSON.parse(JSON.stringify(response.data)));
        setReport(JSON.stringify(response.data));
        /*  Don't know how to pass query string for now like invoice:id kind of format. 
            Will implement if learnt later
            For now it is only json format.
        */ 
        
        // const report_id = response.data['report_id'];
        // const queryString = '?token=';
        // queryString.concat(token);
        // queryString.concat('&report_id');
        // queryString.concat(report_id);
        // props.history.push({
        //   pathname: '/reports/read',
        //   search: queryString,
        //   state: { report_type }
        // });
  
        // const data = response.data;
      })
      .catch((error) => { setError("File is not xml format or report type is not correct") });
    }

  return(
    <Container component="main" maxWidth="lg">
      <Box boxShadow={1}>
        <Typography component="h1" variant="h2">
          Upload Invoice
        </Typography>
        {
          <form onSubmit={handleSubmit}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="file"
              name="file"
              type="file"
              autoFocus 
            />
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
            <div className="report">{report ? <p>{report}</p> : <p>{error}</p>}</div>
          </form>

            
        }
      </Box>
    </Container>
  );
}

export default UploadInvoice;
// UploadInvoice.propTypes = {
//   setSelectedFile: PropTypes.func.isRequired
// }

