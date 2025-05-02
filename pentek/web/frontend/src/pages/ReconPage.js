import React, { useState, useEffect } from 'react';
import { Button, Typography, CircularProgress, TextField, Snackbar, Alert } from '@mui/material';
import axios from 'axios';
import io from 'socket.io-client';
import './ReconPage.css'

const socket = io("http://localhost:5000");

export default function ReconPage() {
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [domain, setDomain] = useState('');
  const [loadingResults, setLoadingResults] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Real-time updates
    socket.on('scan_started', (data) => {
      setStatus(data.message);
    });

    return () => {
      socket.off('scan_started');
    };
  }, []);

  const startScan = async () => {
    if (!domain) {
      setError('Please provide a domain.');
      return;
    }

    setLoading(true);
    const scanType = 'recon';
    const mode = 'web';

    try {
      const response = await axios.post('http://localhost:5000/api/scan/start', {
        domain,
        scan_type: scanType,
        mode: mode,
      });
      setStatus(response.data.status);
    } catch (error) {
      setError('Error starting scan');
      console.error('Error starting scan:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchResults = async () => {
    setLoadingResults(true);
    try {
      const response = await axios.get('http://localhost:5000/api/scan/results');
      setResults(response.data.results);
    } catch (error) {
      setError('Error fetching results');
      console.error('Error fetching results:', error);
    } finally {
      setLoadingResults(false);
    }
  };

  const handleCloseSnackbar = () => {
    setError(null);
  };

  return (
    <div style={{ padding: '20px' }}>
      <Typography variant="h4" gutterBottom>
        Recon Phase
      </Typography>
      <TextField
        label="Domain"
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
        fullWidth
        margin="normal"
      />
      
      {status && <Typography variant="body1">{status}</Typography>}
      
      {loading ? (
        <CircularProgress />
      ) : (
        <Button onClick={startScan} variant="contained" color="primary">Start Recon Scan</Button>
      )}

      <Button
        onClick={fetchResults}
        variant="contained"
        color="secondary"
        style={{ marginLeft: '10px' }}
        disabled={loadingResults}
      >
        Get Results
      </Button>
      
      {loadingResults && <CircularProgress style={{ marginLeft: '10px' }} />}

      {results && (
        <div style={{ marginTop: '20px' }}>
          <Typography variant="h6">Scan Results:</Typography>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}

      {error && (
        <Snackbar open={Boolean(error)} autoHideDuration={6000} onClose={handleCloseSnackbar}>
          <Alert onClose={handleCloseSnackbar} severity="error">
            {error}
          </Alert>
        </Snackbar>
      )}
    </div>
  );
}
