from __future__ import division
import logging
import sqlite3
import numpy as np
import pandas as pd
import unittest
from sqlalchemy import Column, Table, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# from sqlalchemy import *
metadata = MetaData()


# import csv, sqlite3
# #import csv to sqlite database
# con = sqlite3.connect("sqlite_agdrift.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f);") # use your column names here
#
# with open('agdrift_database.csv','rb') as fin: # `with` statement available in 2.5+
#      # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['distance'], i['pond_airblast_orchard'],i['pond_airblast_vineyard'],i['pond_ground_high_f2m'],i['pond_ground_high_vf2f'],i['pond_ground_low_f2m'],i['pond_ground_low_vf2f'],i['pond_aerial_c2vc'],i['pond_aerial_m2c'],i['pond_aerial_f2m'],i['pond_aerial_vf2f']) for i in dr]
#
# cur.executemany("INSERT INTO output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# con.commit()# save changes
# con.close()
# output = Table('output', metadata, autoload=True, autoload_with=conn)


def get_distance():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT distance from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_distance()
print(answer)
print(answer.dtype)


def get_pond_ground_high_vf2f():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_ground_high_vf2f from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_ground_high_vf2f()
print(answer)
print(answer.dtype)


def get_pond_ground_high_f2m():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_ground_high_f2m from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_ground_high_f2m()
print(answer)
print(answer.dtype)


def get_pond_ground_low_f2m():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_ground_low_f2m from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_ground_low_f2m()
print(answer)
print(answer.dtype)


def get_pond_ground_low_vf2f():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_ground_low_vf2f from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_ground_low_vf2f()
print(answer)
print(answer.dtype)


def get_pond_aerial_vf2f():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_aerial_vf2f from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_aerial_vf2f()
print(answer)
print(answer.dtype)


def get_pond_aerial_f2m():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_aerial_f2m from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_aerial_f2m()
print(answer)
print(answer.dtype)


def get_pond_aerial_m2c():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_aerial_m2c from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_aerial_m2c()
print(answer)
print(answer.dtype)


def get_pond_aerial_c2vc():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_aerial_c2vc from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_aerial_c2vc()
print(answer)
print(answer.dtype)


def get_pond_airblast_orchard():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_airblast_orchard from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_airblast_orchard()
print(answer)
print(answer.dtype)


def get_pond_airblast_vineyard():
    engine = create_engine('sqlite:///sqlite_agdrift.db')
    conn = engine.connect()
    result = conn.execute("SELECT pond_airblast_vineyard from output")
    data = np.zeros(300)
    for i, row in enumerate(result):
        temp = float(row[0])
        data[i] = temp.real
    conn.close()
    return data


answer = get_pond_airblast_vineyard()
print(answer)
print(answer.dtype)

# cursor = conn.connection.cursor("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# cursor.execute("SELECT pond_ground_high_vf2f from output")
# pond_ground_high_vf2fs = cursor.fetchall()
# pond_ground_high_vf2fs = np.array(pond_ground_high_vf2fs).astype('float').flatten()
# cursor.close()
# conn.close()
# cursor = conn.execute("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# for row in cursor:
#       print row[4]

