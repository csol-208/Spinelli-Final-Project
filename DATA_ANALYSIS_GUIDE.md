# California Biomass Resources: Comprehensive Data Analysis Guide

## Overview

You have a **complete biomass resource assessment system** for California that goes far beyond forest waste. This is a comprehensive database that maps the **entire circular bioeconomy** potential for the state.

---

## The Big Picture: What Story Can Be Told

This dataset allows you to paint a complete picture of California's **renewable carbon resources** and answer critical questions:

### 🌍 **The Circular Bioeconomy Story**

1. **Resource Availability**: How much biomass is available across ALL sectors?
   - Agricultural waste (crops, orchards, field residues)
   - Animal agriculture (manure, bedding)
   - Urban waste (MSW - food, paper, cardboard, green waste)
   - Forest management (small-diameter trees, logging residues)
   - Industrial processing (food/beverage processors, mills, wineries)

2. **Geographic Distribution**: Where are the resources AND where are the processing facilities?
   - Match supply (biomass sources) with demand (processing facilities)
   - Identify infrastructure gaps
   - Optimize collection and transportation logistics

3. **Economic Development Opportunities**: 
   - Which counties have the most biomass potential?
   - Where should new biorefinery facilities be located?
   - What are the optimal feedstock combinations?

4. **Environmental Impact**:
   - Waste diversion from landfills
   - Greenhouse gas emission reductions
   - Renewable energy generation potential
   - Wildfire risk mitigation (forest biomass)

---

## How the Datasets Work Together

### 📊 **Three-Layer Data Architecture**

#### **LAYER 1: County-Level Gross Resources** (25 files)
These files show WHAT and HOW MUCH biomass is available

**File Naming Convention**: `CA_gross[type][year].csv`

##### Agricultural Residues:
- **`CA_grossfieldres[14/20/50].csv`** - Field crop residues (corn, wheat, rice, cotton, etc.)
  - By county, by crop type
  - Different years (2014 baseline, 2020, 2050 projections)
  
- **`CA_grossorchres[14/20/50].csv`** - Orchard residues (prunings, trimmings)
  - Almonds, walnuts, citrus, stone fruits, etc.
  
- **`CA_grossrowres[14/20/50].csv`** - Row crop residues (vegetables, melons, etc.)

##### Crop Culls (unmarketable but usable):
- **`CA_grossorchcull[20/50].csv`** - Orchard culls
- **`CA_grossrowculls[20/50].csv`** - Row crop culls
- **`CA_grossrowcull14.csv`** - 2014 baseline

##### Animal Agriculture:
- **`CA_grossmanure.csv`** - Animal manure by livestock type
  - Dairy cattle, beef, layers, broilers, turkeys, hogs, goats, sheep, horses
  - Total: **~11 million wet tonnes/year**
  
- **`CA_grossbedding.csv`** - Animal bedding waste

##### Food Processing Residues:
- **`CA_grossprocHMS[14].csv`** - High Moisture Solids (wet processing waste)
- **`CA_grossprocLMS[14].csv`** - Low Moisture Solids (dry processing waste)
- **`CA_grossprocMSW[14].csv`** - Municipal solid waste from processors

##### Municipal Solid Waste:
- **`CA_grossMSW[20/50].csv`** - MSW by type (lumber, paper, cardboard, green, food, FOG, other)
  - Two scenarios per file: Baseline vs. High Recycle
  - Massive potential: **~550,000 tonnes/year across categories**

##### Other Specialized:
- **`CA_olivestonefruitpits.csv`** - Pits from processing (olive, stone fruits)

**KEY INSIGHT**: These files tell you the TOTAL POTENTIAL by county, but not WHERE specifically.

---

#### **LAYER 2: Geographic Point Data** (4 files + forest data)
These files show WHERE infrastructure and resources are located

##### Processing & Infrastructure Facilities:

**`CA_proc_points.csv`** (713 facilities)
- **What it contains**: Actual processing facilities that GENERATE biomass waste
- **Categories**: 
  - Almond processors (60) - hulls, shells
  - Walnut processors (65) - shells
  - Wineries (20) - pomace, stems, lees
  - Breweries/Distilleries (74) - spent grains, mash
  - Canneries (48) - fruit/vegetable waste
  - Dehydrators (44) - processing residues
  - Red meat processors (63) - organic waste
  - Rice mills (23) - hulls, bran
  - Bakeries (65) - food waste
  - Cotton gins (18) - gin trash
  - Dairies (35) - whey, processing waste
  - And many more...

