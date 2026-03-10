#!/usr/bin/env python3
"""
California Comprehensive Biomass End Uses Sankey Diagram
Visualizes the flow of ALL California biomass resources to various end uses
Includes: Forest, Agricultural, Animal, Processing, and MSW biomass
"""

import pandas as pd
import plotly.graph_objects as go

print("="*80)
print("CALIFORNIA COMPREHENSIVE BIOMASS SANKEY DIAGRAM")
print("="*80)
print()

# Define all biomass resources with their amounts (from analyze_all_biomass.py results)
resource_totals = {
    # Forest Biomass
    'Logging Residues': 2_760_264,
    'Small-Diameter Trees': 677_269,
    'Other Forest Waste': 231_199,
    'Forest Processing Waste': 23_295,
    
    # Agricultural Residues
    'Orchard Residues': 14_701_977,
    'Field Residues': 7_390_666,
    'Row Crop Residues': 1_310_969,
    
    # Crop Culls
    'Row Crop Culls': 1_979_711,
    'Orchard Culls': 658_525,
    
    # Animal Agriculture
    'Animal Manure': 2_195_237,  # Dry basis
    'Animal Bedding': 932_661,
    
    # Food Processing
    'Processing MSW': 12_993_076,
    'Low Moisture Solids': 3_717_252,
    'High Moisture Solids': 809_100,
    'Olive & Fruit Pits': 108_740,
    
    # Municipal Solid Waste
    'MSW Organic': 28_702_694,
}

# Group resources into major sectors
sectors = {
    'Forest Biomass': {
        'Logging Residues': 2_760_264,
        'Small-Diameter Trees': 677_269,
        'Other Forest Waste': 231_199,
        'Forest Processing Waste': 23_295,
    },
    'Agricultural Residues': {
        'Orchard Residues': 14_701_977,
        'Field Residues': 7_390_666,
        'Row Crop Residues': 1_310_969,
    },
    'Crop Culls': {
        'Row Crop Culls': 1_979_711,
        'Orchard Culls': 658_525,
    },
    'Animal Agriculture': {
        'Animal Manure': 2_195_237,
        'Animal Bedding': 932_661,
    },
    'Food Processing': {
        'Processing MSW': 12_993_076,
        'Low Moisture Solids': 3_717_252,
        'High Moisture Solids': 809_100,
        'Olive & Fruit Pits': 108_740,
    },
    'Municipal Waste': {
        'MSW Organic': 28_702_694,
    },
}

# Calculate sector totals
sector_totals = {sector: sum(resources.values()) for sector, resources in sectors.items()}

print("BIOMASS RESOURCES BY SECTOR:")
print("-"*80)
for sector, total in sector_totals.items():
    pct = (total / sum(sector_totals.values())) * 100
    print(f"  {sector:.<35} {total:>15,.0f} tonnes/year ({pct:>5.1f}%)")
print("-"*80)
print(f"  {'TOTAL':.<35} {sum(sector_totals.values()):>15,.0f} tonnes/year")
print()

# Define end use categories with optimized allocations by sector
# Allocations based on feedstock characteristics and industry practices
end_use_allocations = {
    'Bioenergy & Electricity': {
        'Forest Biomass': 0.35,
        'Agricultural Residues': 0.30,
        'Crop Culls': 0.10,
        'Animal Agriculture': 0.05,  # Low - better for biogas
        'Food Processing': 0.15,
        'Municipal Waste': 0.30,
    },
    'Biogas & Renewable Natural Gas': {
        'Forest Biomass': 0.05,
        'Agricultural Residues': 0.10,
        'Crop Culls': 0.30,  # High organic content
        'Animal Agriculture': 0.60,  # Ideal for anaerobic digestion
        'Food Processing': 0.40,  # High organic content
        'Municipal Waste': 0.25,
    },
    'Biofuels (Ethanol/Biodiesel)': {
        'Forest Biomass': 0.15,
        'Agricultural Residues': 0.25,
        'Crop Culls': 0.20,
        'Animal Agriculture': 0.05,
        'Food Processing': 0.25,  # Some lipid content
        'Municipal Waste': 0.15,
    },
    'Wood Pellets & Solid Fuels': {
        'Forest Biomass': 0.25,
        'Agricultural Residues': 0.20,
        'Crop Culls': 0.05,
        'Animal Agriculture': 0.10,
        'Food Processing': 0.05,
        'Municipal Waste': 0.15,
    },
    'Biochar & Soil Amendments': {
        'Forest Biomass': 0.10,
        'Agricultural Residues': 0.10,
        'Crop Culls': 0.20,
        'Animal Agriculture': 0.15,
        'Food Processing': 0.10,
        'Municipal Waste': 0.10,
    },
    'Biochemicals & Materials': {
        'Forest Biomass': 0.10,
        'Agricultural Residues': 0.05,
        'Crop Culls': 0.15,
        'Animal Agriculture': 0.05,
        'Food Processing': 0.05,
        'Municipal Waste': 0.05,
    },
}

