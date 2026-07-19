with open("data/training_pairs.txt", "r") as f:
    lines = f.readlines()

training_texts = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("CLAUSE:"):
        clause = line.replace("CLAUSE:", "").strip()
    elif line.startswith("EXPLANATION:"):
        explanation = line.replace("EXPLANATION:", "").strip()
        if clause and explanation:
            training_texts.append(f"Clause: {clause}\nExplanation: {explanation}\n")

with open("data/training_data.txt", "w") as f:
    f.writelines(training_texts)
