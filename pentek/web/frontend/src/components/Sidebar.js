import React from 'react';
import { Box, Button, Stack } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

export default function Sidebar() {
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <Box className="sidebar-container">
      <Stack spacing={2} direction="column">
        <Button
          component={Link}
          to="/"
          variant={currentPath === '/' ? 'contained' : 'outlined'}
          className="sidebar-button"
        >
          Dashboard
        </Button>
        <Button
          component={Link}
          to="/new-scan"
          variant={currentPath === '/new-scan' ? 'contained' : 'outlined'}
          className="sidebar-button"
        >
          New Scan
        </Button>
        <Button
          component={Link}
          to="/scans"
          variant={currentPath === '/scans' ? 'contained' : 'outlined'}
          className="sidebar-button"
        >
          All Scans
        </Button>
      </Stack>
    </Box>
  );
}