#
#
# import csv, sqlite3
# import csv to sqlite database
# con = sqlite3.connect("sqlite_agdrift.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f);") # use your column names here
#
# with open('agdrift_database.csv','rb') as fin: # `with` statement available in 2.5+
#      # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['distance'], i['pond_airblast_orchard'],i['pond_airblast_vineyard'],i['pond_ground_high_f2m'],i['pond_ground_high_vf2f'],i['pond_ground_low_f2m'],i['pond_ground_low_vf2f'],i['pond_aerial_c2vc'],i['pond_aerial_m2c'],i['pond_aerial_f2m'],i['pond_aerial_vf2f']) for i in dr]
#
# cur.executemany("INSERT INTO output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# con.commit()# save changes
# con.close()
#
# #Create an engine that stores data in the local directory's
# #sqlalchemy_example.db file.
# class Bookmarks(object):
#     pass
#
# def loadSession():
#       dbPath ="sqlite.agdrift"
#       engine = create_engine('sqlite:///sqlite_agdrift.db'% dbPath, echo=False)
#       Base = declarative_base(engine)
#
#       class Bookmarks(Base):
#             """"""
#             __tablename__ = 'output'
#             __table_args__ = {'autoload': True}
#
#       metadata = MetaData(engine)
#       output =Table("output", metadata, autoload=True)
#       mapper(Bookmarks, output)
#       Session = sessionmaker(bind=engine)
#       session = Session()
#       return session
#
#
# metadata = MetaData(engine)
# moz_bookmarks = Table('output', metadata,
#                       Column('id', Integer, primary_key=True),
#                       Column('pond_airblast_orchard', Float),
#                       Column('pond_ground_high_f2m', Float),
#                       Column('pond_ground_high_vf2f', Float),
#                       Column('pond_ground_low_f2m', Float),
#                       Column('pond_ground_low_vf2f', Float),
#                       Column('pond_aerial_c2vc', Float),
#                       Column('pond_aerial_f2m', Float),
#                       Column('pond_aerial_vf2f', Float))
#
# mapper(Bookmarks, output)
#
# Session = sessionmaker(bind=engine)
# session = Session()
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)
#
# conn = engine.connect('sqlit_agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_ground_high_vf2f from output")
# pond_ground_high_vf2fs = cur.fetchall()
# pond_ground_high_vf2fs = np.array(pond_ground_high_vf2fs).astype('float').flatten()
# cur.close()
# conn.close()
#


#


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
# import sqlite3
#
# conn = sqlite3.connect('sqlite_agdrift.db')
# print "Opened database successfully";
#
# cursor = conn.execute("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# for row in cursor:
#       print row[4]
#
# print "Operation done successfully";
# conn.close()

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






# import csv, sqlite3
# #import csv to sqlite database
# con = sqlite3.connect("sqlite_agdrift.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f);") # use your column names here
#
# with open('agdrift_database.csv','rb') as fin: # `with` statement available in 2.5+
#      # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['distance'], i['pond_airblast_orchard'],i['pond_airblast_vineyard'],i['pond_ground_high_f2m'],i['pond_ground_high_vf2f'],i['pond_ground_low_f2m'],i['pond_ground_low_vf2f'],i['pond_aerial_c2vc'],i['pond_aerial_m2c'],i['pond_aerial_f2m'],i['pond_aerial_vf2f']) for i in dr]
#
# cur.executemany("INSERT INTO output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# con.commit()# save changes
# con.close()

# output = Table('output', metadata, autoload=True, autoload_with=conn)

# def get_pond_ground_high_vf2f():
#       engine = create_engine('sqlite:///sqlite_agdrift.db')
#       conn = engine.connect()
#       result =conn.execute("SELECT pond_ground_high_vf2f from output")
#       data = np.zeros(300)
#       for i, row in enumerate(result):
#             temp = float(row[0])
#             data[i] = temp.real
#       conn.close()
#       return data
#
# answer = get_pond_ground_high_vf2f()
# print (answer)
# print(answer.dtype)
#
#
#
# def get_pond_ground_high_f2m():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_ground_high_f2m from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
#
# answer = get_pond_ground_high_f2m()
# print(answer)
# print(answer.dtype)
#
# def get_pond_ground_low_f2m():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_ground_low_f2m from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
# answer = get_pond_ground_low_f2m()
# print(answer)
# print(answer.dtype)
#
# def get_pond_ground_low_vf2f():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_ground_low_vf2f from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
#
# answer = get_pond_ground_low_vf2f()
# print(answer)
# print(answer.dtype)
#
# def get_pond_aerial_vf2f():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_aerial_vf2f from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
#
# answer = get_pond_aerial_vf2f()
# print(answer)
# print(answer.dtype)
#
# def get_pond_aerial_f2m():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_aerial_f2m from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
# answer = get_pond_aerial_f2m()
# print(answer)
# print(answer.dtype)
#
# def get_pond_aerial_m2c():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_aerial_m2c from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
# answer = get_pond_aerial_m2c()
# print(answer)
# print(answer.dtype)
#
# def get_pond_aerial_c2vc():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_aerial_c2vc from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
# answer = get_pond_aerial_c2vc()
# print(answer)
# print(answer.dtype)
#
# def get_pond_airblast_orchard():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_airblast_orchard from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
# answer = get_pond_airblast_orchard()
# print(answer)
# print(answer.dtype)
#
# def get_pond_airblast_vineyard():
#     engine = create_engine('sqlite:///sqlite_agdrift.db')
#     conn = engine.connect()
#     result = conn.execute("SELECT pond_airblast_vineyard from output")
#     data = np.zeros(300)
#     for i, row in enumerate(result):
#         temp = float(row[0])
#         data[i] = temp.real
#     conn.close()
#     return data
#
# answer = get_pond_airblast_vineyard()
# print(answer)
# print(answer.dtype)

