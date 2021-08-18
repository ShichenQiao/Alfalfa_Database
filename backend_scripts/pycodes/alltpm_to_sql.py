import csv

with open('alltpm.csv', 'r') as fp:
    reader = csv.reader(fp)
    rf = open('alltpm.sql', 'w')
    for row in reader:
        values = ""
        for x in row:
            values += "\"" + x + "\","
        values = values[0 : len(values) - 1]
        sql = "INSERT INTO alltpm(GeneID, \"150_trueleaf_rep1\", \"150_xia_rep1\", \"150_ziye_rep1\", fennie_rep1, flower_bud_rep1, flower_rep1, flower_rep2, flower_rep3, flower_rep4, flower_rep5, flower_rep6, flower_rep7, flower_rep8, germ_seed_rep1, guojia_rep1, lateral_root_rep1, leaf_bud_rep1, leaf_bud_rep2, leaf_bud_rep3, main_root_rep1, mature_leaf_rep1, mature_leaf_rep2, mature_leaf_rep3, MS_trueleaf_rep1, MS_xia_rep1, MS_ziye_rep1, nod_21_rep1, nod_28_rep1, seed_rep1, stem_branch_rep1, stem_rep1, yige_rep1, yige_rep2, yige_rep3, young_leaf_rep1, young_leaf_rep2, young_leaf_rep3) VALUES(" + values + ");\n"
        rf.write(sql)
    fp.close()
    rf.close()