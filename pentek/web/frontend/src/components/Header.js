import React from 'react';
import { Box, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import './Header.css';

export default function Header() {
  return (
    <div className='header'>
    <Box className="header-container">
      <Link to="/" className="header-link">
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: 'left' }}>
          PenTek
        </Typography>
      </Link>
    </Box>
    </div>
  );
}
