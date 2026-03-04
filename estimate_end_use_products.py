#!/usr/bin/env python3
"""
California Biomass End-Use Product Potential Estimator
Estimates potential products from biomass feedstocks using industry conversion factors
"""

import pandas as pd
import os

# Industry-standard conversion factors (from literature and industry data)
CONVERSION_FACTORS = {
    # ELECTRICITY GENERATION (Direct combustion)
    'electricity_kwh_per_tonne': {
        'woody': 2000,      # 2 MWh per dry tonne woody biomass
        'herbaceous': 1800,  # Slightly lower for ag residues
        'msw': 1500,        # Lower heating value
        'wet_organic': 500,  # After drying
    },
    
    # BIOGAS (Anaerobic Digestion) - cubic meters CH4 per tonne
    'biogas_m3_ch4_per_tonne': {
        'manure': 25,        # 25 m3 CH4 per tonne (dry basis)
        'food_waste': 100,   # High biogas potential
        'green_waste': 60,   # Moderate potential
        'processing_waste': 80,  # Varies by type
    },
    
    # BIOFUELS (Cellulosic ethanol) - gallons per dry tonne
    'ethanol_gallons_per_tonne': {
        'woody': 75,         # ~75 gallons/tonne cellulosic ethanol
        'herbaceous': 85,    # Agricultural residues slightly higher
        'msw': 60,          # Lower due to contamination
    },
    
    # BIODIESEL/RENEWABLE DIESEL (from lipids/oils)
    'diesel_gallons_per_tonne': {
        'fog': 250,          # Fats, oils, grease - high yield
        'food_processing': 50,  # Some lipid content
    },
    
    # HEAT (Thermal energy) - MMBtu per tonne
    'heat_mmbtu_per_tonne': {
        'woody': 16,         # ~16 MMBtu/dry tonne
        'herbaceous': 14,    # Slightly lower
        'msw': 12,
        'processing': 10,
    },
    
    # BIOCHAR (Pyrolysis) - tonnes biochar per tonne feedstock
    'biochar_yield': {
        'woody': 0.25,       # 25% mass yield
        'herbaceous': 0.20,  # 20% yield
    },
    
    # COMPOST - tonnes compost per tonne feedstock
    'compost_yield': {
        'green_waste': 0.50,  # 50% volume reduction
        'food_waste': 0.40,
        'manure': 0.60,
    },
    
    # WOOD PELLETS - tonnes pellets per tonne feedstock
    'pellet_yield': {
        'woody': 0.90,       # 90% (minimal processing loss)
        'herbaceous': 0.85,
    },
    
    # BIOCHEMICALS (High-value products) - $ value per tonne
    'biochemical_value_per_tonne': {
        'lignin': 500,       # Lignin extraction
        'cellulose': 300,    # Cellulosic products
        'specialty': 1000,   # Specialty chemicals
    }
}