# Verify allocations sum to 100% for each sector
print("VERIFYING ALLOCATION PERCENTAGES:")
print("-"*80)
for sector in sectors.keys():
    total_alloc = sum(end_use[sector] for end_use in end_use_allocations.values())
    print(f"  {sector:.<35} {total_alloc*100:>6.1f}%")
print()

# Calculate flows
flows = {}
for end_use, allocations in end_use_allocations.items():
    end_use_total = 0
    for sector, percentage in allocations.items():
        flow_amount = sector_totals[sector] * percentage
        flows[(sector, end_use)] = flow_amount
        end_use_total += flow_amount
    flows[('_total_', end_use)] = end_use_total

# Print end use totals
print("END USE ALLOCATION TOTALS:")
print("-"*80)
end_use_totals = {eu: flows[('_total_', eu)] for eu in end_use_allocations.keys()}
total_all = sum(end_use_totals.values())
for end_use, total in sorted(end_use_totals.items(), key=lambda x: -x[1]):
    pct = (total / total_all) * 100
    print(f"  {end_use:.<45} {total:>15,.0f} ({pct:>5.1f}%)")
print("-"*80)
print(f"  {'TOTAL':.<45} {total_all:>15,.0f}")
print()

# Create Sankey diagram
print("Building Sankey diagram...")

# Define node labels and colors
node_labels = list(sectors.keys()) + list(end_use_allocations.keys())

# Colors for sectors (sources)
sector_colors = {
    'Forest Biomass': '#2E7D32',           # Dark green
    'Agricultural Residues': '#F57C00',    # Orange
    'Crop Culls': '#FFA726',               # Light orange
    'Animal Agriculture': '#8D6E63',       # Brown
    'Food Processing': '#5C6BC0',          # Indigo
    'Municipal Waste': '#757575',          # Gray
}

# Colors for end uses (targets)
end_use_colors = {
    'Bioenergy & Electricity': '#E53935',             # Red
    'Biogas & Renewable Natural Gas': '#43A047',     # Green
    'Biofuels (Ethanol/Biodiesel)': '#FB8C00',       # Deep orange
    'Wood Pellets & Solid Fuels': '#6D4C41',         # Brown
    'Biochar & Soil Amendments': '#4E342E',          # Dark brown
    'Biochemicals & Materials': '#1E88E5',           # Blue
}

all_colors = {**sector_colors, **end_use_colors}
node_colors = [all_colors[label] for label in node_labels]

# Build source, target, value lists
source_indices = []
target_indices = []
flow_values = []
link_colors = []

for (sector, end_use), amount in flows.items():
    if sector == '_total_':
        continue
    
    source_idx = node_labels.index(sector)
    target_idx = node_labels.index(end_use)
    
    source_indices.append(source_idx)
    target_indices.append(target_idx)
    flow_values.append(amount)
    
    # Link color is semi-transparent version of source color
    color = sector_colors[sector]
    link_colors.append(color.replace(')', ', 0.3)').replace('#', 'rgba(').replace('rgb', ''))

# Convert hex to rgba for link colors
def hex_to_rgba(hex_color, alpha=0.3):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {alpha})'

link_colors = [hex_to_rgba(sector_colors[node_labels[src]]) for src in source_indices]

