# IFC-Cost-Calculation

This script processes an IFC file to:

- ✅ Filter elements based on a custom **Property Set (PSet)** value
- 📊 Group them by one or more attributes or PSet values
- 📐 Extract surface area values from a defined PSet
- 📁 Export the results to a clean CSV file

Built with [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) and [pandas](https://pandas.pydata.org/).

**🧠 Script Logic**
Loads all IfcBuildingElement objects (you can change this to IfcProduct for broader coverage).

Applies the filter to include only elements matching your PSet rule.

Extracts grouping values and area per element.

Aggregates total surface area per group.

Exports the grouped data to filtered_grouped_data.csv.

---

## 📦 Requirements

**Install dependencies:**

```bash
pip install ifcopenshell pandas
⚙️ Configuration
Edit these variables at the top of the script to match your IFC file:

1. IFC File Path

2. Filter by Property Set

3. Grouping Configuration
Define how elements should be grouped in the output:

4. Surface Area Source
Set the property where area (in m²) is stored:

