import React, { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography, CircularProgress, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './AllScans.css';

export default function AllScans() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchScans = async () => {
      setLoading(true);
      try {
        const res = await axios.get('http://localhost:5000/api/scan/list');
        // group by collection_name
        const grouped = {};
        res.data.forEach(item => {
          if (!grouped[item.collection_name]) {
            grouped[item.collection_name] = { ...item, items: [] };
          }
          grouped[item.collection_name].items.push(item);
        });
        setScans(Object.values(grouped).sort((a,b)=>
          new Date(b.timestamp) - new Date(a.timestamp)
        ));
      } finally {
        setLoading(false);
      }
    };
    fetchScans();
  }, []);

  if (loading) return <CircularProgress />;
  if (!scans.length) return <Typography>No scans found.</Typography>;

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        All Scans
      </Typography>
      <Grid container spacing={2}>
        {scans.map(scan => (
          <Grid item xs={12} sm={6} md={4} key={scan.collection_name}>
            <Card
              onClick={() => navigate(`/scan-details/${scan.collection_name}`)}
              className="scan-card"
            >
              <CardContent>
                <Typography variant="h6">{scan.domain}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Last run: {new Date(scan.timestamp).toLocaleString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