def calculate_products(feedstock_name, amount_tonnes, feedstock_type):
    """Calculate potential products from a feedstock"""
    results = {}
    
    # Electricity
    if feedstock_type in ['woody', 'herbaceous', 'msw', 'wet_organic']:
        kwh = amount_tonnes * CONVERSION_FACTORS['electricity_kwh_per_tonne'].get(feedstock_type, 1500)
        mwh = kwh / 1000
        results['Electricity (MWh)'] = mwh
        results['Homes Powered (annual)'] = mwh / 10000  # Average home uses 10 MWh/year
    
    # Biogas
    if feedstock_type in ['manure', 'food_waste', 'green_waste', 'processing_waste']:
        ch4_m3 = amount_tonnes * CONVERSION_FACTORS['biogas_m3_ch4_per_tonne'].get(feedstock_type, 50)
        # 1 m3 CH4 = 35.8 MJ = 9.94 kWh
        biogas_kwh = ch4_m3 * 9.94
        biogas_mwh = biogas_kwh / 1000
        results['Biogas Electricity (MWh)'] = biogas_mwh
        results['Biogas (million m3 CH4)'] = ch4_m3 / 1_000_000
    
    # Ethanol
    if feedstock_type in ['woody', 'herbaceous', 'msw']:
        gallons = amount_tonnes * CONVERSION_FACTORS['ethanol_gallons_per_tonne'].get(feedstock_type, 70)
        results['Cellulosic Ethanol (million gal)'] = gallons / 1_000_000
    
    # Biodiesel
    if feedstock_type in ['fog', 'food_processing']:
        gallons = amount_tonnes * CONVERSION_FACTORS['diesel_gallons_per_tonne'].get(feedstock_type, 100)
        results['Biodiesel (million gal)'] = gallons / 1_000_000
    
    # Heat
    if feedstock_type in ['woody', 'herbaceous', 'msw', 'processing']:
        mmbtu = amount_tonnes * CONVERSION_FACTORS['heat_mmbtu_per_tonne'].get(feedstock_type, 12)
        results['Thermal Energy (trillion BTU)'] = mmbtu / 1_000_000
    
    # Biochar
    if feedstock_type in ['woody', 'herbaceous']:
        biochar = amount_tonnes * CONVERSION_FACTORS['biochar_yield'].get(feedstock_type, 0.20)
        results['Biochar (tonnes)'] = biochar
    
    # Compost
    if feedstock_type in ['green_waste', 'food_waste', 'manure']:
        compost = amount_tonnes * CONVERSION_FACTORS['compost_yield'].get(feedstock_type, 0.50)
        results['Compost (tonnes)'] = compost
    
    # Wood Pellets
    if feedstock_type in ['woody', 'herbaceous']:
        pellets = amount_tonnes * CONVERSION_FACTORS['pellet_yield'].get(feedstock_type, 0.85)
        results['Wood Pellets (tonnes)'] = pellets
    
    return results

