import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Dashboard from './pages/Dashboard';
import NewScan from './pages/NewScan';
import AllScans from './pages/AllScans';
import ScanDetailsPage from './pages/ScanDetailsPage';

import Header from './components/Header';
import Sidebar from './components/Sidebar';

function App() {
  return (
    <Router>
      <Header />
      <div style={{ display: 'flex', height: 'calc(100vh - 48px)' }}>
        <Sidebar />
        <div style={{ flexGrow: 1, overflowY: 'auto' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/new-scan" element={<NewScan />} />
            <Route path="/scans" element={<AllScans />} />
            <Route path="/scan-details/:collectionName" element={<ScanDetailsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
