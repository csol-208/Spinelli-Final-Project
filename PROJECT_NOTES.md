# California Forest Biomass Resources - Project Development Notes

## Project Overview

This project analyzes California's forest biomass waste resources using data from the 2023 Billion Ton Report. The analysis includes interactive visualizations showing spatial distribution and potential end-use applications for forest biomass.

**Date Created:** February 25, 2026  
**Data Source:** 2023 Billion Ton Report, U.S. Department of Energy

---

## Available Data

The project includes four primary datasets covering California forest biomass resources:

### 1. Forest Processing Waste
- **Records:** 1,800
- **Total Amount:** 23,295 dry tonnes/year
- **Resource Type:** Softwood processing residues
- **Scenario:** Near-term
- **Price:** $54/dry tonne
- **Primary Regions:** Humboldt County and other timber-producing areas

### 2. Logging Residues
- **Records:** 30,180
- **Total Amount:** 2,760,264 dry tonnes/year (74.8% of total)
- **Resource Types:** 
  - Softwood planted logging residues
  - Softwood natural logging residues
- **Scenarios:** Near-term, emerging, mature-market (low/medium/high)
- **Price:** $40/dry tonne
- **Note:** Largest dataset covering multiple future scenarios

### 3. Other Forest Waste
- **Records:** 5,700
- **Total Amount:** 231,199 dry tonnes/year
- **Resource Type:** Forest waste human generated
- **Scenario:** Emerging
- **Price:** $50/dry tonne
- **Primary Regions:** Amador County and surrounding areas

### 4. Small-Diameter Trees
- **Records:** 7,920
- **Total Amount:** 677,269 dry tonnes/year
- **Resource Type:** Softwood natural small-diameter trees
- **Scenario:** Mature-market medium
- **Price:** $70.11/dry tonne
- **Primary Regions:** Del Norte County and northern California

### Total Dataset Summary
- **Total Records:** 45,600 data points
- **Total Annual Biomass:** 3,692,027 dry tonnes/year
- **Coverage:** Statewide California with county-level detail

### Common Data Fields
All datasets include:
- Geographic coordinates (longitude/latitude)
- State/county information with FIPS codes
- Resource amounts in dry tonnes/year
- Scenario types and resource pricing
- Source attribution to 2023 Billion Ton Report

---

## Visualizations Created

### 1. Interactive Resource Map (`california_forest_biomass_map.html`)

**Description:** An interactive folium-based map showing the spatial distribution of forest biomass resources across California.

**Features:**
- Color-coded markers for each resource type:
  - **Teal** - Logging Residues
  - **Red** - Forest Processing Waste
  - **Light Green** - Other Forest Waste
  - **Pink** - Small-Diameter Trees
- Marker size proportional to resource amount
- Interactive layer controls to toggle resource types on/off
- Clickable popups with detailed information:
  - Resource amount
  - County location
  - Scenario type
  - Price per tonne
  - Geographic coordinates
- Fullscreen mode available
- Shows top 500 highest-concentration points per resource type for performance

**Key Findings from Map:**
- Logging residues dominate northern California (Del Norte, Humboldt counties)
- Small-diameter trees concentrated in forested regions
- Processing waste clustered near timber mills
- Clear geographic patterns indicating infrastructure opportunities

### 2. Sankey Flow Diagram (`biomass_sankey_diagram.html`)

**Description:** Interactive Sankey diagram visualizing the potential flow of forest biomass resources to various end-use applications.

**End Use Applications & Allocations:**

1. **Bioenergy & Electricity** - 1,350,936 tonnes/year (36.6%)
   - Forest Processing Waste: 35%
   - Logging Residues: 40%
   - Other Forest Waste: 30%
   - Small-Diameter Trees: 25%

2. **Heat & Thermal Energy** - 717,267 tonnes/year (19.4%)
   - Forest Processing Waste: 25%
   - Logging Residues: 20%
   - Other Forest Waste: 25%
   - Small-Diameter Trees: 15%

3. **Wood Pellets** - 668,119 tonnes/year (18.1%)
   - Forest Processing Waste: 20%
   - Logging Residues: 15%
   - Other Forest Waste: 20%
   - Small-Diameter Trees: 30%

4. **Biofuels (Ethanol/Biodiesel)** - 507,216 tonnes/year (13.7%)
   - Forest Processing Waste: 10%
   - Logging Residues: 15%
   - Other Forest Waste: 10%
   - Small-Diameter Trees: 10%

5. **Biochar & Soil Amendments** - 196,161 tonnes/year (5.3%)
   - Forest Processing Waste: 5%
   - Logging Residues: 5%
   - Other Forest Waste: 10%
   - Small-Diameter Trees: 5%

