#general script
import ifcopenshell
import pandas as pd

# === Config ===
ifc_file_path = "USZ_MI12_FAS_BM_GE_FASSA.ifc"

# 1. Filter by this PSet property
element_filter = ("Pset", ("YourPSetName", "YourPropertyName"), "DesiredValue")

# 2. Grouping logic
group_by_attributes = [
    ("Name", "WallName"),
    ("Pset", ("Fire Protection", "Feuerwiderstand Soll"))
]

# 3. Surface area logic
area_source = ("Pset", ("Dimensions", "Area"))

# === Load and filter ===
ifc_file = ifcopenshell.open(ifc_file_path)

# Load a broad category (or even everything if needed)
elements = ifc_file.by_type("IfcBuildingElement")  # Or use ifc_file.by_type("IfcProduct") for max coverage

# === Helper functions ===
def get_property_value(element, pset_name, prop_name):
    for definition in element.IsDefinedBy:
        if definition.is_a("IfcRelDefinesByProperties"):
            props = definition.RelatingPropertyDefinition
            if props.is_a("IfcPropertySet") and props.Name == pset_name:
                for prop in props.HasProperties:
                    if prop.Name == prop_name:
                        val = getattr(prop, "NominalValue", None)
                        return val.wrappedValue if hasattr(val, "wrappedValue") else val
    return None

def get_clean_name(name):
    if not name:
        return None
    parts = name.split(":")
    return parts[1] if len(parts) >= 3 else name

def get_attribute(element, attr_config):
    attr_type, spec = attr_config
    if attr_type == "Name":
        return get_clean_name(element.Name)
    elif attr_type == "Pset":
        pset_name, prop_name = spec
        value = get_property_value(element, pset_name, prop_name)
        return str(value) if value else "0"
    return None

def get_surface_area(element, source):
    if source[0] == "Pset":
        pset_name, prop_name = source[1]
        value = get_property_value(element, pset_name, prop_name)
        try:
            return float(value) if value else 0.0
        except:
            return 0.0
    return 0.0

def passes_filter(element, filter_config):
    filter_type, (pset, prop), target_value = filter_config
    if filter_type == "Pset":
        value = get_property_value(element, pset, prop)
        return str(value) == str(target_value)
    return True

# === Main processing ===
data = []

for element in elements:
    if not passes_filter(element, element_filter):
        continue

    entry = {}
    for label, attr_cfg in group_by_attributes:
        entry[label] = get_attribute(element, (label, attr_cfg))
    entry["Surface_m2"] = get_surface_area(element, area_source)
    data.append(entry)

# === Group and export ===
df = pd.DataFrame(data)
group_cols = [label for label, _ in group_by_attributes]
grouped = df.groupby(group_cols).agg({"Surface_m2": "sum"}).reset_index()

output_file = "filtered_grouped_data.csv"
grouped.to_csv(output_file, index=False)

print(f"✅ Exported to '{output_file}' with {len(grouped)} grouped rows")
