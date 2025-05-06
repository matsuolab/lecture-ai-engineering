import nbformat
from nbformat import read, write

nb = read("homework.ipynb", as_version=4)


def ensure_state(meta):
    if isinstance(meta, list):
        for widget in meta:
            if "state" not in widget:
                widget["state"] = {}  # add empty state


# Top‐level widgets
if "widgets" in nb.metadata:
    ensure_state(nb.metadata["widgets"])

# Per‐cell widgets
for cell in nb.cells:
    if "widgets" in cell.metadata:
        ensure_state(cell.metadata["widgets"])

write(nb, "your_notebook_fixed.ipynb")
print("Injected missing state fields – output in your_notebook_fixed.ipynb")