6. **Biochemicals & Materials** - 252,328 tonnes/year (6.8%)
   - Forest Processing Waste: 5%
   - Logging Residues: 5%
   - Other Forest Waste: 5%
   - Small-Diameter Trees: 15%

**Features:**
- Interactive hover functionality showing exact values
- Color-coded nodes for resources and end uses
- Flow width proportional to biomass volume
- Professional layout with detailed annotations

### 3. Integrated Web Platform (`index.html`)

**Description:** A comprehensive web-based dashboard combining both visualizations with detailed analysis and documentation.

**Design Inspiration:**
- BioSiting Tool (https://biositing.jbei.org/national) - Interactive mapping interface
- EU Woody Biomass Flows (https://knowledge4policy.ec.europa.eu/) - Professional Sankey presentation

**Structure:**
- **Header:** Gradient design with project title and subtitle
- **Navigation Tabs:** Sticky navigation with four sections
  - Overview
  - Resource Map
  - End Use Flows
  - Data Details

**Overview Tab:**
- Key statistics cards showing:
  - Total annual biomass (3.7M tonnes)
  - Number of data points (45,600)
  - Resource categories (4)
  - Potential end uses (6)
- Resource breakdown cards with amounts, percentages, and pricing
- Key insights section with analytical findings

**Resource Map Tab:**
- Embedded interactive map
- Feature descriptions and usage instructions
- Layer control information

**End Use Flows Tab:**
- Statistics cards for top end uses
- Embedded Sankey diagram
- Detailed descriptions of each end-use application:
  - Bioenergy & electricity generation
  - District heating and thermal energy
  - Wood pellet production
  - Advanced biofuels
  - Biochar and soil amendments
  - Biochemicals and bio-based materials

**Data Details Tab:**
- Complete data source information
- Dataset specifications and record counts
- Field descriptions
- Methodology and technical notes
- Data currency and verification information

**Design Features:**
- Responsive layout for mobile and desktop
- Smooth animations and transitions
- Professional color scheme
- Modern card-based interface
- Accessible navigation
- Footer with links to source data

---

## Technical Implementation

### Python Scripts Created

#### 1. `create_resource_map.py`
**Purpose:** Generates the interactive resource map

**Key Libraries:**
- pandas - Data processing
- folium - Interactive mapping
- folium.plugins - Additional map features

**Functionality:**
- Loads all four CSV datasets
- Combines data with resource category labels
- Calculates statistics and summaries
- Creates folium map centered on California
- Adds color-coded circle markers
- Implements feature groups for layer control
- Samples top 500 points per resource type for performance
- Exports to HTML

**Output:** `california_forest_biomass_map.html`

#### 2. `create_sankey_diagram.py`
**Purpose:** Generates the Sankey flow diagram

**Key Libraries:**
- pandas - Data processing
- plotly.graph_objects - Interactive visualizations

**Functionality:**
- Loads and combines all datasets
- Calculates total amounts by resource category
- Defines end-use allocation percentages
- Creates nodes for resources and end uses
- Builds flow connections with values
- Applies color coding
- Generates interactive Sankey diagram
- Exports to HTML

**Output:** `biomass_sankey_diagram.html`

### Python Environment

**Environment Type:** Virtual Environment (.venv)  
**Python Version:** 3.14.3

**Packages Installed:**
- pandas - Data manipulation
- folium - Interactive maps
- matplotlib - Plotting utilities
- numpy - Numerical operations
- plotly - Interactive visualizations
- kaleido - Image export (optional)

---

## Key Insights & Findings

### Resource Distribution
1. **Logging residues dominate** the biomass landscape, representing nearly 75% of total available resources
2. **Geographic concentration** in northern California counties (Del Norte, Humboldt) indicates established timber industry infrastructure
3. **Small-diameter trees** represent 18% of resources with higher market value ($70.11/tonne)
4. **Multiple scenarios** provide flexibility for planning under different market conditions

### End-Use Potential
1. **Bioenergy applications** lead with 36.6% allocation, supporting California's renewable energy goals
2. **Thermal energy** (19.4%) represents significant opportunity for district heating and industrial applications
3. **Wood pellets** (18.1%) offer both domestic and export market potential
4. **Advanced biofuels** (13.7%) align with transportation decarbonization objectives
5. **High-value products** (biochemicals, biochar) represent emerging markets with premium pricing

### Economic Considerations
- Resource pricing ranges from $40-$70.11 per dry tonne
- Total estimated annual resource value: $150-260M depending on end use
- Infrastructure investment needed to optimize collection and processing
- Transportation costs will significantly impact feasibility

### Policy & Planning Implications
1. **Infrastructure development** needed in key resource-rich counties
2. **Multi-use strategies** can optimize value across different end-use pathways
3. **Wildfire mitigation** synergy through small-diameter tree removal
4. **Carbon sequestration** opportunities through biochar production
5. **Energy security** enhancement through local biomass utilization

---

## Project Files

### Data Files (in `/data/` directory)
- `CA_forest_processing_waste_points_BillionTonReport.csv`
- `CA_logging_residues_points_BillionTonReport.csv`
- `CA_other_forest_waste_points_BillionTonReport.csv`
- `CA_small-diameter_trees_points_BillionTonReport.csv`

### Python Scripts
- `create_resource_map.py` - Map generation script
- `create_sankey_diagram.py` - Sankey diagram generation script

### Visualization Outputs
- `california_forest_biomass_map.html` - Interactive resource map
- `biomass_sankey_diagram.html` - Interactive Sankey diagram
- `index.html` - Integrated web dashboard

### Documentation
- `README.md` - Project readme (basic)
- `PROJECT_NOTES.md` - This file (detailed conversation notes)

---

## Development Workflow

### Initial Analysis
1. Examined available data files and structure
2. Read sample records from each dataset
3. Calculated row counts and basic statistics
4. Identified common fields and data patterns

### Visualization Development
1. **Resource Map Creation:**
   - Configured Python environment
   - Installed required packages (pandas, folium)
   - Developed mapping script with interactive features
   - Generated HTML output
   - Tested in VS Code Simple Browser

2. **Sankey Diagram Creation:**
   - Installed plotly for interactive diagrams
   - Defined end-use categories and allocation logic
   - Created flow connections and styling
   - Generated interactive HTML output
   - Tested visualization

3. **Web Dashboard Integration:**
   - Researched reference sites for design inspiration
   - Designed responsive HTML structure
   - Implemented tabbed navigation
   - Created statistics cards and info sections
   - Embedded both visualizations
   - Added comprehensive documentation
   - Styled with modern CSS

### Testing & Refinement
- Opened visualizations in VS Code Simple Browser
- Verified interactive features (layer controls, hover states, popups)
- Ensured responsive design across different viewport sizes
- Validated data accuracy in displays

---

## Future Enhancement Opportunities

### Data Analysis
- Time-series analysis if multi-year data becomes available
- Seasonal availability patterns
- Economic feasibility analysis by county
- Transportation cost modeling
- Carbon accounting and lifecycle analysis

### Visualizations
- Add county-level aggregation view
- Create comparison charts between scenarios
- Develop cost-benefit analysis dashboard
- Add filtering by price point or resource type
- Implement scenario comparison tools

### Web Platform
- Add data export functionality
- Implement user-defined allocation scenarios
- Create printable report generation
- Add search and filter capabilities
- Integrate real-time data updates if available

### Technical Improvements
- Implement database backend for larger datasets
- Add API endpoints for data access
- Create automated data update pipeline
- Optimize performance for full dataset rendering
- Add user authentication for advanced features

---

## Data Source & Attribution

**Primary Source:** 2023 Billion Ton Report  
**Publisher:** U.S. Department of Energy, Bioenergy Technologies Office  
**Data Portal:** https://bioenergykdf.net/bt23-data-portal  
**Report Website:** https://www.energy.gov/eere/bioenergy/2023-billion-ton-report

**Citation:** U.S. Department of Energy. 2023. "2023 Billion-Ton Report: An Assessment of U.S. Renewable Carbon Resources." Bioenergy Technologies Office.

**Data License:** Public domain (U.S. Government work)

---

## Technical Notes

### Performance Optimizations
- Map displays top 500 points per resource category (2,000 total) to maintain responsive performance
- Full dataset contains 45,600 points - can be rendered if needed but may impact load times
- Sankey diagram uses aggregated flows rather than individual point data

### Browser Compatibility
- Tested in VS Code Simple Browser
- Compatible with modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled for interactive features
- Responsive design supports mobile and tablet viewing

### Data Processing Notes
- All amounts in dry tonnes per year
- Coordinate system: WGS84 (standard latitude/longitude)
- FIPS codes included for programmatic county identification
- Some resources appear in multiple scenarios - this is expected and by design

---

## Contact & Collaboration

This project was developed as an analytical tool for understanding California's forest biomass resources. The visualizations and analysis can be adapted for:
- Policy planning and decision support
- Infrastructure investment analysis
- Research and academic studies
- Public education and outreach
- Grant proposals and funding applications

For questions or collaboration opportunities regarding this analysis, refer to the data source contacts at the 2023 Billion Ton Report portal.

---

**Project Status:** Complete  
**Last Updated:** February 25, 2026  
**Version:** 1.0
