from __future__ import division
import csv

metadata = MetaData()

#import csv to sqlite database
con = sqlite3.connect("sqlite_agdrift_distance.db")
cur = con.cursor()
cur.execute("CREATE TABLE output (distance_ft,aerial_vf2f,aerial_f2m,aerial_m2c,aerial_c2vc,ground_low_vf,ground_low_fmc,ground_high_vf,ground_high_fmc,airblast_normal,airblast_dense,airblast_sparse,airblast_vineyard,airblast_orchard);") # use your column names here

with open('opp_spray_drift_values.csv','rb') as fin: # `with` statement available in 2.5+
     # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['distance_ft'], i['aerial_vf2f'],i['aerial_f2m'],i['aerial_m2c'],i['aerial_c2vc'],i['ground_low_vf'],i['ground_low_fmc'],i['ground_high_vf'],i['ground_high_fmc'],i['airblast_normal'],i['airblast_dense'],i['airblast_sparse'],i['airblast_vineyard'],i['airblast_orchard']) for i in dr]

cur.executemany("INSERT INTO output (distance_ft,aerial_vf2f,aerial_f2m,aerial_m2c,aerial_c2vc,ground_low_vf,ground_low_fmc,ground_high_vf,ground_high_fmc,airblast_normal,airblast_dense,airblast_sparse,airblast_vineyard,airblast_orchard) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?);", to_db)
con.commit()
con.close()

