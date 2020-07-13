
import json

lines = []
output = []

with open("jobava.json") as getCourse:
    lines = json.load(getCourse)[u"course"][u"data"]

for line in lines:
    if not line["showWInfo"]:
        output.append({
            "id": str(line["id"]),
            "pgn": " ".join(m["san"] for m in line["moves"]),
        })

with open(f"books/jobava.json", "w") as file:
    file.write(json.dumps(output, indent=2))
