
import React from 'react'
import { Link } from 'react-router-dom'

function Dashboard( {...props} ) {
    return (
        <div className="text-center">
            <h1 className="main-title home-page-title">welcome to our app</h1>
            <Link to="/invoice/upload/api">
                <button className="primary-button">Invoice upload</button>
            </Link>
            <Link to="/invoice/list">
                <button className="primary-button">Invoice list</button>
            </Link>
            <Link to="/invoice/upload/email">
                <button className="primary-button">Invoice receive through email</button>
            </Link>
            <Link to="/report/list">
                <button className="primary-button">Reports list</button>
            </Link>
            <Link to="/invoice/send">
                <button className="primary-button">Send Invoice</button>
            </Link>
            <Link to="/invoice/remove">
                <button className="primary-button">Remove invoice</button>
            </Link>

            
        </div>
    )
}
            /* <Link to="/invoice/remove">
                <button className="primary-button">Remove invoice</button>
            </Link> */
export default Dashboard;
