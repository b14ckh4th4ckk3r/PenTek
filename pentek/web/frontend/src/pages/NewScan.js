import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Typography,
  Dialog, DialogTitle, DialogContent, TextField, DialogActions,
  Button, Snackbar, Alert, CircularProgress
} from '@mui/material';
import { BugReport, Search, Visibility } from '@mui/icons-material';
import axios from 'axios';
import io from 'socket.io-client';
import './NewScan.css';

const socket = io("http://localhost:5000");

const scanTypes = [
  { key: 'full', label: 'Full Automated Test', icon: <BugReport fontSize="large" /> },
  { key: 'recon', label: 'Only Recon', icon: <Search fontSize="large" /> },
  { key: 'scanning', label: 'Only Scanning', icon: <Visibility fontSize="large" /> },
];

export default function NewScan() {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedScanType, setSelectedScanType] = useState(null);
  const [domain, setDomain] = useState('');
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('');
  const [scanStarted, setScanStarted] = useState(false);

  useEffect(() => {
    socket.on('scan_started', data => {
      setStatus(data.message);
      setScanStarted(true);
    });
    socket.on('scan_completed', data => {
      setStatus(data.message);
      setScanStarted(false);
    });
    return () => {
      socket.off('scan_started');
      socket.off('scan_completed');
    };
  }, []);

  const handleNewScanClick = scanType => {
    setSelectedScanType(scanType);
    setDomain('');
    setError(null);
    setOpenDialog(true);
  };

  const startScan = async () => {
    if (!domain) {
      setError('Please enter a domain');
      return;
    }
    try {
      await axios.post('http://localhost:5000/api/scan/start', {
        domain,
        scan_type: selectedScanType.key,
      });
      setStatus('Scan started');
      setScanStarted(true);
      setOpenDialog(false);
    } catch {
      setError('Failed to start scan');
    }
  };

  return (
    <div className='newscan'>
    <Box className="newscan-container">
      <Typography variant="h4" className="newscan-title" gutterBottom>
        Start a New Scan
      </Typography>
      <Grid container spacing={4} justifyContent="center">
        {scanTypes.map(type => (
          <Grid item xs={12} sm={6} md={4} key={type.key}>
            <Card className="scan-card" onClick={() => handleNewScanClick(type)}>
              <CardContent className="scan-card-content">
                <Box display="flex" flexDirection="column" alignItems="center">
                  {type.icon}
                  <Typography variant="h6" align="center" sx={{ mt: 1 }}>
                    {type.label}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {scanStarted && (
        <Box sx={{ mt: 3, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <CircularProgress size={20} sx={{ mr: 1, color: '#4a90e2' }} />
          <Typography color="primary">{status}</Typography>
        </Box>
      )}

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Start {selectedScanType?.label}</DialogTitle>
        <DialogContent>
          <TextField
            label="Domain or IP"
            fullWidth
            value={domain}
            onChange={e => setDomain(e.target.value)}
            error={Boolean(error)}
            helperText={error}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={startScan} disabled={scanStarted}>
            Start
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={Boolean(error)}
        autoHideDuration={6000}
        onClose={() => setError(null)}
      >
        <Alert severity="error">{error}</Alert>
      </Snackbar>
    </Box>
    </div>  
  );
}
