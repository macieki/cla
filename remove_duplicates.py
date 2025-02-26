import csv

input_csv = "ads_data.csv"
output_csv = "ads_data_unique.csv"

# Set to track seen links and list to store unique rows
seen_links = set()
unique_rows = []

with open(input_csv, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        link = row.get("link", "")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_rows.append(row)

if unique_rows:
    fieldnames = unique_rows[0].keys()
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)
    print(f"Done! {len(unique_rows)} unique ads written to {output_csv}.")
else:
    print("No unique data found.")
