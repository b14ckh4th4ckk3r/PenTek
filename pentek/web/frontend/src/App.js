import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ScanDetailsPage from './pages/ScanDetailsPage';
import { AppBar, Toolbar, Button, Typography } from '@mui/material';
import './App.css';

function App() {
  return (
    <Router>
      <AppBar position="static" className="AppBar">
        <Toolbar>
          <Typography variant="h6">Pentesting Web App</Typography>
          <Button color="inherit" component={Link} to="/">Dashboard</Button>
        </Toolbar>
      </AppBar>

      <div className="main-content" style={{ height: 'calc(100vh - 64px)' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scan-details/:collectionName" element={<ScanDetailsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
