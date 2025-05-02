import React, { useEffect, useState } from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

export default function ToolOutput({ collectionName, toolName }) {
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchOutput() {
      try {
        const response = await axios.get("http://localhost:5000/api/scan/results", {
          params: { collection: collectionName, tool: toolName }
        });
        if (response.data && response.data.results && response.data.results.length > 0) {
          setOutput(response.data.results[0].output || '');
        } else {
          setOutput('No output available');
        }
      } catch (error) {
        setOutput('Error fetching output');
        console.error('Error fetching tool output:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchOutput();
  }, [collectionName, toolName]);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box style={{ whiteSpace: 'pre-wrap', maxHeight: 140, overflowY: 'auto', padding: 8, border: '1px solid #ccc', borderRadius: 4 }}>
      <Typography variant="body2">{output}</Typography>
    </Box>
  );
}
