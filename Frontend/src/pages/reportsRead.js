import React from 'react';
import './wrapper.css';
import axios from 'axios';
import './wrapper.css';
import PropTypes from 'prop-types';

import Credentials from '../Credentials';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
} from '@material-ui/core';

function reportsRead( {...props} ) {
    const [query_str, setQueryStr] = React.useState("");

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
        console.log(response.data);
        const report_id = response.data['report_id'];
        const queryString = '?token=';
        queryString.concat(token);
        queryString.concat('&report_id');
        queryString.concat(report_id);
        props.history.push({
          pathname: '/reports/read',
          search: queryString,
          state: { report_type }
        });
  
        // const data = response.data;
      })
      .catch((error) => { console.error('Error, error') });
    }

  return(
    <Container component="main" maxWidth="sm">
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
            </form>
        }
      </Box>
    </Container>
  );
}

export default reportsRead;
// UploadInvoice.propTypes = {
//   setSelectedFile: PropTypes.func.isRequired
// }