- **Geographic data**: Exact addresses, lat/lon, county, city
- **Value**: Shows WHERE processing residues are being generated

**`CA_des_points.csv`** (49 locations)
- **What it contains**: Distributed Energy Systems (DES)
- **Types**: Cogeneration plants, district heating/cooling systems
- **Details**: Capacity (heating/cooling kW, CHP capacity), fuel type, use type
- **Examples**: Universities, hospitals, military bases, industrial facilities
- **Value**: Shows existing energy infrastructure that could potentially use biomass

**`CA_comb_points.csv`** (40 locations)
- **What it contains**: Combined Heat & Power (CHP) facilities
- **Value**: Existing facilities that could be biomass-fueled

**`CA_wte_points.csv`** (9 locations)
- **What it contains**: Waste-to-Energy facilities
- **Value**: Existing biomass conversion infrastructure

##### Forest Biomass (from your existing data):
- Forest processing waste points
- Logging residue points
- Other forest waste points
- Small-diameter trees points

**KEY INSIGHT**: These files tell you WHERE to find resources and infrastructure geographically.

---

#### **LAYER 3: Supporting Data** (7 files)
These files provide CONTEXT and CALCULATION parameters

- **`CA_data_dictionary.csv`** - Explains all the codes and abbreviations
- **`CA_cattlepopulation.csv`** - Livestock numbers by county
- **`CA_livestockpopulation.csv`** - All livestock populations
- **`CA_manureyields.csv`** - How much manure per animal type
- **`CA_manureschedule.csv`** - Manure characteristics by animal
- **`CA_beddingyield.csv`** - Bedding waste generation rates

**KEY INSIGHT**: These files explain HOW the estimates were calculated and provide validation data.

---

## How They Work Together: Use Cases

### 🎯 **Use Case 1: Biorefinery Site Selection**

**Question**: Where should we build a new biorefinery in California?

**Data Integration**:
1. **Aggregate county-level data** to identify high-biomass regions
   - Combine `grossmanure`, `grossfieldres20`, `grossMSW20`
   - Calculate total available biomass by county
   
2. **Map processing facilities** (`proc_points.csv`)
   - Identify clusters of food processors
   - These are SOURCES of additional processing residues
   
3. **Check existing infrastructure** (`des_points`, `comb_points`, `wte_points`)
   - Are there existing energy facilities that could be upgraded?
   
4. **Forest biomass overlay** (your existing maps)
   - Add forest resources for counties with both ag and forest potential

**Result**: A map showing optimal locations considering:
- Total biomass availability
- Proximity to processing facilities (feedstock sources)
- Existing energy infrastructure
- Transportation logistics (highway access, rail)

---

### 🎯 **Use Case 2: Sector-by-Sector Analysis**

**Question**: Which sector has the most biomass potential in California?

**Analysis**:
```
AGRICULTURE:
├── Crop Residues: Field + Orchard + Row = ~X million tonnes
├── Crop Culls: ~Y million tonnes  
├── Animal Manure: ~11 million wet tonnes (convert to dry tonnes)
└── Animal Bedding: ~Z thousand tonnes

MUNICIPAL WASTE:
├── Food Waste: ~550,000 tonnes/year
├── Green Waste: ~X tonnes/year
├── Paper/Cardboard: ~X tonnes/year
└── Wood/Lumber: ~X tonnes/year

INDUSTRIAL:
├── Food Processing (from proc_points): ~X tonnes/year
├── Beverage Processing: ~Y tonnes/year
└── Nut Hulls/Shells: ~Z tonnes/year

FOREST:
├── Logging Residues: 2.76 million dry tonnes/year
├── Small-Diameter Trees: 677k dry tonnes/year
├── Forest Processing: 23k dry tonnes/year
└── Other Forest Waste: 231k dry tonnes/year

TOTAL = Comprehensive California Bioeconomy Potential
```

**Result**: A comprehensive Sankey diagram showing ALL biomass flows from ALL sectors to potential end uses.

---

### 🎯 **Use Case 3: County-Level Economic Development**

**Question**: What is the bioeconomy potential for [specific county]?

