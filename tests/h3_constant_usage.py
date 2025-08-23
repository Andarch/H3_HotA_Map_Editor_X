import os
import re

H3M_PATH = "h3mex\\core\\h3m"
SRC_PATH = "h3mex\\src"
OUTPUT_PATH = "tests\\h3_constant_usage.txt"


def extract_class_names_from_file(filepath, modulename):
    class_names = set()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        # Class names
        for cls in re.findall(r"^class\s+([A-Za-z_][A-Za-z0-9_]*)", content, re.MULTILINE):
            class_names.add(f"{modulename}.{cls}")
    return class_names


# Step 1: Gather all qualified class names from h3m files
qualified_class_names = set()
for filename in os.listdir(H3M_PATH):
    if filename.endswith(".py") and filename != "__init__.py":
        modulename = filename[:-3]  # Remove .py
        filepath = os.path.join(H3M_PATH, filename)
        qualified_class_names.update(extract_class_names_from_file(filepath, modulename))

# Step 2: Search for usage in src
usage = {name: [] for name in qualified_class_names}
for root, dirs, files in os.walk(SRC_PATH):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                for name in qualified_class_names:
                    if re.search(rf"\b{name}\b", content):
                        usage[name].append(filepath)

# Step 3: Write results to file
with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for name in sorted(usage.keys()):
        out.write(f"{name}:\n")
        for mod in usage[name]:
            out.write(f"  {mod}\n")
        out.write("\n")

print(f"Results written to {OUTPUT_PATH}")
