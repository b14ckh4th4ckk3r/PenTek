import React from 'react';
import { Box, Typography, Grid, Card, CardContent } from '@mui/material';
import { AccountTree, Search, BugReport, Extension, Language, Assessment } from '@mui/icons-material';
import './Dashboard.css'; // Regular CSS import

export default function Dashboard() {
  return (
    <div className="dashboard-container-page">
      <Box className="dashboardContainer">
        <Typography variant="h3" className="dashboardTitle" gutterBottom>
          Pentek Dashboard
        </Typography>
        <Typography variant="body1" className="dashboardText" paragraph>
          Welcome to Pentek – your automated penetration testing tool, equipped with multiple modules for recon, scanning, exploitation, and post-exploitation.
        </Typography>

        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12} sm={6} md={3}>
            <Card className="dashboardCard">
              <CardContent>
                <AccountTree fontSize="large" color="primary" />
                <Typography variant="h6" className="cardTitle">
                  Recon
                </Typography>
                <Typography variant="body2">
                  Discover and enumerate target systems with advanced recon capabilities.
                  <br />
                  Includes DNS, subdomain, and network mapping tools.
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card className="dashboardCard">
              <CardContent>
                <Search fontSize="large" color="primary" />
                <Typography variant="h6" className="cardTitle">
                  Scanning
                </Typography>
                <Typography variant="body2">
                  Run comprehensive port scans and vulnerability assessments.
                  <br />
                  Supports Nmap, NSE, and service fingerprinting.
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card className="dashboardCard">
              <CardContent>
                <BugReport fontSize="large" color="primary" />
                <Typography variant="h6" className="cardTitle">
                  Exploitation
                </Typography>
                <Typography variant="body2">
                  Identify and exploit vulnerabilities using automated scripts.
                  <br />
                  Integrates with Metasploit and Exploit-DB.
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* <Grid item xs={12} sm={6} md={3}>
            <Card className="dashboardCard">
              <CardContent>
                <Extension fontSize="large" color="primary" />
                <Typography variant="h6" className="cardTitle">
                  Post-Exploitation
                </Typography>
                <Typography variant="body2">
                  Gather further data and execute post-access tasks.
                  <br />
                  Includes persistence, pivoting, and data exfiltration.
                </Typography>
              </CardContent>
            </Card>
          </Grid> */}

          <Grid item xs={12} sm={6} md={3}>
            <Card className="dashboardCard">
              <CardContent>
                <Language fontSize="large" color="primary" />
                <Typography variant="h6" className="cardTitle">
                  Web Scanning
                </Typography>
                <Typography variant="body2">
                  Detect web technologies, vulnerabilities, and misconfigurations.
                  <br />
                  Supports XSS, SQLi, Dirb, and WAF detection.
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card className="dashboardCard">
              <CardContent>
                <Assessment fontSize="large" color="primary" />
                <Typography variant="h6" className="cardTitle">
                  Automation
                </Typography>
                <Typography variant="body2">
                  Automate scan workflows.
                  <br />
      
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </div>
  );
}
