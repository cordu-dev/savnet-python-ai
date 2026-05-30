import os


def find_in_path(base_path: str, target_name: str):
    matches = []
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            if d == target_name:
                matches.append(os.path.join(root, d))
        for f in files:
            if f == target_name:
                matches.append(os.path.join(root, f))
    return matches


findings = find_in_path("M2/", "file.bin")

print(findings)
