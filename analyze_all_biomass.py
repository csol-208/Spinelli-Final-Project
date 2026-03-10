#!/usr/bin/env python3
"""
Comprehensive California Biomass Resource Analysis
Analyzes all biomass datasets to calculate total potential across all sectors
"""

import pandas as pd
import os
import re

def clean_numeric(value):
    """Clean numeric values from formatted strings"""
    if pd.isna(value) or value in ['-', '(D)', '', ' ']:
        return 0
    if isinstance(value, str):
        # Remove quotes, spaces, commas
        value = value.strip().strip('"').replace(',', '').replace(' ', '')
        if value in ['-', '(D)', '']:
            return 0
        try:
            return float(value)
        except:
            return 0
    return float(value)

def analyze_county_file(filepath, skip_first_col=True, total_col_only=False):
    """Analyze a county-level gross file and return total"""
    try:
        df = pd.read_csv(filepath)
        
        # For processing files, just use the TOTAL column (second column)
        if total_col_only and len(df.columns) > 1:
            # Get the total from the "Total" row (second to last row)
            total_value = clean_numeric(df.iloc[-2, 1])  # Total row, second column
            return total_value
        
        # For other files, skip the first column (usually COUNTY) and sum all numeric data
        total = 0
        for col in df.columns[1 if skip_first_col else 0:]:
            if 'Unnamed' not in col and col not in ['Scenario', 'NULL']:
                total += df[col].apply(clean_numeric).sum()
        return total
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return 0

