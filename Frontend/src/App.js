import React from 'react';
import './App.css';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { CredentialsAdmin } from './Credentials'
// dashboard is home dir
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import ProtectedRoute from './pages/protectedRoutes';
import UploadInvoice from './pages/invoiceUpload';
import ListInvoice from './pages/invoiceList';
import ListReport from './pages/ReportList';
import invoiceEmailReceive from './pages/invoiceEmailReceive';
import InvoiceSend from './pages/invoiceSend';
import InvoiceRemove from './pages/invoiceRemove';
// import API_receive must be protected route

function App() {
  // Title of the app
  document.title = 'Invoice Hub';
  // Creating states for token, noToken
  const [token, SetToken] = React.useState(localStorage.getItem('token'));
  
  function setCredentials(token) {
    localStorage.setItem('token', JSON.stringify(token));
    SetToken(JSON.stringify(token))
  }
  return (
    // Ensures any route ensures the need of token
    <CredentialsAdmin value={token}>
      <BrowserRouter>
        <Switch>
          <Route
            exact
            path="/"
            render={(props) => {
              return <Login {...props} setCredentials={setCredentials} />;
            }}
          />
          <Route
            path="/register"
            render={(props) => {
              return <Register {...props} setCredentials={setCredentials} />;
            }}
          />
          {/* <Route
            exact
            path="/invoice/upload"
            render={(props) => {
              return <UploadInvoice {...props} setCredentials={UploadInvoice} />;
            }}
          /> */}
          <ProtectedRoute path="/dashboard" component={Dashboard} />
          <ProtectedRoute path="/invoice/list" component={ListInvoice} />
          <ProtectedRoute path="/invoice/upload/api" component={UploadInvoice} />
          <ProtectedRoute path="/invoice/upload/email" component={invoiceEmailReceive} />
          <ProtectedRoute path="/report/list" component={ListReport} />
          <ProtectedRoute path="/invoice/send" component={InvoiceSend} />
          <ProtectedRoute path="/invoice/remove" component={InvoiceRemove} />

        </Switch>
      </BrowserRouter>
    </CredentialsAdmin>
  );
}

export default App;
/* <ProtectedRoute path="/invoice/remove" component={InvoiceRemove} /> */