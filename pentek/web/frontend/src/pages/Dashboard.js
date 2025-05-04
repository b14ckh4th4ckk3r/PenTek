import './Dashboard.css';
import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Snackbar,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Divider,
} from '@mui/material';
import axios from 'axios';
import io from 'socket.io-client';
import { useNavigate } from 'react-router-dom';

const socket = io("http://localhost:5000");

const scanTypes = [
  { key: 'full', label: 'Full Automated Test' },
  { key: 'recon', label: 'Only Recon' },
  { key: 'scanning', label: 'Only Scanning' },
];

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`dashboard-tabpanel-${index}`}
      aria-labelledby={`dashboard-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function Dashboard() {
  const [tabIndex, setTabIndex] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedScanType, setSelectedScanType] = useState(null);
  const [domain, setDomain] = useState('');
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('');
  const [scanStarted, setScanStarted] = useState(false);
  const [scansList, setScansList] = useState([]);
  const [loadingScans, setLoadingScans] = useState(false);
  const [selectedScan, setSelectedScan] = useState(null);
  const [scanResults, setScanResults] = useState([]);
  const [loadingResults, setLoadingResults] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    socket.on('scan_started', (data) => {
      setStatus(data.message);
      setScanStarted(true);
      fetchScansList();
    });

    socket.on('scan_completed', (data) => {
      setStatus(data.message);
      setScanStarted(false);
      fetchScansList();
      if (selectedScan) {
        fetchScanResults(selectedScan.collection_name);
      }
    });

    fetchScansList();

    return () => {
      socket.off('scan_started');
      socket.off('scan_completed');
    };
  }, [selectedScan]);

  const fetchScansList = async () => {
    setLoadingScans(true);
    try {
      const response = await axios.get('http://localhost:5000/api/scan/list');
      const grouped = {};
      response.data.forEach((item) => {
        if (!grouped[item.collection_name]) {
          grouped[item.collection_name] = {
            collection_name: item.collection_name,
            domain: item.domain,
            latest_timestamp: item.timestamp,
            items: [],
          };
        }
        grouped[item.collection_name].items.push(item);
        if (new Date(item.timestamp) > new Date(grouped[item.collection_name].latest_timestamp)) {
          grouped[item.collection_name].latest_timestamp = item.timestamp;
        }
      });
      const groupedArray = Object.values(grouped).sort(
        (a, b) => new Date(b.latest_timestamp) - new Date(a.latest_timestamp)
      );
      setScansList(groupedArray);
    } catch (err) {
      setError('Failed to fetch scans list');
    } finally {
      setLoadingScans(false);
    }
  };

  const fetchScanResults = async (collectionName) => {
    setLoadingResults(true);
    try {
      const scan = scansList.find((s) => s.collection_name === collectionName);
      if (scan) {
        setScanResults(scan.items);
        setSelectedScan(scan);
      }
    } catch (err) {
      setError('Failed to fetch scan results');
    } finally {
      setLoadingResults(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabIndex(newValue);
    setSelectedScan(null);
    setScanResults([]);
    setStatus('');
    if (newValue === 1) {
      fetchScansList();
    }
  };

  const handleScanDetailsClick = (scan) => {
    if (scan && scan.collection_name) {
      navigate(`/scan-details/${scan.collection_name}`);
    }
  };

  const handleNewScanClick = (scanType) => {
    setSelectedScanType(scanType);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const startScan = async () => {
    if (!domain) {
      setError('Please enter a domain');
      return;
    }
    setError(null);
    setStatus('Starting scan...');
    try {
      await axios.post('http://localhost:5000/api/scan/start', {
        domain,
        scan_type: selectedScanType.key,
      });
      setStatus('Scan started');
      setScanStarted(true);
      setOpenDialog(false);
      fetchScansList();
    } catch (err) {
      setError('Failed to start scan');
      setStatus('');
      setScanStarted(false);
    }
  };

  return (
    <Box className="main-content" sx={{ display: 'flex', height: '100vh' }}>
      <Tabs
        orientation="vertical"
        variant="scrollable"
        value={tabIndex}
        onChange={handleTabChange}
        aria-label="Dashboard Tabs"
        sx={{ borderRight: 1, borderColor: 'divider', minWidth: 280 }}
      >
        <Tab label="New Scan" />
        <Tab label="All Scans" />
      </Tabs>

      <Box sx={{ flexGrow: 1, overflowY: 'auto' }}>
        <TabPanel value={tabIndex} index={0}>
          <Typography variant="h5" gutterBottom>
            Start a New Scan
          </Typography>
          <Grid container spacing={3}>
            {scanTypes.map((scanType) => (
              <Grid key={scanType.key} sx={{ flexGrow: 1, minWidth: 0, maxWidth: '33.33%' }}>
                <Card
                  className="scan-card"
                  onClick={() => handleNewScanClick(scanType)}
                  elevation={4}
                >
                  <CardContent>
                    <Typography variant="h6" align="center">
                      {scanType.label}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        <TabPanel value={tabIndex} index={1}>
          <Typography variant="h5" gutterBottom>
            All Scans
          </Typography>
          {loadingScans ? (
            <CircularProgress />
          ) : scansList.length === 0 ? (
            <Typography>No scans found.</Typography>
          ) : (
            <Grid container spacing={2}>
              {scansList.map((scan) => (
                <Grid key={scan.collection_name} sx={{ flexGrow: 1, minWidth: 0, maxWidth: '33.33%' }}>
                  <Card
                    className="scan-card"
                    onClick={() => handleScanDetailsClick(scan)}
                    variant={selectedScan?.collection_name === scan.collection_name ? 'outlined' : 'elevation'}
                    sx={{ padding: 2 }}
                  >
                    <Typography variant="subtitle1" gutterBottom>
                      {scan.domain}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Last updated: {new Date(scan.latest_timestamp).toLocaleString()}
                    </Typography>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}

          <Divider sx={{ my: 3 }} />

          {selectedScan && (
            <>
              <Typography variant="h6" gutterBottom>
                Scan Results for {selectedScan.domain}
              </Typography>
              {loadingResults ? (
                <CircularProgress />
              ) : scanResults.length === 0 ? (
                <Typography>No results found.</Typography>
              ) : (
                <Box className="scan-results-container">
                  <Grid container spacing={2}>
                    {scanResults.map((item, index) => (
                      <Grid key={index} sx={{ flexGrow: 1, minWidth: 0, maxWidth: '33.33%' }}>
                        <Card className="scan-result-card">
                          <Typography className="scan-result-title" variant="subtitle1" gutterBottom>
                            {item.scan_type} - {item.module} - {item.name}
                          </Typography>
                          <Typography className="scan-result-output" variant="body2">
                            {item.output || 'No output'}
                          </Typography>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              )}
            </>
          )}
        </TabPanel>
      </Box>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Start {selectedScanType?.label}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Domain"
            type="text"
            fullWidth
            variant="standard"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            error={Boolean(error)}
            helperText={error}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={startScan} variant="contained">
            Start
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={Boolean(error)}
        autoHideDuration={6000}
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
}
