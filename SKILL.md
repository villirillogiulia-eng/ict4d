# CSV Visualizer Blueprint & Publishing Skill

This document provides the technical specification and workflow for replicating the **CSV Data Visualizer** web application for any dataset. Use this as a guide to create new "Sentinels" or data tools within this repository.

## 1. Core Functionality Specification

### A. Data Ingestion
- **Formats Supported:** CSV, TXT (Comma-separated).
- **Methods:** File Drag-and-Drop, System File Picker, Clipboard Paste (Global listener included).
- **Parsing Logic:** 
  - Custom `parseCSV` function handles basic comma separation.
  - Supports quoted strings to prevent breaking on commas within fields.
  - Automated header normalization (lowercasing and trimming).

### B. Intelligent Column Mapping
To support various CSV structures, the app uses a "Fuzzy Mapping" strategy for coordinates:
- **Latitude Patterns:** `['lat', 'latitude', 'anonymous_lat', 'y', 'lat_dd', 'latitude_dd']`
- **Longitude Patterns:** `['lon', 'lng', 'long', 'longitude', 'anonymous_long', 'x', 'lon_dd', 'longitude_dd']`
- **Extensibility:** When adapting for new CSVs (e.g., social media data), add relevant patterns like `['geo_lat', 'coord_y']`.

### C. Mapping & Visualization
- **Library:** Leaflet.js with CartoDB Dark Matter tiles.
- **Rendering:** Circle Markers with dynamic scaling based on "Severity" or "Impact" scores.
- **Color Logic:** Gradient scales (Green -> Yellow -> Orange -> Red) based on quantitative thresholds.
- **Popups:** Context-aware popups that display key metadata (ID, Country, Cause, Impact).

### D. Real-time Analysis
- **Filtering:** Dynamic dropdowns for categorical data (e.g., Country, Type) and range sliders for quantitative data (e.g., Severity).
- **Summary Statistics:** Automated calculation of Total Records, Fatalities, Displacements, and Affected Area based on the current filtered view.

## 2. Technical Component Architecture

```html
<!-- Required Libraries -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Key State Variables -->
let rawData = [];      // Original parsed data
let filteredData = []; // Data currently on the map
let map = null;        // Leaflet instance
```

## 3. Deployment & Publishing Process (Mandatory)

To maintain a clean repository structure and ensure separate URLs for each sub-app, follow this exact process:

### Step 1: Subdirectory Isolation
Each new visualizer **must** live in its own subdirectory.
- **Directory Name:** Descriptive and lowercase (e.g., `health-sentinel`, `flood-tracker`).
- **Entry Point:** Always name the main file `index.html` inside that directory.

### Step 2: URL Structure
The app will be published at:
`https://villirillogiulia-eng.github.io/ict4d/[directory-name]/`

### Step 3: Git Workflow
Execute the following commands in order:
1. `mkdir -p [directory-name]`
2. `cp [template_file].html [directory-name]/index.html`
3. `git add [directory-name]/index.html`
4. `git commit -m "feat: deploy [name] visualizer to /[directory-name]/"`
5. `git push origin main`

## 4. Customization Checklist for New Apps
- [ ] **Styles:** Update `:root` CSS variables to match the new project's branding.
- [ ] **Columns:** Add new mapping patterns to `LAT_COLUMNS` and `LON_COLUMNS` if the source CSV uses non-standard names.
- [ ] **Data Model:** Update the `processData` function to map specific CSV columns to the `id`, `lat`, `lon`, and `metadata` properties.
- [ ] **Legend:** Adjust the `getSeverityColor` logic and HTML legend items to reflect the new data's ranges.

---
*Created on April 16, 2026, for the ict4d Gambia Disaster Preparedness Project.*
