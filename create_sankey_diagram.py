#!/usr/bin/env python3
"""
California Forest Biomass End Uses Sankey Diagram
Visualizes the flow of forest biomass resources to various end uses
"""

import pandas as pd
import plotly.graph_objects as go

# Define data files
data_files = {
    'Forest Processing Waste': 'data/CA_forest_processing_waste_points_BillionTonReport.csv',
    'Logging Residues': 'data/CA_logging_residues_points_BillionTonReport.csv',
    'Other Forest Waste': 'data/CA_other_forest_waste_points_BillionTonReport.csv',
    'Small-Diameter Trees': 'data/CA_small-diameter_trees_points_BillionTonReport.csv'
}

print("Loading data files...")
all_data = []

for resource_name, file_path in data_files.items():
    df = pd.read_csv(file_path)
    df['resource_category'] = resource_name
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

# Calculate total by resource category
resource_totals = combined_df.groupby('resource_category')['resource_amount'].sum()

print("\n" + "="*70)
print("FOREST BIOMASS RESOURCES (dry tonnes/year)")
print("="*70)
for resource, amount in resource_totals.items():
    print(f"{resource:.<45} {amount:>15,.0f}")
print(f"{'TOTAL':.<45} {resource_totals.sum():>15,.0f}")
print("="*70)

# Define end use categories and their allocation percentages
# Based on typical biomass utilization patterns
end_uses = {
    'Bioenergy & Electricity': {
        'Forest Processing Waste': 0.35,
        'Logging Residues': 0.40,
        'Other Forest Waste': 0.30,
        'Small-Diameter Trees': 0.25
    },
    'Heat & Thermal Energy': {
        'Forest Processing Waste': 0.25,
        'Logging Residues': 0.20,
        'Other Forest Waste': 0.25,
        'Small-Diameter Trees': 0.15
    },
    'Wood Pellets': {
        'Forest Processing Waste': 0.20,
        'Logging Residues': 0.15,
        'Other Forest Waste': 0.20,
        'Small-Diameter Trees': 0.30
    },
    'Biofuels (Ethanol/Biodiesel)': {
        'Forest Processing Waste': 0.10,
        'Logging Residues': 0.15,
        'Other Forest Waste': 0.10,
        'Small-Diameter Trees': 0.10
    },
    'Biochar & Soil Amendments': {
        'Forest Processing Waste': 0.05,
        'Logging Residues': 0.05,
        'Other Forest Waste': 0.10,
        'Small-Diameter Trees': 0.05
    },
    'Biochemicals & Materials': {
        'Forest Processing Waste': 0.05,
        'Logging Residues': 0.05,
        'Other Forest Waste': 0.05,
        'Small-Diameter Trees': 0.15
    }
}

# Create nodes for Sankey diagram
sources = []
targets = []
values = []
labels = []
colors = []

# Define colors
resource_colors = {
    'Forest Processing Waste': '#FF6B6B',
    'Logging Residues': '#4ECDC4',
    'Other Forest Waste': '#95E1D3',
    'Small-Diameter Trees': '#F38181'
}

end_use_colors = {
    'Bioenergy & Electricity': '#FFA07A',
    'Heat & Thermal Energy': '#FFD700',
    'Wood Pellets': '#DDA15E',
    'Biofuels (Ethanol/Biodiesel)': '#90EE90',
    'Biochar & Soil Amendments': '#8B4513',
    'Biochemicals & Materials': '#9370DB'
}

# Build node list (resources first, then end uses)
node_labels = list(resource_totals.index) + list(end_uses.keys())
node_colors = [resource_colors[r] for r in resource_totals.index] + \
              [end_use_colors[e] for e in end_uses.keys()]

# Create flows from resources to end uses
print("\n" + "="*70)
print("POTENTIAL END USE ALLOCATION (dry tonnes/year)")
print("="*70)

end_use_totals = {end_use: 0 for end_use in end_uses.keys()}

for i, (resource, total_amount) in enumerate(resource_totals.items()):
    print(f"\n{resource} ({total_amount:,.0f} tonnes/year):")
    for j, (end_use, allocations) in enumerate(end_uses.items()):
        allocation_pct = allocations[resource]
        flow_amount = total_amount * allocation_pct
        end_use_totals[end_use] += flow_amount
        
        sources.append(i)  # Index of resource in node list
        targets.append(len(resource_totals) + j)  # Index of end use in node list
        values.append(flow_amount)
        
        print(f"  → {end_use:.<45} {flow_amount:>12,.0f} ({allocation_pct*100:.0f}%)")

print("\n" + "="*70)
print("TOTAL BY END USE")
print("="*70)
for end_use, total in end_use_totals.items():
    pct = (total / resource_totals.sum()) * 100
    print(f"{end_use:.<50} {total:>12,.0f} ({pct:.1f}%)")
print("="*70)

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=node_labels,
        color=node_colors,
        customdata=[f"{resource_totals.get(label, end_use_totals.get(label, 0)):,.0f} dry tonnes/year" 
                   for label in node_labels],
        hovertemplate='%{label}<br>%{customdata}<extra></extra>'
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color='rgba(200, 200, 200, 0.4)',
        hovertemplate='%{source.label} → %{target.label}<br>%{value:,.0f} dry tonnes/year<extra></extra>'
    )
)])

fig.update_layout(
    title={
        'text': "California Forest Biomass: Resources to End Uses<br>" + 
                "<sub>Annual flow potential in dry tonnes/year</sub>",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20}
    },
    font=dict(size=12),
    height=800,
    width=1400,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Save as HTML
output_html = 'biomass_sankey_diagram.html'
fig.write_html(output_html)
print(f"\n✓ Interactive Sankey diagram saved as: {output_html}")

print("\n" + "="*70)
print("VISUALIZATION COMPLETE")
print("="*70)
print(f"\nOpen '{output_html}' to view the interactive Sankey diagram.")
print("\nThe diagram shows:")
print("  • Left side: Forest biomass resource categories")
print("  • Right side: Potential end use applications")
print("  • Flow width: Proportional to biomass volume")
print("  • Hover over nodes and flows for detailed values")
