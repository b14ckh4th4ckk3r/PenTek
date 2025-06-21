import React, { useState, useEffect, Fragment } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import {
  Box,
  List,
  ListItemButton,
  ListItemText,
  Collapse,
  Tabs,
  Tab,
  Typography,
  CircularProgress,
} from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import axios from 'axios';
import './ScanDetailsPage.css';

function TabPanel({ children, value, index }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      aria-labelledby={`tab-${index}`}
      style={{ overflowY: 'auto' }}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function ScanDetailsPage() {
  const { collectionName } = useParams();
  const location = useLocation();
  const state = location.state || {};

  const [modulesByScanType, setModulesByScanType] = useState({});
  const [scanTypes, setScanTypes] = useState([]);
  const [loading, setLoading] = useState(true);

  // Sidebar state
  const [selectedScanTypeIndex, setSelectedScanTypeIndex] = useState(0);
  const [openModules, setOpenModules] = useState({});
  const [selectedModuleIndex, setSelectedModuleIndex] = useState(0);

  // Port-tabs state
  const [selectedPortIndex, setSelectedPortIndex] = useState(0);
  const [outputSubTabIndices, setOutputSubTabIndices] = useState({});

  useEffect(() => {
    const buildFromArray = (items) => {
      if (!Array.isArray(items)) return false;
      const byType = {};
      items.forEach((it) => {
        byType[it.scan_type] = byType[it.scan_type] || {};
        byType[it.scan_type][it.module] = byType[it.scan_type][it.module] || [];
        byType[it.scan_type][it.module].push(it);
      });
      setModulesByScanType(byType);
      const types = Object.keys(byType);
      setScanTypes(types);
      const opens = {};
      types.forEach((t) => (opens[t] = true));
      setOpenModules(opens);
      return true;
    };

    const buildFromObject = (obj) => {
      if (obj && typeof obj === 'object' && !Array.isArray(obj)) {
        setModulesByScanType(obj);
        const types = Object.keys(obj);
        setScanTypes(types);
        const opens = {};
        types.forEach((t) => (opens[t] = true));
        setOpenModules(opens);
        return true;
      }
      return false;
    };

    const data = state.items ?? null;
    if (buildFromArray(data)) {
      setLoading(false);
    } else {
      axios
        .get(`http://localhost:5000/api/scan/details/${collectionName}`)
        .then((res) => {
          const d = res.data;
          if (!buildFromArray(d)) {
            buildFromObject(d);
          }
        })
        .catch((err) => console.error('Fetch failed:', err))
        .finally(() => setLoading(false));
    }
  }, [state, collectionName]);

  if (loading) return <CircularProgress sx={{ m: 2 }} />;
  if (!scanTypes.length) return <Typography sx={{ m: 2 }}>No scan details found.</Typography>;

  const selectedScanType = scanTypes[selectedScanTypeIndex];
  const modulesForSelectedType = Object.keys(modulesByScanType[selectedScanType] || {});
  const tools = modulesForSelectedType.length
    ? modulesByScanType[selectedScanType][modulesForSelectedType[selectedModuleIndex]]
    : [];

  const byPort = {};
  tools.forEach((tool) => {
    const port = tool.name || 'Unknown';
    byPort[port] = byPort[port] || [];
    byPort[port].push(tool);
  });
  const portNames = Object.keys(byPort);

  const selectedPortName = portNames[selectedPortIndex] || '';
  const portTools = byPort[selectedPortName] || [];

  const bySub = {};
  portTools.forEach((t) => {
    const s = t.scan_subtype || 'Output';
    bySub[s] = bySub[s] || [];
    bySub[s].push(t);
  });
  const subTypes = Object.keys(bySub);
  const subIndex = outputSubTabIndices[selectedPortName] || 0;

  const handleScanTypeClick = (index) => {
    setSelectedScanTypeIndex(index);
    setSelectedModuleIndex(0);
    setSelectedPortIndex(0);
    setOutputSubTabIndices({});
  };

  const toggleModule = (type) => {
    setOpenModules((o) => ({ ...o, [type]: !o[type] }));
  };

  const handleModuleClick = (index) => {
    setSelectedModuleIndex(index);
    setSelectedPortIndex(0);
    setOutputSubTabIndices({});
  };

  const handlePortChange = (_, i) => {
    setSelectedPortIndex(i);
    setOutputSubTabIndices({});
  };

  const handleSubChange = (port) => (_, i) => {
    setOutputSubTabIndices((o) => ({ ...o, [port]: i }));
  };

  return (
    <div className="scan-details-page">
    <Box className="page-container">
      <Box className="sidebar">
        <List disablePadding>
          {scanTypes.map((type, ti) => {
            const modulesForType = Object.keys(modulesByScanType[type] || {});
            return (
              <Fragment key={type}>
                <ListItemButton
                  selected={ti === selectedScanTypeIndex}
                  onClick={() => handleScanTypeClick(ti)}
                >
                  <ListItemText primary={type.toUpperCase()} />
                  {openModules[type] ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
                <Collapse in={openModules[type]} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding>
                    {modulesForType.map((mod, mi) => (
                      <ListItemButton
                        key={mod}
                        selected={ti === selectedScanTypeIndex && mi === selectedModuleIndex}
                        onClick={() => handleModuleClick(mi)}
                        sx={{ pl: 4 }}
                      >
                        <ListItemText primary={mod} />
                      </ListItemButton>
                    ))}
                  </List>
                </Collapse>
              </Fragment>
            );
          })}
        </List>
      </Box>

      <Box className="port-tabs-and-output">
        <Tabs
          value={selectedPortIndex}
          onChange={handlePortChange}
          variant="scrollable"
          scrollButtons="auto"
        >
          {portNames.map((p) => (
            <Tab key={p} label={p} />
          ))}
        </Tabs>

        <Box className="port-output-container">
          {subTypes.length === 0 ? (
            <Typography>No outputs found.</Typography>
          ) : (
            <>
              <Tabs
                value={subIndex}
                onChange={handleSubChange(selectedPortName)}
                variant="scrollable"
                scrollButtons="auto"
                sx={{ mb: 2 }}
              >
                {subTypes.map((s) => (
                  <Tab key={s} label={s} />
                ))}
              </Tabs>

              {subTypes.map((s, si) => (
                <TabPanel key={s} value={subIndex} index={si}>
                  {bySub[s].map((tool, idx) => (
                    <Box
                      key={idx}
                      sx={{ mb: 2, p: 2, border: '1px solid #ccc', borderRadius: 1 }}
                    >
                      <Typography variant="h6" gutterBottom>
                        {tool.name}
                      </Typography>
                      <Typography component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                        {tool.output?.full ?? tool.output ?? 'No output'}
                      </Typography>
                    </Box>
                  ))}
                </TabPanel>
              ))}
            </>
          )}
        </Box>
      </Box>
    </Box>
    </div>
  );
  
}
