#!/usr/bin/env python3
"""
California Forest Biomass Waste Resource Map
Creates an interactive map visualizing forest waste resources across California
"""

import pandas as pd
import folium
from folium import plugins
import os

# Define data files
data_files = {
    'Forest Processing Waste': 'data/CA_forest_processing_waste_points_BillionTonReport.csv',
    'Logging Residues': 'data/CA_logging_residues_points_BillionTonReport.csv',
    'Other Forest Waste': 'data/CA_other_forest_waste_points_BillionTonReport.csv',
    'Small-Diameter Trees': 'data/CA_small-diameter_trees_points_BillionTonReport.csv'
}

# Define colors for each resource type
colors = {
    'Forest Processing Waste': '#FF6B6B',  # Red
    'Logging Residues': '#4ECDC4',          # Teal
    'Other Forest Waste': '#95E1D3',        # Light green
    'Small-Diameter Trees': '#F38181'       # Pink
}

print("Loading data files...")
all_data = []

for resource_name, file_path in data_files.items():
    df = pd.read_csv(file_path)
    df['resource_category'] = resource_name
    all_data.append(df)
    print(f"  ✓ Loaded {resource_name}: {len(df):,} records")

# Combine all data
combined_df = pd.concat(all_data, ignore_index=True)
print(f"\nTotal records: {len(combined_df):,}")

# Calculate statistics
print("\n" + "="*60)
print("RESOURCE SUMMARY")
print("="*60)
for resource_name in data_files.keys():
    resource_data = combined_df[combined_df['resource_category'] == resource_name]
    total_amount = resource_data['resource_amount'].sum()
    avg_amount = resource_data['resource_amount'].mean()
    print(f"\n{resource_name}:")
    print(f"  Total: {total_amount:,.2f} dry tonnes/year")
    print(f"  Average per point: {avg_amount:.2f} dry tonnes/year")
    print(f"  Number of points: {len(resource_data):,}")

# Create the map centered on California
print("\nCreating interactive map...")
ca_center = [combined_df['latitude'].mean(), combined_df['longitude'].mean()]
m = folium.Map(
    location=ca_center,
    zoom_start=6,
    tiles='OpenStreetMap'
)

# Add title
title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 400px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px;">
    <h4 style="margin-top:0;">California Forest Biomass Waste Resources</h4>
    <p style="margin:0; font-size:11px;">Data from 2023 Billion Ton Report</p>
    </div>
    '''
m.get_root().html.add_child(folium.Element(title_html))

# Create feature groups for each resource type
feature_groups = {}
for resource_name in data_files.keys():
    feature_groups[resource_name] = folium.FeatureGroup(name=resource_name)

# Sample data for visualization (use subset if too many points)
# For large datasets, we'll sample to keep the map responsive
max_points_per_type = 500

print("\nAdding data points to map...")
for resource_name in data_files.keys():
    resource_data = combined_df[combined_df['resource_category'] == resource_name]
    
    # Sample if dataset is too large
    if len(resource_data) > max_points_per_type:
        # Sample the largest amounts to show most significant resources
        resource_data = resource_data.nlargest(max_points_per_type, 'resource_amount')
        print(f"  {resource_name}: Using top {max_points_per_type} largest sources")
    else:
        print(f"  {resource_name}: Using all {len(resource_data)} points")
    
    for idx, row in resource_data.iterrows():
        # Scale marker size based on resource amount (with reasonable bounds)
        radius = min(max(row['resource_amount'] * 0.5, 3), 15)
        
        # Create popup with detailed information
        popup_html = f"""
        <b>{resource_name}</b><br>
        <b>Amount:</b> {row['resource_amount']:.2f} dry tonnes/year<br>
        <b>Resource:</b> {row['resource']}<br>
        <b>County:</b> {row['county_name']}<br>
        <b>Scenario:</b> {row['bt23_scenario']}<br>
        <b>Price:</b> ${row['resource_price']:.2f}/tonne<br>
        <b>Location:</b> ({row['latitude']:.4f}, {row['longitude']:.4f})
        """
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=300),
            color=colors[resource_name],
            fill=True,
            fillColor=colors[resource_name],
            fillOpacity=0.6,
            weight=1
        ).add_to(feature_groups[resource_name])

# Add all feature groups to map
for fg in feature_groups.values():
    fg.add_to(m)

# Add layer control to toggle resource types
folium.LayerControl().add_to(m)

# Add fullscreen option
plugins.Fullscreen().add_to(m)

# Save the map
output_file = 'california_forest_biomass_map.html'
m.save(output_file)

print(f"\n{'='*60}")
print(f"✓ Map created successfully!")
print(f"✓ Saved as: {output_file}")
print(f"{'='*60}")
print(f"\nOpen '{output_file}' in your web browser to view the interactive map.")
print("\nFeatures:")
print("  • Toggle resource types on/off using the layer control")
print("  • Click on markers for detailed information")
print("  • Zoom and pan to explore different regions")
print("  • Marker size represents resource amount")