**Analysis** (Example: Fresno County):
1. **Agricultural potential**:
   - Sum all `gross*` files for Fresno County
   - Field residues, orchard residues, row crops
   
2. **Processing facilities**:
   - Count facilities in `proc_points.csv` where County=Fresno
   - Identify types: almonds, wineries, dairies, canneries, etc.
   
3. **Animal agriculture**:
   - Get livestock populations from `cattlepopulation.csv`
   - Calculate manure potential using `manureyields.csv`
   
4. **MSW potential**:
   - Get Fresno row from `grossMSW20.csv`

**Result**: A county-specific report showing:
- Total biomass resource: XX thousand tonnes/year
- Primary sources: Agriculture (X%), Processing (Y%), MSW (Z%)
- Existing infrastructure: N processing facilities
- Economic value: $XX million/year potential
- Job creation potential: XXX jobs

---

### 🎯 **Use Case 4: Supply Chain Optimization**

**Question**: How do we efficiently collect and transport biomass to processing facilities?

**Data Integration**:
1. **Map resource density** (county-level gross data)
   - Heat map of biomass availability
   
2. **Overlay facility locations** (proc_points, wte_points)
   - These are COLLECTION points (they generate waste)
   
3. **Add potential conversion facilities** (des_points, comb_points)
   - These could be DESTINATION points for biomass
   
4. **Calculate optimal routes**
   - Minimize transportation distance
   - Maximize feedstock diversity
   - Consider seasonal availability

**Result**: A logistics optimization model showing:
- Optimal collection routes
- Hub-and-spoke collection centers
- Transportation cost analysis
- Seasonal supply curves

---

### 🎯 **Use Case 5: Time-Series Scenario Analysis**

**Question**: How will biomass availability change over time?

**Analysis**:
Compare files with different years:
- **2014 baseline**: `grossfieldres14`, `grossprocHMS14`, etc.
- **2020 projection**: `grossfieldres20`, `grossMSW20`, etc.
- **2050 projection**: `grossfieldres50`, `grossMSW50`, etc.

**Consider scenarios**:
- **MSW**: Baseline vs. High Recycle scenarios
  - Shows impact of recycling programs on available feedstock
- **Agricultural**: Changes in crop production, land use
- **Forest**: Near-term vs. mature-market scenarios

**Result**: Interactive scenario comparison showing:
- Growth/decline in different sectors
- Impact of policy decisions (recycling, land use)
- Future infrastructure needs

---

## Data Quality & Completeness Notes

### Strengths:
✅ **Comprehensive coverage** of all major biomass sectors
✅ **Geographic specificity** - county level + point locations
✅ **Multiple time horizons** - historical, current, projected
✅ **Scenario analysis** - baseline vs. alternative futures
✅ **Real facility data** - actual addresses and companies

### Gaps & Considerations:
⚠️ **Moisture content**: Different units across datasets
   - Forest data: dry tonnes/year
   - Manure data: wet tonnes
   - Need conversion factors (in supporting files)

⚠️ **Collectability**: Not all biomass is practically collectible
   - Field residues: Need to leave some for soil health
   - Manure: Collection varies by animal housing type
   - MSW: Contamination and sorting challenges

⚠️ **Seasonality**: 
   - Crop residues: seasonal (harvest time)
   - Manure: year-round but varies with herd size
   - Forest: project-based, not continuous

