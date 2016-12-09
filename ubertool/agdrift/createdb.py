# import csv to sqlite database
# import csv, sqlite3
#
# con = sqlite3.connect("sqlite_agdrift.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f);") # use your column names here
#
# with open('agdrift_database.csv','rb') as fin: # `with` statement available in 2.5+
#     # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['distance'], i['pond_airblast_orchard'],i['pond_airblast_vineyard'],i['pond_ground_high_f2m'],i['pond_ground_high_vf2f'],i['pond_ground_low_f2m'],i['pond_ground_low_vf2f'],i['pond_aerial_c2vc'],i['pond_aerial_m2c'],i['pond_aerial_f2m'],i['pond_aerial_vf2f']) for i in dr]
#
# cur.executemany("INSERT INTO output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# con.commit()# save changes
# con.close()

#
# ## fetch and display records by raws from output table
#
# import sqlite3
#
# conn = sqlite3.connect('agdrift.db')
# print "Opened database successfully";
#
# cursor = conn.execute("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# for row in cursor:
#    print "distance = ", row[0]
#    print "pond_airblast_orchard = ", row[1]
#    print "pond_airblast_vineyard = ", row[2]
#    print "pond_ground_high_f2m = ", row[3]
#    print "pond_ground_high_vf2f = ", row[4]
#    print "pond_ground_low_f2m = ", row[5]
#    print "pond_ground_low_vf2f = ", row[6]
#    print "pond_aerial_c2vc = ", row[7]
#    print "pond_aerial_m2c = ", row[8]
#    print "pond_aerial_f2m = ", row[9]
#    print "pond_aerial_vf2f = ", row[10], "\n"
#
# print "Operation done successfully";
# conn.close()
#
#
# ## fetch and display records for one column from output table
import sqlite3

conn = sqlite3.connect('sqlite_agdrift.db')
print "Opened database successfully";

cursor = conn.execute("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
for row in cursor:
      print row[4]

print "Operation done successfully";
conn.close()


# ## method2_fetch and display records for one column from output table
# import sqlite3
#
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_ground_high_vf2f  from output")
# pond_ground_high_vf2fs = cur.fetchall()
# #print(pond_ground_high_vf2fs)
# import numpy as np
# pond_ground_high_vf2fs = np.array(pond_ground_high_vf2fs).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_ground_high_f2m
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_ground_high_f2m  from output")
# pond_ground_high_f2m = cur.fetchall()
# import numpy as np
# pond_ground_high_f2m = np.array(pond_ground_high_f2m).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_ground_low_vf2f
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_ground_low_vf2f  from output")
# pond_ground_low_vf2f = cur.fetchall()
# import numpy as np
# pond_ground_low_vf2f = np.array(pond_ground_low_vf2f).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_ground_low_f2m
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_ground_low_f2m  from output")
# pond_ground_low_f2m = cur.fetchall()
# import numpy as np
# pond_ground_low_f2m = np.array(pond_ground_low_f2m).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_aerial_vf2f
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_aerial_vf2f  from output")
# pond_aerial_vf2f = cur.fetchall()
# import numpy as np
# pond_aerial_vf2f = np.array(pond_aerial_vf2f).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_aerial_f2m
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_aerial_f2m  from output")
# pond_aerial_f2m = cur.fetchall()
# import numpy as np
# pond_aerial_f2m = np.array(pond_aerial_f2m).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_aerial_m2c
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_aerial_m2c  from output")
# pond_aerial_m2c = cur.fetchall()
# import numpy as np
# pond_aerial_m2c = np.array(pond_aerial_m2c).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_aerial_c2vc
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_aerial_c2vc  from output")
# pond_aerial_c2vc = cur.fetchall()
# import numpy as np
# pond_aerial_c2vc = np.array(pond_aerial_c2vc).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_airblast_orchard
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_airblast_orchard  from output")
# pond_airblast_orchard = cur.fetchall()
# import numpy as np
# pond_airblast_orchard = np.array(pond_airblast_orchard).astype('float').flatten()
# cur.close()
# conn.close()
#
# ## import pond_airblast_vineyard
# import sqlite3
# conn = sqlite3.connect('agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_airblast_vineyard  from output")
# pond_airblast_vineyard = cur.fetchall()
# import numpy as np
# pond_airblast_vineyard = np.array(pond_airblast_vineyard).astype('float').flatten()
# cur.close()
# conn.close()
# # ## fetch and display records by column from output table
# # import sqlite3
# #
# # conn = sqlite3.connect('agdrift.db')
# # print "Opened database successfully";
# #
# # cursor = conn.execute("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# # for row in cursor:
# #       print('{0},{1}, {2},{3},{4},{5},{6},{7},{8},{9},{10}'.format(row[0], row[1], row[2],row[3], row[4], row[5],row[6], row[7], row[8],row[9], row[10]))
# #
# #
# # print "Operation done successfully";
# # conn.close()


