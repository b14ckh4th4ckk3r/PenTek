import React, { useState, useEffect } from 'react';
import { CircularProgress, Typography, LinearProgress, Button } from '@mui/material';
import io from 'socket.io-client';
import axios from 'axios';
import './ScanningPage.css';

const socket = io("http://localhost:5000");

export default function ScanningPage() {
  const [scanStatus, setScanStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);  // For displaying scan progress
  const [scanCompleted, setScanCompleted] = useState(false);

  // Real-time scan progress updates
  useEffect(() => {
    socket.on('scan_started', (data) => {
      setScanStatus('Scan started...');
    });

    socket.on('scan_progress', (data) => {
      setScanProgress(data.progress);
    });

    socket.on('scan_completed', (data) => {
      setScanStatus('Scan completed!');
      setScanProgress(100);
      setScanCompleted(true);
    });

    return () => {
      socket.off('scan_started');
      socket.off('scan_progress');
      socket.off('scan_completed');
    };
  }, []);

  const handleStartScan = async () => {
    setLoading(true);
    setScanStatus('Initializing scan...');
    try {
      const response = await axios.post('http://localhost:5000/api/scan/start', {
        domain: 'example.com', // You may want to make this dynamic or add input field
        scan_type: 'scanning',
        mode: 'web',
      });
      setScanStatus(response.data.status);
    } catch (error) {
      setScanStatus('Error starting scan');
      console.error('Error starting scan:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <Typography variant="h4">Scanning Page</Typography>
      {scanStatus && <Typography>{scanStatus}</Typography>}

      {loading ? (
        <CircularProgress />
      ) : (
        <Button onClick={handleStartScan} variant="contained">
          Start Scan
        </Button>
      )}

      {scanProgress < 100 && <LinearProgress variant="determinate" value={scanProgress} />}
      {scanCompleted && <Typography>Scan Completed!</Typography>}
    </div>
  );
}
