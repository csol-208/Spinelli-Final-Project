# California Forest Biomass Resources Analysis

An interactive web-based analysis of California's forest biomass waste resources, featuring spatial distribution mapping and end-use flow visualization using data from the 2023 Billion Ton Report.

## 🎯 Project Overview

This project analyzes **3.7 million dry tonnes per year** of forest biomass resources across California, visualizing their spatial distribution and potential applications through interactive maps and flow diagrams. The analysis supports decision-making for renewable energy planning, wildfire mitigation, and sustainable forest management.

### Key Features

- **Interactive Resource Map**: Geographic visualization of 45,600 data points showing forest biomass distribution across California
- **Sankey Flow Diagram**: Interactive flow visualization of biomass allocation to six end-use applications
- **Integrated Web Dashboard**: Professional web interface combining both visualizations with detailed analytics and documentation

## 📊 Dataset Summary

The project analyzes four primary forest biomass resource categories:

| Resource Type | Annual Volume | % of Total | Records | Price/Tonne |
|--------------|---------------|------------|---------|-------------|
| Logging Residues | 2,760,264 tonnes | 74.8% | 30,180 | $40 |
| Small-Diameter Trees | 677,269 tonnes | 18.3% | 7,920 | $70.11 |
| Other Forest Waste | 231,199 tonnes | 6.3% | 5,700 | $50 |
| Forest Processing Waste | 23,295 tonnes | 0.6% | 1,800 | $54 |
| **Total** | **3,692,027 tonnes** | **100%** | **45,600** | - |

**Data Source**: [2023 Billion Ton Report](https://www.energy.gov/eere/bioenergy/2023-billion-ton-report), U.S. Department of Energy

## 🚀 Quick Start

### View the Dashboard

Simply open `index.html` in any modern web browser to access the full interactive dashboard.

```bash
open index.html
```

Or view individual visualizations:
- `california_forest_biomass_map.html` - Resource map
- `biomass_sankey_diagram.html` - Sankey diagram

### Running the Analysis Scripts

#### Prerequisites

- Python 3.8 or higher
- pip package manager

#### Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

2. Install required packages:
```bash
pip install pandas folium plotly matplotlib numpy
```

#### Generate Visualizations

```bash
# Generate the resource map
python create_resource_map.py

# Generate the Sankey diagram
python create_sankey_diagram.py
```

## 📁 Project Structure

```
Spinelli-Final-Project/
├── index.html                          # Main dashboard (start here!)
├── california_forest_biomass_map.html  # Interactive resource map
├── biomass_sankey_diagram.html         # Sankey flow diagram
├── create_resource_map.py              # Map generation script
├── create_sankey_diagram.py            # Sankey generation script
├── README.md                           # This file
├── PROJECT_NOTES.md                    # Detailed development notes
└── data/
    ├── CA_forest_processing_waste_points_BillionTonReport.csv
    ├── CA_logging_residues_points_BillionTonReport.csv
    ├── CA_other_forest_waste_points_BillionTonReport.csv
    └── CA_small-diameter_trees_points_BillionTonReport.csv
```

## 🗺️ Interactive Map Features

The resource map provides:

- **Color-coded markers** by resource type:
  - 🔵 Teal - Logging Residues
  - 🔴 Red - Forest Processing Waste
  - 🟢 Light Green - Other Forest Waste
  - 🩷 Pink - Small-Diameter Trees
- **Proportional marker sizing** based on resource amount
- **Layer controls** to toggle resource types on/off
- **Interactive popups** with detailed information
- **Fullscreen mode** for detailed exploration
- Top 500 concentration points per resource type (2,000 total points displayed)

## 📈 End-Use Applications

The Sankey diagram shows potential allocation of forest biomass to six applications:

1. **Bioenergy & Electricity** (36.6%) - 1,350,936 tonnes/year
2. **Heat & Thermal Energy** (19.4%) - 717,267 tonnes/year
3. **Wood Pellets** (18.1%) - 668,119 tonnes/year
4. **Biofuels** (13.7%) - 507,216 tonnes/year
5. **Biochar & Soil Amendments** (5.3%) - 196,161 tonnes/year
6. **Biochemicals & Materials** (6.8%) - 252,328 tonnes/year

## 🔍 Key Insights

### Geographic Distribution
- **Northern California concentration**: Logging residues and small-diameter trees dominate Del Norte and Humboldt counties
- **Established infrastructure**: Processing waste clustering indicates existing timber mill locations
- **Statewide coverage**: Resources available across multiple regions for distributed utilization

### Economic Potential
- **Total resource value**: $150-260M annually (depending on end use)
- **Price range**: $40-$70.11 per dry tonne
- **Premium products**: Biochemicals and small-diameter trees offer higher value opportunities

### Policy Implications
- Supports California's renewable energy and carbon neutrality goals
- Wildfire mitigation synergy through small-diameter tree removal
- Infrastructure investment opportunities in resource-rich counties
- Multi-use strategies optimize value across different pathways

## 🛠️ Technologies Used

- **Python**: Data processing and visualization generation
  - pandas: Data manipulation
  - folium: Interactive mapping
  - plotly: Sankey diagrams
- **HTML/CSS/JavaScript**: Web dashboard and user interface
- **VS Code**: Development environment

## 📖 Documentation

For detailed technical documentation, development workflow, and analytical findings, see [PROJECT_NOTES.md](PROJECT_NOTES.md).

## 📊 Data Source & Citation

**Primary Source**: 2023 Billion Ton Report  
**Publisher**: U.S. Department of Energy, Bioenergy Technologies Office  
**Data Portal**: https://bioenergykdf.net/bt23-data-portal  
**Report Website**: https://www.energy.gov/eere/bioenergy/2023-billion-ton-report

**Citation**: U.S. Department of Energy. 2023. "2023 Billion-Ton Report: An Assessment of U.S. Renewable Carbon Resources." Bioenergy Technologies Office.

**License**: Public domain (U.S. Government work)

## 🔮 Future Enhancements

Potential additions to the project:
- County-level aggregation views
- Scenario comparison tools
- Transportation cost modeling
- Economic feasibility analysis
- Data export functionality
- Time-series analysis (if multi-year data becomes available)

## 📧 Contact

For questions about this analysis or collaboration opportunities, refer to the contacts at the [2023 Billion Ton Report data portal](https://bioenergykdf.net/bt23-data-portal).

---

**Project Status**: Complete  
**Version**: 1.0  
**Last Updated**: February 25, 2026