def main():
    print("="*80)
    print("CALIFORNIA COMPREHENSIVE BIOMASS RESOURCE ANALYSIS")
    print("="*80)
    print()
    
    # Dictionary to store results
    results = {}
    
    # 1. FOREST BIOMASS (from existing analysis)
    print("1. FOREST BIOMASS RESOURCES")
    print("-"*80)
    forest_files = {
        'Forest Processing Waste': 'data/CA_forest_processing_waste_points_BillionTonReport.csv',
        'Logging Residues': 'data/CA_logging_residues_points_BillionTonReport.csv',
        'Other Forest Waste': 'data/CA_other_forest_waste_points_BillionTonReport.csv',
        'Small-Diameter Trees': 'data/CA_small-diameter_trees_points_BillionTonReport.csv'
    }
    
    forest_total = 0
    for name, filepath in forest_files.items():
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            total = df['resource_amount'].sum()
            forest_total += total
            results[name] = total
            print(f"  {name:.<40} {total:>15,.0f} dry tonnes/year")
    
    results['FOREST TOTAL'] = forest_total
    print(f"  {'SUBTOTAL - FOREST':.<40} {forest_total:>15,.0f} dry tonnes/year")
    print()
    
    # 2. ANIMAL AGRICULTURE
    print("2. ANIMAL AGRICULTURE RESOURCES")
    print("-"*80)
    
    # Manure (wet tonnes - note this needs moisture conversion)
    if os.path.exists('data/CA_grossmanure.csv'):
        df = pd.read_csv('data/CA_grossmanure.csv')
        # Get the total row (last row)
        total_manure = clean_numeric(df.iloc[-1, 1])  # Second column is TOTAL MANURE
        results['Animal Manure (wet)'] = total_manure
        print(f"  {'Animal Manure (WET tonnes)':.<40} {total_manure:>15,.0f} wet tonnes/year")
        print(f"  {'  → Dry matter equivalent (~20%)':.<40} {total_manure*0.2:>15,.0f} dry tonnes/year")
    
    # Bedding
    if os.path.exists('data/CA_grossbedding.csv'):
        total_bedding = analyze_county_file('data/CA_grossbedding.csv')
        results['Animal Bedding'] = total_bedding
        print(f"  {'Animal Bedding':.<40} {total_bedding:>15,.0f} dry tonnes/year")
    
    animal_total_dry = (total_manure * 0.2) + total_bedding  # Convert manure to dry basis
    results['ANIMAL TOTAL (dry)'] = animal_total_dry
    print(f"  {'SUBTOTAL - ANIMAL (dry basis)':.<40} {animal_total_dry:>15,.0f} dry tonnes/year")
    print()
    
    # 3. AGRICULTURAL RESIDUES (2020 scenario)
    print("3. AGRICULTURAL CROP RESIDUES (2020 Projection)")
    print("-"*80)
    
    ag_files = {
        'Field Residues': 'data/CA_grossfieldres20.csv',
        'Orchard Residues': 'data/CA_grossorchres20.csv',
        'Row Crop Residues': 'data/CA_grossrowres20.csv',
        'Orchard Culls': 'data/CA_grossorchcull20.csv',
        'Row Crop Culls': 'data/CA_grossrowculls20.csv',
    }
    
    ag_total = 0
    for name, filepath in ag_files.items():
        if os.path.exists(filepath):
            total = analyze_county_file(filepath)
            ag_total += total
            results[name] = total
            print(f"  {name:.<40} {total:>15,.0f} dry tonnes/year")
    
    results['CROP RESIDUES TOTAL'] = ag_total
    print(f"  {'SUBTOTAL - CROP RESIDUES':.<40} {ag_total:>15,.0f} dry tonnes/year")
    print()
    
    # 4. PROCESSING RESIDUES (2014 baseline)
    print("4. FOOD PROCESSING RESIDUES (2014 Baseline)")
    print("-"*80)
    
    proc_files = {
        'High Moisture Solids': 'data/CA_grossprocHMS14.csv',
        'Low Moisture Solids': 'data/CA_grossprocLMS14.csv',
        'Processing MSW': 'data/CA_grossprocMSW14.csv',
    }
    
    proc_total = 0
    for name, filepath in proc_files.items():
        if os.path.exists(filepath):
            total = analyze_county_file(filepath, total_col_only=True)
            proc_total += total
            results[name] = total
            print(f"  {name:.<40} {total:>15,.0f} dry tonnes/year")
    
    # Add olive/stone fruit pits
    if os.path.exists('data/CA_olivestonefruitpits.csv'):
        total_pits = analyze_county_file('data/CA_olivestonefruitpits.csv')
        proc_total += total_pits
        results['Olive & Stone Fruit Pits'] = total_pits
        print(f"  {'Olive & Stone Fruit Pits':.<40} {total_pits:>15,.0f} dry tonnes/year")
    
    results['PROCESSING TOTAL'] = proc_total
    print(f"  {'SUBTOTAL - PROCESSING':.<40} {proc_total:>15,.0f} dry tonnes/year")
    print()
    
    # 5. MUNICIPAL SOLID WASTE (2020 baseline scenario)
    print("5. MUNICIPAL SOLID WASTE - Organic Fraction (2020 Baseline)")
    print("-"*80)
    
    if os.path.exists('data/CA_grossMSW20.csv'):
        df = pd.read_csv('data/CA_grossMSW20.csv', skiprows=[0])  # Skip first row with scenario labels
        msw_categories = {}
        
        # Process each pair of columns (Baseline, High Recycle)
        for i in range(1, len(df.columns), 2):
            category = df.columns[i]
            if 'Unnamed' not in category:
                baseline_total = df[df.columns[i]].apply(clean_numeric).sum()
                msw_categories[category] = baseline_total
                results[f'MSW - {category}'] = baseline_total
                print(f"  {category:.<40} {baseline_total:>15,.0f} tonnes/year")
        
        msw_total = sum(msw_categories.values())
        results['MSW TOTAL'] = msw_total
        print(f"  {'SUBTOTAL - MSW':.<40} {msw_total:>15,.0f} tonnes/year")
    print()
    
    # 6. INFRASTRUCTURE SUMMARY
    print("6. EXISTING BIOMASS INFRASTRUCTURE")
    print("-"*80)
    
    infra_files = {
        'Processing Facilities': 'data/CA_proc_points.csv',
        'Distributed Energy Systems': 'data/CA_des_points.csv',
        'Combined Heat & Power': 'data/CA_comb_points.csv',
        'Waste-to-Energy': 'data/CA_wte_points.csv'
    }
    
    for name, filepath in infra_files.items():
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            count = len(df)
            results[f'{name} (count)'] = count
            print(f"  {name:.<40} {count:>15} facilities")
    print()
    
    # GRAND TOTAL
    print("="*80)
    print("TOTAL CALIFORNIA BIOMASS RESOURCE POTENTIAL")
    print("="*80)
    
    grand_total = forest_total + animal_total_dry + ag_total + proc_total + msw_total
    
    print(f"\n  Forest Biomass:                          {forest_total:>15,.0f} dry tonnes/year")
    print(f"  Animal Agriculture (dry basis):          {animal_total_dry:>15,.0f} dry tonnes/year")
    print(f"  Crop Residues:                           {ag_total:>15,.0f} dry tonnes/year")
    print(f"  Processing Residues:                     {proc_total:>15,.0f} dry tonnes/year")
    print(f"  Municipal Solid Waste (organic):         {msw_total:>15,.0f} tonnes/year")
    print(f"  {'-'*60}")
    print(f"  GRAND TOTAL:                             {grand_total:>15,.0f} dry tonnes/year")
    print()
    
    # Percentage breakdown
    print("SECTOR BREAKDOWN (% of total):")
    print(f"  Forest:                                  {(forest_total/grand_total)*100:>14.1f}%")
    print(f"  Animal Agriculture:                      {(animal_total_dry/grand_total)*100:>14.1f}%")
    print(f"  Crop Residues:                           {(ag_total/grand_total)*100:>14.1f}%")
    print(f"  Processing:                              {(proc_total/grand_total)*100:>14.1f}%")
    print(f"  MSW:                                     {(msw_total/grand_total)*100:>14.1f}%")
    print()
    
    print("="*80)
    print("NOTES:")
    print("  • Manure converted from wet to dry basis (20% dry matter)")
    print("  • MSW uses 2020 baseline scenario (pre-high-recycle)")
    print("  • Processing residues from 2014 baseline year")
    print("  • Crop residues from 2020 projections")
    print("  • Not all biomass is technically or economically collectible")
    print("  • Some resources have competing uses (soil amendment, animal feed)")
    print("="*80)
    
    # Save results to CSV
    results_df = pd.DataFrame(list(results.items()), columns=['Category', 'Amount'])
    results_df.to_csv('california_biomass_summary.csv', index=False)
    print("\n✓ Results saved to: california_biomass_summary.csv")

if __name__ == '__main__':
    main()