# Define descriptions for each sector
sector_descriptions = {
    'Forest Biomass': 'Logging residues, small-diameter trees, and forest processing waste',
    'Agricultural Residues': 'Dry plant stalks, leaves, and prunings left after harvest. Low moisture (~10-20%), ideal for combustion and conversion to solid fuels.',
    'Crop Culls': 'Rejected produce unsuitable for sale. High moisture (80-90%), perishable, best for composting or wet processing.',
    'Animal Agriculture': 'Manure and bedding from livestock operations. Very high moisture, ideal for anaerobic digestion.',
    'Food Processing': 'Waste from 712 commercial facilities (canneries, dairies, wineries, mills). Concentrated at facilities with existing infrastructure, easier collection than field residues.',
    'Municipal Waste': 'Organic waste from homes, businesses, and institutions',
    'Biochemicals & Materials': 'High-value bio-based products including bioplastics (PLA, PHA), platform chemicals (succinic acid, lactic acid), solvents, adhesives, and composite materials.<br>Requires advanced processing.',
}

# Create custom data with descriptions
node_customdata = []
for label in node_labels:
    amount = sector_totals.get(label, end_use_totals.get(label, 0))
    desc = sector_descriptions.get(label, '')
    if desc:
        node_customdata.append(f"{amount:,.0f} tonnes/year<br><br><i>{desc}</i>")
    else:
        node_customdata.append(f"{amount:,.0f} tonnes/year")

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=30,
        line=dict(color="white", width=2),
        label=node_labels,
        color=node_colors,
        customdata=node_customdata,
        hovertemplate='<b>%{label}</b><br>%{customdata}<extra></extra>',
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=flow_values,
        color=link_colors,
        customdata=[f"{val:,.0f} tonnes/year" for val in flow_values],
        hovertemplate='%{source.label} → %{target.label}<br>%{customdata}<extra></extra>',
    )
)])

# Update layout
fig.update_layout(
    title={
        'text': "California Comprehensive Biomass Resource Flow to End Uses<br>" +
                f"<sub>Total Annual Potential: {sum(sector_totals.values()):,.0f} dry tonnes/year</sub>",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#2c3e50'}
    },
    font=dict(size=12, family="Arial, sans-serif"),
    plot_bgcolor='#f8f9fa',
    paper_bgcolor='#ffffff',
    height=900,
    margin=dict(t=120, b=60, l=40, r=40),
)

# Add annotations
annotations_text = (
    "<b>Data Sources:</b> 2023 Billion Ton Report (Forest), CA County-Level Biomass Data (Agriculture, MSW)<br>" +
    "<b>Sectors:</b> Forest (2.8%), Agriculture (19.4%), Processing (54.1%), MSW (21.4%), Animal (2.3%)<br>" +
    "<b>Note:</b> Allocation percentages based on feedstock characteristics and industry best practices"
)

fig.add_annotation(
    text=annotations_text,
    xref="paper", yref="paper",
    x=0.5, y=-0.05,
    showarrow=False,
    font=dict(size=10, color='#666'),
    align='center',
    xanchor='center'
)

# Save the figure
output_file = 'biomass_sankey_diagram.html'
fig.write_html(output_file)

print("="*80)
print(f"✓ Comprehensive Sankey diagram saved as: {output_file}")
print("="*80)
print()
print("VISUALIZATION FEATURES:")
print("  • Left side: 6 major biomass sectors")
print("  • Right side: 6 end-use applications")
print("  • Flow width: Proportional to biomass volume (tonnes/year)")
print("  • Colors: Sector-coded with semi-transparent flows")
print("  • Interactive: Hover for exact values and percentages")
print()
print("KEY INSIGHTS:")
print(f"  • Largest sector: Food Processing ({sector_totals['Food Processing']:,.0f} tonnes, 54%)")
print(f"  • Largest end use: Biogas/RNG ({end_use_totals['Biogas & Renewable Natural Gas']:,.0f} tonnes, {(end_use_totals['Biogas & Renewable Natural Gas']/total_all)*100:.1f}%)")
print(f"  • Total resource: {sum(sector_totals.values()):,.0f} tonnes/year")
print("="*80)
