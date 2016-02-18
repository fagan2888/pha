import os
from collections import defaultdict

n_digits = 4    # number of digits used in filenames
n_scenarios = 117
inputs_dir = "inputs"
inputs_subdir = "pha_117"
pha_dir = os.path.join(inputs_dir, inputs_subdir)
mean_dir = os.path.join(inputs_dir, inputs_subdir + "_mean") 

values = defaultdict(list)
sums = defaultdict(float)

for x in range(n_scenarios):
    with open(os.path.join(
            inputs_dir, inputs_subdir, "fuel_supply_curves_{}.dat".format(str(x).zfill(n_digits))
        )
    ) as f:
        rows = [r.split("\t") for r in f.read().split('\n')]
        for r in rows[1:-2]:   # omit header row and semicolon and blank line at end
            key = r[0]
            if r[2] != "base":
                key += r[2]
            values[(key, r[1])].append(r[3])
            sums[(r[0], r[1], r[2])] += float(r[3])

# store the average values back into the row list
for r in rows[1:-2]:
    r[3] = str(sums[(r[0], r[1], r[2])] / float(n_scenarios))

# write the mean values to a special fuel supply curve
if not os.path.exists(mean_dir):
    os.makedirs(mean_dir)
with open(os.path.join(mean_dir, "fuel_supply_curves_0000.dat"), "w") as f:
    f.write("\n".join(["\t".join(r) for r in rows]))

with open(os.path.join(pha_dir, "fuel_supply_costs.tsv"), "w") as f:
    f.write("fuel\tyear\tprice_per_mmbtu\n")
    f.writelines(
        "\t".join(list(k) + map(str, values[k])) + "\n"
            for k in sorted(values.keys())
    )

