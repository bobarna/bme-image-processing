import csv
rows = []
with open("output.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row[0].split(';'))

def get_original_file_name(f):
    return '_'.join(f.split('_')[0:-1]) + ".jpg"

# Find all original file names
original_file_names = set()
output_rows = {}
for r in rows:
    # print(r)
    og_fn = get_original_file_name(r[0])
    # Create or append dict element
    # print(r)
    output_rows[og_fn] = r[1:] if not (og_fn in output_rows) else output_rows[og_fn] + r[1:]

with open('output_original.csv', mode='w') as f:
    for r in output_rows:
        # Write each line to the output
        f.write("{};{}\n".format(
            r,
            ';'.join(output_rows[r])
        ))
