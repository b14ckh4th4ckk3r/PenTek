import './ScanDetailsPage.css';
import React, { useState, useEffect } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Typography,
  CircularProgress,
  List,
  ListItemButton,
  ListItemText,
  Collapse,
} from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`vertical-tabpanel-${index}`}
      aria-labelledby={`vertical-tab-${index}`}
      {...other}
      style={{ overflowY: 'auto' }}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function ScanDetailsPage() {
  const { collectionName } = useParams();

  const [scanTypes, setScanTypes] = useState([]);
  const [modulesByScanType, setModulesByScanType] = useState({});
  const [selectedScanTypeIndex, setSelectedScanTypeIndex] = useState(0);
  const [openModules, setOpenModules] = useState({});
  const [selectedModuleIndex, setSelectedModuleIndex] = useState(0);
  const [selectedPortIndex, setSelectedPortIndex] = useState(0);
  const [outputSubTabIndices, setOutputSubTabIndices] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchScanDetails = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`http://localhost:5000/api/scan/details/${collectionName}`);
        const data = response.data;
        const scanTypeKeys = Object.keys(data);
        setScanTypes(scanTypeKeys);
        setModulesByScanType(data);
        setSelectedScanTypeIndex(0);
        setSelectedModuleIndex(0);
        setSelectedPortIndex(0);
        setOutputSubTabIndices({});
        // Initialize all modules as open for collapsible sidebar
        const initialOpenModules = {};
        scanTypeKeys.forEach((type) => {
          initialOpenModules[type] = true;
        });
        setOpenModules(initialOpenModules);
      } catch (error) {
        console.error('Failed to fetch scan details', error);
      } finally {
        setLoading(false);
      }
    };
    fetchScanDetails();
  }, [collectionName]);

  const handleScanTypeChange = (event, newValue) => {
    setSelectedScanTypeIndex(newValue);
    setSelectedModuleIndex(0);
    setSelectedPortIndex(0);
    setOutputSubTabIndices({});
  };

  const handleModuleClick = (index) => {
    setSelectedModuleIndex(index);
    setSelectedPortIndex(0);
    setOutputSubTabIndices({});
  };

  const toggleModule = (type) => {
    setOpenModules((prev) => ({
      ...prev,
      [type]: !prev[type],
    }));
  };

  const handlePortTabChange = (event, newValue) => {
    setSelectedPortIndex(newValue);
    setOutputSubTabIndices({});
  };

  const handleOutputSubTabChange = (portName) => (event, newValue) => {
    setOutputSubTabIndices((prev) => ({
      ...prev,
      [portName]: newValue,
    }));
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (scanTypes.length === 0) {
    return <Typography>No scan details found.</Typography>;
  }

  const selectedScanType = scanTypes[selectedScanTypeIndex];
  const modules = Object.keys(modulesByScanType[selectedScanType] || {});
  const ports = modules.length > 0 ? modulesByScanType[selectedScanType][modules[selectedModuleIndex]] : [];

  // Group tools by port name, then group outputs by scan_subtype
  const groupedByPort = {};
  ports.forEach((tool) => {
    const portName = tool.name || 'Unknown Port';
    if (!groupedByPort[portName]) {
      groupedByPort[portName] = [];
    }
    groupedByPort[portName].push(tool);
  });

  const portNames = Object.keys(groupedByPort);
  const selectedPortName = portNames[selectedPortIndex] || '';
  const selectedPortTools = groupedByPort[selectedPortName] || [];

  // Group selected port tools by scan_subtype
  const groupedBySubType = {};
  selectedPortTools.forEach((tool) => {
    const subType = tool.scan_subtype || 'Output';
    if (!groupedBySubType[subType]) {
      groupedBySubType[subType] = [];
    }
    groupedBySubType[subType].push(tool);
  });

  const subTypeNames = Object.keys(groupedBySubType);
  const selectedSubTabIndex = outputSubTabIndices[selectedPortName] || 0;

  return (
    <Box className="page-container">
      {/* Scan Types Vertical Tabs with collapsible modules */}
      <Tabs
        orientation="vertical"
        variant="scrollable"
        value={selectedScanTypeIndex}
        onChange={handleScanTypeChange}
        aria-label="Scan Types"
        className="scan-types-tabs"
      >
        {scanTypes.map((type, index) => {
          const modulesForType = Object.keys(modulesByScanType[type] || {});
          return (
            <div key={type} className="collapsible-tab">
              <ListItemButton onClick={() => toggleModule(type)} sx={{ pl: 2 }}>
                <ListItemText primary={type} />
                {openModules[type] ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
              <Collapse in={openModules[type]} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                  {modulesForType.map((module, idx) => (
                    <ListItemButton
                      key={module}
                      selected={selectedScanTypeIndex === index && selectedModuleIndex === idx}
                      onClick={() => handleModuleClick(idx)}
                      className={`modules-list-item ${
                        selectedScanTypeIndex === index && selectedModuleIndex === idx ? 'selected' : ''
                      }`}
                      sx={{ pl: 4 }}
                    >
                      <ListItemText primary={module} />
                    </ListItemButton>
                  ))}
                </List>
              </Collapse>
            </div>
          );
        })}
      </Tabs>

      {/* Port Tabs and Outputs stacked vertically */}
      <Box className="port-tabs-and-output" sx={{ marginLeft: 2, width: '100%' }}>
        <Box className="port-tabs-container">
          <Tabs
            value={selectedPortIndex}
            onChange={handlePortTabChange}
            aria-label="Port Tabs"
            variant="scrollable"
            scrollButtons="auto"
          >
            {portNames.map((portName, idx) => (
              <Tab key={idx} label={portName} />
            ))}
          </Tabs>
        </Box>

        <Box className="port-output-container" sx={{ marginTop: 2 }}>
          {subTypeNames.length === 0 ? (
            <Typography>No outputs found.</Typography>
          ) : (
            <>
              <Tabs
                value={selectedSubTabIndex}
                onChange={handleOutputSubTabChange(selectedPortName)}
                aria-label="Output Sub Tabs"
                variant="scrollable"
                scrollButtons="auto"
                sx={{ marginBottom: 2 }}
              >
                {subTypeNames.map((subType, idx) => (
                  <Tab key={idx} label={subType} />
                ))}
              </Tabs>
              {subTypeNames.map((subType, idx) => {
                const tools = groupedBySubType[subType];
                return (
                  <TabPanel key={idx} value={selectedSubTabIndex} index={idx}>
                    {tools.map((tool, toolIdx) => {
                      const fullOutput =
                        tool.output?.full || (typeof tool.output === 'string' ? tool.output : 'No full output available.');
                      return (
                        <Box
                          key={toolIdx}
                          sx={{
                            marginBottom: 3,
                            padding: 2,
                            border: '1px solid #ccc',
                            borderRadius: 1,
                            backgroundColor: '#fafafa',
                            width: '600px',
                            maxWidth: '100%',
                          }}
                        >
                          <Typography variant="h6" gutterBottom>
                            {tool.name || 'Output'}
                          </Typography>
                          <Typography
                            variant="body2"
                            component="pre"
                            sx={{ whiteSpace: 'pre-wrap', maxHeight: 300, overflowY: 'auto' }}
                          >
                            {fullOutput}
                          </Typography>
                        </Box>
                      );
                    })}
                  </TabPanel>
                );
              })}
            </>
          )}
        </Box>
      </Box>
    </Box>
  );
}
