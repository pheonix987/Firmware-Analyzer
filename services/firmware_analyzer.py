import csv, json, os, re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

TOKEN_PATTERN = re.compile(
    r"<Tkn\d{3}[A-Z]{5}Tkn>"
)

def analyze_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        matches = TOKEN_PATTERN.findall(content)
        if not matches:
            return Counter(), 0

        return Counter(matches), len(matches)
    except Exception:
        return Counter(), 0


def analyze_firmware(
    directory_path: str,
    csv_output_path: str = "report.csv",
):
    all_files = []

    for root, _, files in os.walk(directory_path):
        for filename in files:
            all_files.append(os.path.join(root, filename))

    csv_rows = []
    global_token_counts = defaultdict(int)

    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(analyze_file, file_path): file_path
            for file_path in all_files
        }

        for future in futures:
            file_path = futures[future]
            token_counts, _ = future.result()

            if not token_counts:
                continue

            relative_path = os.path.relpath(file_path, directory_path)

            for token, occurrences in token_counts.items():
                csv_rows.append(
                    {
                        "Path": relative_path,
                        "Token": token,
                        "Occurrences": occurrences,
                    }
                )
                global_token_counts[token] += occurrences

    csv_rows.sort(
        key=lambda row: (
            row["Path"],
            row["Occurrences"],
            row["Token"],
        )
    )

    if os.path.dirname(csv_output_path):
        os.makedirs(os.path.dirname(csv_output_path), exist_ok=True)

    with open(csv_output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["Path", "Token", "Occurrences"],
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    summary = dict(global_token_counts)
    
    print(json.dumps(summary)) 

    return summary