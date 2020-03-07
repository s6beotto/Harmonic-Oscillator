from matplotlib import pyplot as plt
from tools import getRootDirectory
import csv
import sys

if len(sys.argv) >= 2:
	dirs = sys.argv[1:]
else:
	exit(-1)

root_path = getRootDirectory()

for subdir_pattern in dirs:
	for subdir in root_path.glob(subdir_pattern):
		filename = root_path / subdir
		relative_path = filename.relative_to(root_path / 'data')

		if not filename.exists() or filename.is_dir():
			continue

		distances = []
		tunneling_rates = []

		with filename.open('r') as csvfile:
			reader = csv.reader(csvfile)
			for i, row in enumerate(reader):
				#print(row)
				if i == 0:
					pass
				else:
					distance = float(row[0])
					tunneling_rate = int(row[1])
					distances.append(distance)
					tunneling_rates.append(tunneling_rate)

		plt.figure()
		plt.errorbar(distances, tunneling_rates, fmt='.')
		plt.xlabel('Distance')
		plt.ylabel('Tunneling rate')

		out_filename = root_path / 'imgs' / relative_path
		out_filename.parent.mkdir(parents=True, exist_ok=True)

		plt.savefig(out_filename.with_suffix(".pdf"))