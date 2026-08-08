import json

with open("PRisma-ContoursPR.ipynb", "r") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = cell["source"]
        for i, line in enumerate(source):
            if "geo.blockFactor(ringed.tau, ieff)" in line:
                source[i] = line.replace("geo.blockFactor(ringed.tau, ieff)", "geo.blockFactor(-np.log(ringed.alpha), ieff)")

with open("PRisma-ContoursPR.ipynb", "w") as f:
    json.dump(nb, f, indent=1)