# cursor = conn.connection.cursor("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# cursor.execute("SELECT pond_ground_high_vf2f from output")
# pond_ground_high_vf2fs = cursor.fetchall()
# pond_ground_high_vf2fs = np.array(pond_ground_high_vf2fs).astype('float').flatten()
# cursor.close()
# conn.close()
# cursor = conn.execute("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# for row in cursor:
#       print row[4]

#
#
# import csv, sqlite3
# import csv to sqlite database
# con = sqlite3.connect("sqlite_agdrift.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f);") # use your column names here
#
# with open('agdrift_database.csv','rb') as fin: # `with` statement available in 2.5+
#      # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['distance'], i['pond_airblast_orchard'],i['pond_airblast_vineyard'],i['pond_ground_high_f2m'],i['pond_ground_high_vf2f'],i['pond_ground_low_f2m'],i['pond_ground_low_vf2f'],i['pond_aerial_c2vc'],i['pond_aerial_m2c'],i['pond_aerial_f2m'],i['pond_aerial_vf2f']) for i in dr]
#
# cur.executemany("INSERT INTO output (distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# con.commit()# save changes
# con.close()
#
# #Create an engine that stores data in the local directory's
# #sqlalchemy_example.db file.
# class Bookmarks(object):
#     pass
#
# def loadSession():
#       dbPath ="sqlite.agdrift"
#       engine = create_engine('sqlite:///sqlite_agdrift.db'% dbPath, echo=False)
#       Base = declarative_base(engine)
#
#       class Bookmarks(Base):
#             """"""
#             __tablename__ = 'output'
#             __table_args__ = {'autoload': True}
#
#       metadata = MetaData(engine)
#       output =Table("output", metadata, autoload=True)
#       mapper(Bookmarks, output)
#       Session = sessionmaker(bind=engine)
#       session = Session()
#       return session
#
#
# metadata = MetaData(engine)
# moz_bookmarks = Table('output', metadata,
#                       Column('id', Integer, primary_key=True),
#                       Column('pond_airblast_orchard', Float),
#                       Column('pond_ground_high_f2m', Float),
#                       Column('pond_ground_high_vf2f', Float),
#                       Column('pond_ground_low_f2m', Float),
#                       Column('pond_ground_low_vf2f', Float),
#                       Column('pond_aerial_c2vc', Float),
#                       Column('pond_aerial_f2m', Float),
#                       Column('pond_aerial_vf2f', Float))
#
# mapper(Bookmarks, output)
#
# Session = sessionmaker(bind=engine)
# session = Session()
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)
#
# conn = engine.connect('sqlit_agdrift.db')
# cur = conn.cursor()
# cur.execute("SELECT pond_ground_high_vf2f from output")
# pond_ground_high_vf2fs = cur.fetchall()
# pond_ground_high_vf2fs = np.array(pond_ground_high_vf2fs).astype('float').flatten()
# cur.close()
# conn.close()
#


#


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
# import sqlite3
#
# conn = sqlite3.connect('sqlite_agdrift.db')
# print "Opened database successfully";
#
# cursor = conn.execute("SELECT distance,pond_airblast_orchard,pond_airblast_vineyard,pond_ground_high_f2m,pond_ground_high_vf2f,pond_ground_low_f2m,pond_ground_low_vf2f,pond_aerial_c2vc,pond_aerial_m2c,pond_aerial_f2m,pond_aerial_vf2f  from output")
# for row in cursor:
#       print row[4]
#
# print "Operation done successfully";
# conn.close()

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
