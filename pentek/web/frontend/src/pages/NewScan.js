import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import './NewScan.css';

const scanTypes = [
  { key: 'full', label: 'Full Automated Test' },
  { key: 'recon', label: 'Only Recon' },
  { key: 'scanning', label: 'Only Scanning' },
];

export default function NewScan({ onNewScanClick }) {
  return (
    <Grid container spacing={3}>
      {scanTypes.map((scanType) => (
        <Grid key={scanType.key} sx={{ flexGrow: 1, minWidth: 0, maxWidth: '33.33%' }}>
          <Card
            className="scan-card"
            onClick={() => onNewScanClick(scanType)}
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
  );
}