⚠️ **Competition for resources**:
   - Animal bedding needs (can't use all crop residues)
   - Composting (some organics better for compost)
   - Paper recycling (competes with bioenergy use)

---

## Recommended Visualizations

### 1. **Interactive Multi-Layer Map**
- **Base layer**: County boundaries with heat map of total biomass
- **Toggle layers**:
  - Processing facilities (by type)
  - DES/CHP facilities
  - WTE facilities
  - Forest biomass concentration
- **Popups**: Click county for detailed breakdown

### 2. **Comprehensive Sankey Diagram**
- **Left side**: ALL biomass sources (agriculture, forest, MSW, processing)
- **Middle**: Resource types (food waste, manure, crop residues, etc.)
- **Right side**: End uses (bioenergy, biofuels, biochar, compost, etc.)
- **Interactive**: Filter by sector, county, or scenario

### 3. **County Comparison Dashboard**
- **Bar charts**: Top 20 counties by biomass potential
- **Pie charts**: Sector breakdown for selected county
- **Timeline**: Historical to projected (2014→2020→2050)

### 4. **Facility Network Diagram**
- **Nodes**: Processing facilities sized by potential waste generation
- **Edges**: Optimal transportation routes to conversion facilities
- **Colors**: Facility type or biomass type

### 5. **Economic Potential Calculator**
- **Interactive tool**: User selects county + resource types
- **Output**: 
  - Total available biomass
  - Potential products (electricity, fuel, heat)
  - Economic value ($)
  - Job creation potential
  - GHG emissions avoided

---

## Data Integration Strategy

### Step 1: Data Cleaning & Standardization
```python
# Convert all to common units (dry tonnes/year)
# Parse county names consistently
# Handle missing data ("-", "(D)", etc.)
# Extract numeric values from formatted strings ("30,612" → 30612)
```

### Step 2: Build Master Database
```python
# Create unified table:
# - County
# - Resource_Category (Agriculture/Forest/MSW/Processing)
# - Resource_Type (Manure/Field_Res/Orchard_Res/etc.)
# - Sub_Type (Specific crop, animal, waste type)
# - Amount (dry tonnes/year)
# - Year/Scenario
# - Lat/Lon (for point data)
```

### Step 3: Calculate Totals
```python
# Sum by county, by sector, by type
# Create aggregation at multiple levels
# Calculate percentages and rankings
```

### Step 4: Build Visualizations
```python
# Generate interactive maps (folium)
# Create Sankey diagrams (plotly)
# Build dashboards (plotly dash or streamlit)
```

---

## Key Questions This Dataset Can Answer

### Resource Assessment:
- ✅ What is California's total biomass resource potential?
- ✅ How does it break down by sector and county?
- ✅ What are the top 10 counties for biomass development?
- ✅ Which resource types are most abundant?

### Infrastructure Planning:
- ✅ Where are the existing processing facilities?
- ✅ Where are the gaps in collection infrastructure?
- ✅ Which counties need new biorefinery investment?
- ✅ Can existing energy facilities be upgraded to use biomass?

### Economic Development:
- ✅ What is the economic value of California's biomass?
- ✅ How many jobs could the bioeconomy create?
- ✅ Which industries generate the most processing residues?
- ✅ What are the optimal feedstock combinations?

### Environmental Impact:
- ✅ How much waste can be diverted from landfills?
- ✅ What are the GHG emission reduction potentials?
- ✅ How much renewable energy can be generated?
- ✅ What is the wildfire mitigation potential?

### Policy & Planning:
- ✅ How do recycling policies impact biomass availability?
- ✅ What infrastructure investments have the highest ROI?
- ✅ How will biomass availability change over time?
- ✅ What regulatory changes would maximize bioeconomy development?

---

## Next Steps: Building the Analysis

### Immediate Actions:
1. **Parse and clean the county-level data**
   - Remove formatting, handle missing values
   - Convert to consistent units
   
2. **Calculate total potentials**
   - Sum across all counties
   - Break down by major categories
   
3. **Create basic visualizations**
   - Simple bar charts of totals
   - County comparison maps
   
4. **Build processing facility map**
   - Plot all 713 facilities
   - Color code by type
   - Add popups with details

### Advanced Analysis:
5. **Build comprehensive Sankey**
   - All sectors flowing to end uses
   - Interactive filtering
   
6. **Create county dashboard**
   - Drill-down capability
   - Comparison tool
   
7. **Economic valuation model**
   - Price data for different products
   - Cost estimates for collection/processing
   
8. **Optimization model**
   - Facility location optimization
   - Route planning
   - Feedstock mixing scenarios

---

## The Bottom Line

You have a **complete circular bioeconomy dataset** for California. This isn't just about forest biomass anymore - it's about:

- **Agricultural residues** from California's massive farming industry
- **Animal manure** from livestock operations (11 million tonnes/year!)
- **Municipal solid waste** from urban areas (food, green waste, paper)
- **Processing residues** from 713+ food & beverage facilities
- **Forest biomass** from sustainable forest management

**Total Potential**: Likely **50-100+ million tonnes per year** of renewable carbon resources

**Value Proposition**: 
- Renewable energy generation
- Waste diversion and GHG reduction
- Rural economic development
- Circular economy job creation
- Energy independence

This dataset allows you to build a **comprehensive roadmap for California's bioeconomy transition** - showing not just what's possible, but WHERE and HOW to make it happen.
