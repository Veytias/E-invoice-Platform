import React, { useEffect } from 'react';
import axios from 'axios';

import Credentials from '../Credentials';

function ListReport() {
    const [reports, setReports] = React.useState([]);

    const tmp = React.useContext(Credentials);
    const token = tmp.replace(/['"]+/g, '');
    const params = new URLSearchParams([['token', token]]);
   
    useEffect(() => {
      fetchreports();
    }, [])
    useEffect(() => {
      console.log(reports)
    }, [reports])
    const fetchreports=async()=>{
        const response=await axios(`https://h18abrownie.herokuapp.com/reports/list`, { params});
        setReports(response.data)    
    }
    return (
        <div className="App">
        <h1>report List</h1>
        {
          reports && reports.map(report=>{
            return(
                <div key={report.report_id} style={{alignItems:'center',margin:'40px 30px'}}>
                
                <h4>report Id: {report.report_id}</h4>
                <p>FileName: {report.report_name}</p>
                </div>
                )
            })
        }
        </div>
    );
}
   
export default ListReport;
