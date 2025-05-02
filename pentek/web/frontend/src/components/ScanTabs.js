import React, { useState, useEffect } from 'react';
import { Tabs, Tab, Box, Typography } from '@mui/material';
import axios from 'axios';
import ToolOutput from './ToolOutput';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`scan-tabpanel-${index}`}
      aria-labelledby={`scan-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function ScanTabs() {
  const [scanTypes, setScanTypes] = useState([]);
  const [modulesByScanType, setModulesByScanType] = useState({});
  const [toolsByModule, setToolsByModule] = useState({});
  const [selectedScanType, setSelectedScanType] = useState(0);
  const [selectedModule, setSelectedModule] = useState(0);

  useEffect(() => {
    async function fetchScanMetadata() {
      try {
        const response = await axios.get('http://localhost:5000/api/scan/list');
        const scans = response.data;

        const scanTypeSet = new Set();
        const modulesMap = {};
        const toolsMap = {};

        scans.forEach(scan => {
          scanTypeSet.add(scan.scan_type);
          if (!modulesMap[scan.scan_type]) {
            modulesMap[scan.scan_type] = new Set();
          }
          modulesMap[scan.scan_type].add(scan.module);

          if (!toolsMap[scan.module]) {
            toolsMap[scan.module] = new Set();
          }
          toolsMap[scan.module].add(scan.name);
        });

        const scanTypeArr = Array.from(scanTypeSet);
        const modulesByType = {};
        Object.keys(modulesMap).forEach(type => {
          modulesByType[type] = Array.from(modulesMap[type]);
        });
        const toolsByMod = {};
        Object.keys(toolsMap).forEach(mod => {
          toolsByMod[mod] = Array.from(toolsMap[mod]);
        });

        setScanTypes(scanTypeArr);
        setModulesByScanType(modulesByType);
        setToolsByModule(toolsByMod);
      } catch (error) {
        console.error('Error fetching scan metadata:', error);
      }
    }
    fetchScanMetadata();
  }, []);

  const handleScanTypeChange = (event, newValue) => {
    setSelectedScanType(newValue);
    setSelectedModule(0);
  };

  const handleModuleChange = (event, newValue) => {
    setSelectedModule(newValue);
  };

  return (
    <Box sx={{ display: 'flex', height: '100%' }}>
      <Tabs
        orientation="vertical"
        variant="scrollable"
        value={selectedScanType}
        onChange={handleScanTypeChange}
        aria-label="Scan Types"
        sx={{ borderRight: 1, borderColor: 'divider', minWidth: 150 }}
      >
        {scanTypes.map((type, index) => (
          <Tab label={type} key={type} />
        ))}
      </Tabs>

      <Box sx={{ flexGrow: 1 }}>
        {scanTypes.length > 0 && (
          <Tabs
            value={selectedModule}
            onChange={handleModuleChange}
            aria-label="Modules"
            variant="scrollable"
            scrollButtons="auto"
          >
            {(modulesByScanType[scanTypes[selectedScanType]] || []).map((mod, idx) => (
              <Tab label={mod} key={mod} />
            ))}
          </Tabs>
        )}

        {(modulesByScanType[scanTypes[selectedScanType]] || []).map((mod, idx) => (
          <TabPanel value={selectedModule} index={idx} key={mod}>
            <Typography variant="h6">{mod} Tools</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              {(toolsByModule[mod] || []).map(tool => (
                <Box
                  key={tool}
                  sx={{
                    border: '1px solid gray',
                    borderRadius: 1,
                    padding: 2,
                    minWidth: 200,
                    maxWidth: 300,
                    height: 150,
                    overflowY: 'auto',
                  }}
                >
                  <Typography variant="subtitle1">{tool}</Typography>
                  <ToolOutput collectionName={scanTypes[selectedScanType]} toolName={tool} />
                </Box>
              ))}
            </Box>
          </TabPanel>
        ))}
      </Box>
    </Box>
  );
}
