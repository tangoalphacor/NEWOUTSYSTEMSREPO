import httpx
import ast
import sys

basic_type = sys.argv[1] if len(sys.argv) > 1 else "P5151E"
url = f"https://preassembly-referencing-api-prod.eu-de-1.icp.infineon.com//simple_search?user=None&Basistypen={basic_type}&modus=hfgst&key=nfh848h_Su843hTfhg_r82z&id=1620496430&PA_number=69000000&loc=All&milestone=0&differ_pa_baunumbers=False"

response = httpx.get(url, verify=False)
raw = response.text
data = ast.literal_eval(raw)
if isinstance(data, str):
    data = ast.literal_eval(data)

attribute_map = {
    "Basic_type": ("Product", "Basic Type"),
    "Process_Group": ("Product", "Product Line"),
    "Division": ("Product", "Division"),
    "Quality_requirement_cat": ("Product", "Q-Status"),
    "Chip_delivery": ("Product", "Chip Delivery"),
    "FE_FAB": ("FrontEnd", "Substrate"),
    "Wafer_Diameter": ("Preassembly general", "Wafer diameter"),
    "Base_material": ("FrontEnd", "Substrate"),
    "BEOL_STACK_thickness": ("Front Side Stack", "FrontSideMetal Stack w/o EPA"),
    "Organic_Pasivation": ("Front Side Stack", "Organic Passivation Material"),
    "Last_metal_with_thickness": ("Front Side Stack", "FrontSideMetal Stack w/o EPA"),
    "Back_side_Metal_stack_with_thickness": ("Back Side Stack", "BackSideMetal Stack w/o Thickness"),
    "Final_thickness_incl_substrate": ("Thinning", "Si thickness incl. BSM/µm"),
    "Final_thickness_incl_substrate_and_imide": ("Thinning", "Thickness incl. Imid and BSM /µm"),
    "Final_thickness_incl_sub_bomel": ("Thinning", "TAIKO Ring height/µm"),
    "Raster_x": ("Preassembly general", "Raster x/mm"),
    "Raster_y": ("Preassembly general", "Raster y/mm"),
    "Area": ("Preassembly general", "Area/mm^2"),
    "Ratio": ("Preassembly general", "Ratio"),
    "imide_opening": ("Front Side Stack", "Passivation stack w/ EPA"),
    "Scribeline_width_AX_AY": ("Preassembly general", "Street saw width"),
    "Eless_in_Scribeline": ("Back Side Stack", "EPA"),
    "PCM_in_scribeline": ("Other", "Route max"),
    "Balls_Bumps_Pillars_with_height": ("BackEnd", "Package"),
    "DAF": ("BackEnd", "Segment"),
    "Volume_Experience": ("Product", "Product Family"),
    "Preassembly_Yeild": ("Product", "Product and Process Conformity"),
    "Focus_Team_Due_to_Preassembly": ("Preassembly general", "Preassembly site"),
    "Process_block_colour": ("Other", "mounting_orientation"),
}

# All requested fields
all_fields = [
    "PROCESS_GROUP", "DIVISION", "QUALITY_REQUIREMENT_CAT", "CHIP_DELIVERY", "WAFER_DIAMETER", "BEOL_STACK_THICKNESS", "ORGANIC_PASIVATION", "BACK_SIDE_METAL_STACK_WITH_THICKNESS", "FINAL_THICKNESS_INCL_SUBSTRATE", "FINAL_THICKNESS_INCL_SUBSTRATE_AND_IMIDE", "RASTER_X", "RASTER_Y", "AREA", "RATIO", "BASICTYPE_NAME", "REFRENCE_1", "REFRENCE_2", "NEW_BASICTYPE", "ASSESSSMENT", "DATA_SOURCE_DRS_API", "FRONTEND", "FE_FAB", "BASE_MATERIAL", "LAYOUT/DIE", "IMIDE_OPENING", "SCRIBELINE_WIDTH_AX_AY", "ELESS_IN_SCRIBELINE", "PCM_IN_SCRIBELINE", "BALLS_BUMPS_PILLARS_WITH_HEIGHT", "DAF", "QUALITY", "VOLUME_EXPERIENCE", "PREASSEMBLY_YEILD", "FOCUS_TEAM_DUE_TO_PREASSEMBLY", "TECHNICAL_PROCESS_CHAIN", "PROCESS_BLOCK_COLOUR"
]

# Mapped fields
attribute_map.update({
    "PROCESS_GROUP": ("Product", "Product Line"),
    "DIVISION": ("Product", "Division"),
    "QUALITY_REQUIREMENT_CAT": ("Product", "Product and Process Conformity"),
    "CHIP_DELIVERY": ("Product", "Chip Delivery"),
    "WAFER_DIAMETER": ("Preassembly general", "Wafer diameter"),
    "BEOL_STACK_THICKNESS": ("Front Side Stack", "Passivation Stack w/o EPA"),
    "ORGANIC_PASIVATION": ("Front Side Stack", "Organic Passivation Material"),
    "BACK_SIDE_METAL_STACK_WITH_THICKNESS": ("Back Side Stack", "Last BackSideMetal Stack w/ Thickness"),
    "FINAL_THICKNESS_INCL_SUBSTRATE": ("Thinning", "Si thickness incl. BSM/µm"),
    "FINAL_THICKNESS_INCL_SUBSTRATE_AND_IMIDE": ("Thinning", "Thickness incl. Imid and BSM /µm"),
    "RASTER_X": ("Preassembly general", "Raster x/mm"),
    "RASTER_Y": ("Preassembly general", "Raster y/mm"),
    "AREA": ("Preassembly general", "Area/mm^2"),
    "RATIO": ("Preassembly general", "Ratio"),
})

def get_value(category, param):
    for cat in data.get("mainCategories", []):
        if cat["name"] == category:
            for p in cat.get("parameters", []):
                if p["name"] == param:
                    return p["values"][0] if p["values"] else None
    return None

result = {}

# Debug: Print all available categories and parameter names
print("Available categories and parameters in API response:")
for cat in data.get("mainCategories", []):
    print(f"Category: {cat['name']}")
    for p in cat.get("parameters", []):
        print(f"  Parameter: {p['name']}")
        print(f"    Values: {p['values']}")
print("\n--- End of API structure ---\n")

for field in all_fields:
    # Try both original and lower/upper/underscore-insensitive keys
    map_key = field
    if map_key not in attribute_map:
        # Try to match ignoring case and underscores
        for k in attribute_map:
            if k.replace('_', '').lower() == field.replace('_', '').lower():
                map_key = k
                break
    if map_key in attribute_map:
        cat, param = attribute_map[map_key]
        result[field] = get_value(cat, param)
    else:
        result[field] = "not mapped yet"



# Output as JSON for OutSystems integration
import json
print(json.dumps(result, indent=2))
