import argparse
import sqlite3
import os
import pandas as pd
import datetime

def time_convert(time):
	time = time / 100000
	human_time = datetime.datetime.fromtimestamp(time)
	return human_time

def downloads(filename, path):
	downloads_csv_path = path + "/downloads.csv"
	downloads_html_path = path + "/downloads.html"
	downloads_query = "SELECT moz_annos.content, moz_annos.dateAdded, moz_annos.flags, moz_annos.expiration, \
	moz_annos.type, moz_annos.lastModified, moz_places.url, moz_places.title, moz_places.description \
	FROM moz_annos INNER JOIN moz_places on moz_annos.place_id = moz_places.id"
	conn = sqlite3.connect(filename, isolation_level=None,
	                       detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query(downloads_query, conn)
	db_df['dateAdded'] = db_df['dateAdded'].apply(time_convert)
	db_df['lastModified'] = db_df['lastModified'].apply(time_convert)
	db_df.to_csv(downloads_csv_path, index=False)
	db_df.to_html(downloads_html_path, index=False)

def web_history(filename, path):
	history_csv_path = path + "/history.csv"
	history_html_path = path + "/history.html"
	history_query = "SELECT moz_places.url, moz_places.title, moz_places.description, moz_historyvisits.visit_date \
	from moz_places INNER JOIN moz_historyvisits on moz_places.id = moz_historyvisits.place_id"
	conn = sqlite3.connect(filename, isolation_level=None,
	                       detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query(history_query, conn)
	db_df['visit_date'] = db_df['visit_date'].apply(time_convert)
	db_df.to_csv(history_csv_path, index=False)
	db_df.to_html(history_html_path, index=False)

def main():
	parser = argparse.ArgumentParser(description='Converts Chrome History File to CSV')
	parser.add_argument('-i', '--input', required=True, help='Input File Name')
	parser.add_argument('-o', '--output', required=True, help='Output Directory Name')
	args = parser.parse_args()
	os.mkdir(args.output)
	downloads(args.input, args.output)
	web_history(args.input, args.output)

if __name__ == '__main__':
    main()