def main():
    print("="*90)
    print("CALIFORNIA BIOMASS END-USE PRODUCT POTENTIAL ANALYSIS")
    print("="*90)
    print()
    print("This analysis estimates potential products from California's biomass resources")
    print("using industry-standard conversion factors and existing feedstock quantities.")
    print()
    
    # Define feedstock categories and their types for conversion
    feedstock_data = {
        # Forest Biomass - Woody
        'Forest Processing Waste': {'amount': 23_295, 'type': 'woody'},
        'Logging Residues': {'amount': 2_760_264, 'type': 'woody'},
        'Other Forest Waste': {'amount': 231_199, 'type': 'woody'},
        'Small-Diameter Trees': {'amount': 677_269, 'type': 'woody'},
        
        # Animal Agriculture
        'Animal Manure (dry)': {'amount': 2_195_237, 'type': 'manure'},
        'Animal Bedding': {'amount': 932_661, 'type': 'woody'},  # Straw/wood shavings
        
        # Agricultural Residues - Herbaceous
        'Field Residues': {'amount': 7_390_666, 'type': 'herbaceous'},
        'Orchard Residues': {'amount': 14_701_977, 'type': 'woody'},  # Woody prunings
        'Row Crop Residues': {'amount': 1_310_969, 'type': 'herbaceous'},
        'Orchard Culls': {'amount': 658_525, 'type': 'food_waste'},
        'Row Crop Culls': {'amount': 1_979_711, 'type': 'food_waste'},
        
        # Processing Residues
        'High Moisture Solids': {'amount': 3_236_391, 'type': 'processing_waste'},
        'Low Moisture Solids': {'amount': 14_869_013, 'type': 'processing'},
        'Processing MSW': {'amount': 54_239_694, 'type': 'food_processing'},
        'Olive & Fruit Pits': {'amount': 108_740, 'type': 'woody'},
        
        # Municipal Solid Waste (simplified - treating as mixed organic)
        'MSW Organic Fraction': {'amount': 28_702_694, 'type': 'msw'},
    }
    
    # Calculate products for each feedstock
    all_products = {}
    
    print("-"*90)
    print("PRODUCT ESTIMATES BY FEEDSTOCK CATEGORY")
    print("-"*90)
    print()
    
    for feedstock, data in feedstock_data.items():
        amount = data['amount']
        ftype = data['type']
        
        print(f"{feedstock} ({amount:,.0f} tonnes/year, type: {ftype})")
        
        products = calculate_products(feedstock, amount, ftype)
        
        for product, value in products.items():
            print(f"  → {product:.<50} {value:>15,.0f}")
            
            # Accumulate totals
            if product not in all_products:
                all_products[product] = 0
            all_products[product] += value
        
        print()
    
    # Print totals
    print("="*90)
    print("TOTAL CALIFORNIA BIOMASS PRODUCT POTENTIAL (ANNUAL)")
    print("="*90)
    print()
    
    # Organize by product category
    print("ENERGY PRODUCTS:")
    print("-"*90)
    
    energy_products = {k: v for k, v in all_products.items() if 'Electricity' in k or 'MWh' in k}
    for product, value in energy_products.items():
        print(f"  {product:.<70} {value:>15,.0f}")
    
    if 'Homes Powered (annual)' in all_products:
        print(f"\n  {'Equivalent Homes Powered':.<70} {all_products['Homes Powered (annual)']:>15,.0f}")
    
    print()
    print("TRANSPORTATION FUELS:")
    print("-"*90)
    
    fuel_products = {k: v for k, v in all_products.items() if 'Ethanol' in k or 'Biodiesel' in k}
    for product, value in fuel_products.items():
        print(f"  {product:.<70} {value:>15,.0f}")
    
    # Add vehicle equivalents
    if 'Cellulosic Ethanol (million gal)' in all_products:
        ethanol_gal = all_products['Cellulosic Ethanol (million gal)'] * 1_000_000
        vehicles = ethanol_gal / 500  # Average car uses 500 gal/year
        print(f"  {'→ Vehicles Fueled (annual, cars)':.<70} {vehicles:>15,.0f}")
    
    print()
    print("THERMAL ENERGY:")
    print("-"*90)
    
    heat_products = {k: v for k, v in all_products.items() if 'Thermal' in k or 'BTU' in k}
    for product, value in heat_products.items():
        print(f"  {product:.<70} {value:>15,.2f}")
    
    print()
    print("BIOGAS:")
    print("-"*90)
    
    biogas_products = {k: v for k, v in all_products.items() if 'Biogas' in k}
    for product, value in biogas_products.items():
        print(f"  {product:.<70} {value:>15,.2f}")
    
    print()
    print("SOLID PRODUCTS:")
    print("-"*90)
    
    solid_products = {k: v for k, v in all_products.items() if any(x in k for x in ['Biochar', 'Compost', 'Pellets'])}
    for product, value in solid_products.items():
        print(f"  {product:.<70} {value:>15,.0f}")
    
    print()
    print("="*90)
    print("FACILITY CAPACITY REQUIREMENTS")
    print("="*90)
    print()
    
    # Estimate facility needs
    if 'Cellulosic Ethanol (million gal)' in all_products:
        ethanol = all_products['Cellulosic Ethanol (million gal)']
        # Typical cellulosic ethanol plant: 25-30 million gal/year capacity
        plants_needed = ethanol / 25
        print(f"  Cellulosic Ethanol Refineries (25M gal/yr each):           {plants_needed:>10.1f} facilities")
    
    if 'Biogas Electricity (MWh)' in all_products:
        biogas_mwh = all_products['Biogas Electricity (MWh)']
        # Typical AD facility: 1 MW capacity = 8,760 MWh/year
        ad_plants = biogas_mwh / 8760
        print(f"  Anaerobic Digestion Plants (1 MW each):                    {ad_plants:>10.1f} facilities")
    
    if 'Electricity (MWh)' in all_products:
        elec_mwh = all_products['Electricity (MWh)']
        # Typical biomass power plant: 20-50 MW
        # At 20 MW = 175,200 MWh/year
        power_plants = elec_mwh / 175_200
        print(f"  Biomass Power Plants (20 MW each):                         {power_plants:>10.1f} facilities")
    
    if 'Biochar (tonnes)' in all_products:
        biochar = all_products['Biochar (tonnes)']
        # Typical pyrolysis plant: 10,000 tonnes/year
        biochar_plants = biochar / 10_000
        print(f"  Biochar Production Facilities (10k tonnes/yr):             {biochar_plants:>10.1f} facilities")
    
    if 'Wood Pellets (tonnes)' in all_products:
        pellets = all_products['Wood Pellets (tonnes)']
        # Typical pellet plant: 100,000 tonnes/year
        pellet_plants = pellets / 100_000
        print(f"  Wood Pellet Mills (100k tonnes/yr):                        {pellet_plants:>10.1f} facilities")
    
    print()
    print("="*90)
    print("ECONOMIC & ENVIRONMENTAL IMPACT ESTIMATES")
    print("="*90)
    print()
    
    # Economic value estimates ($/unit, 2024 prices)
    revenue = 0
    
    if 'Electricity (MWh)' in all_products:
        elec_revenue = all_products['Electricity (MWh)'] * 80  # $80/MWh average
        revenue += elec_revenue
        print(f"  Electricity Revenue ($80/MWh):                         ${elec_revenue/1_000_000:>12,.0f} million")
    
    if 'Cellulosic Ethanol (million gal)' in all_products:
        ethanol_revenue = all_products['Cellulosic Ethanol (million gal)'] * 2.50 * 1_000_000  # $2.50/gal
        revenue += ethanol_revenue
        print(f"  Ethanol Revenue ($2.50/gal):                           ${ethanol_revenue/1_000_000:>12,.0f} million")
    
    if 'Biochar (tonnes)' in all_products:
        biochar_revenue = all_products['Biochar (tonnes)'] * 500  # $500/tonne
        revenue += biochar_revenue
        print(f"  Biochar Revenue ($500/tonne):                          ${biochar_revenue/1_000_000:>12,.0f} million")
    
    if 'Wood Pellets (tonnes)' in all_products:
        pellet_revenue = all_products['Wood Pellets (tonnes)'] * 150  # $150/tonne
        revenue += pellet_revenue
        print(f"  Wood Pellet Revenue ($150/tonne):                      ${pellet_revenue/1_000_000:>12,.0f} million")
    
    print(f"\n  {'TOTAL ESTIMATED ANNUAL REVENUE':.<50} ${revenue/1_000_000:>12,.0f} million")
    
    # Environmental impacts
    print()
    print("  ENVIRONMENTAL BENEFITS:")
    
    # GHG reductions (rough estimates)
    # Biomass vs fossil fuel: ~0.5-1.0 tonnes CO2e avoided per tonne biomass
    total_biomass = sum(data['amount'] for data in feedstock_data.values())
    ghg_avoided = total_biomass * 0.75  # Conservative 0.75 tonnes CO2e per tonne biomass
    print(f"    GHG Emissions Avoided:                               {ghg_avoided/1_000_000:>12,.1f} million tonnes CO2e")
    print(f"    Equivalent Cars Removed:                             {ghg_avoided/4.6:>12,.0f} vehicles")
    
    # Waste diverted
    print(f"    Waste Diverted from Landfills:                       {total_biomass/1_000_000:>12,.1f} million tonnes")
    
    # Jobs (rough estimate: 1 job per 1,000 tonnes processed)
    jobs = total_biomass / 1_000
    print(f"    Green Jobs Created (direct):                         {jobs:>12,.0f} jobs")
    
    print()
    print("="*90)
    print("NOTES & ASSUMPTIONS:")
    print("="*90)
    print("""
  • Conversion factors based on industry averages and may vary by technology
  • Assumes optimal processing conditions and technology maturity
  • Not all biomass is technically or economically collectible
  • Multiple products can be co-produced from same feedstock (biorefinery approach)
  • Economic values based on 2024 market prices and may fluctuate
  • Facility counts assume full-scale commercial operations
  • Environmental benefits assume biomass replaces fossil fuels
  • Actual implementation requires infrastructure investment, policy support
  • Geographic distribution and logistics not considered in these totals
  • Some feedstocks have competing uses (animal feed, soil amendment)
    """)
    
    print("="*90)
    
    # Save detailed results
    results_df = pd.DataFrame([
        {'Product': k, 'Annual Production': v} 
        for k, v in sorted(all_products.items())
    ])
    results_df.to_csv('biomass_product_estimates.csv', index=False)
    print("\n✓ Detailed results saved to: biomass_product_estimates.csv")

if __name__ == '__main__':
    main()
