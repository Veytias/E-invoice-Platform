import React, { useEffect } from 'react';
import axios from 'axios';

import Credentials from '../Credentials';

function ListInvoice() {
    const [invoices, setInvoices] = React.useState([]);

    const tmp = React.useContext(Credentials);
    const token = tmp.replace(/['"]+/g, '');
    const params = new URLSearchParams([['token', token]]);
   
    useEffect(() => {
      fetchInvoices();
    }, [])
    useEffect(() => {
      console.log(invoices)
    }, [invoices])
    const fetchInvoices=async()=>{
        const response=await axios(`https://h18abrownie.herokuapp.com/invoices/list`, { params});
        setInvoices(response.data)    
    }
    return (
      <div className="App">
      <h1>Invoice List</h1>
      {
        invoices && invoices.map(invoice=>{
          return(
            <div key={invoice.invoice_id} style={{alignItems:'center',margin:'40px 30px'}}>
            
            <h4>Invoice Id: {invoice.invoice_id}</h4>
            <p>FileName: {invoice.filename}</p>
            </div>
            )
            })
        }
        </div>
    );
}
   
export default ListInvoice;
