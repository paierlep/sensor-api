import sqlite3

"""
Simple file to generate a simple sqlite3 database
to store the sensor measurements
"""

conn = sqlite3.connect('../database.db')

conn.execute('CREATE TABLE sensor_measurements '
             '(timestamp INTEGER,'
             ' sensor TEXT,'
             ' humidity REAL,'
             ' temperature REAL,'
             ' pressure REAL)'
             )

conn.close();
