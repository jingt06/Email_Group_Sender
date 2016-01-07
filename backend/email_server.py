#/usr/bin/env python3

from flask import Flask, jsonify
from flask.ext.cors import CORS
import json
import sys
import datetime
from flask import request
import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

@app.route("/mail",methods=['GET','POST'])
def main():
	usr = request.args.get("usr")
	psd = request.args.get("psd")
	sbj = request.args.get("sbj")
	txt = request.args.get("txt")
	rcv = request.args.getlist("rcv")
	if usr is None or psd is None or sbj is None or txt is None or rcv is None:
		result = {
			"success" : False,
			"error" : "some information not specified",
			"serverTime" : str(datetime.datetime.now)
		}
		return  json.dumps(result,ensure_ascii=False,indent=4)
	server = smtplib.SMTP("smtp.live.com",587)
	server.ehlo()
	server.starttls()
	server.login(usr, psd)
	msg = MIMEMultipart()
	msg.attach(MIMEText(txt,'plain','utf-8'))
	msg['subject'] = sbj
	msg['From'] = usr
	msg['To'] = ",".join(rcv)
	server.sendmail(usr, rcv, msg.as_string())
	server.quit()
	return("ok")

@app.route("/all_group",methods=['GET','POST'])
def all_group():
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
	groups = cursor.fetchall()
	final=[]
	for group in groups:
		final.append(group[0])
	groups_array = json.dumps(final)
	return(groups_array)

@app.route("/add_group",methods=['GET','POST'])
def add_group():
	group_name = request.args.get("n")
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
	groups = cursor.fetchall()
	if( group_name not in list(map(lambda x:x[0],groups)) ):
		execution = "CREATE TABLE " + group_name + " (email varchar(50))"
		cursor.execute(execution)
		conn.commit()
		return("ok")
	else:
		return("group already exists")
	return("error")

@app.route("/get_addresses",methods=['GET','POST'])
def get_addresses():
	group = request.args.get("group")
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT email FROM " + group)
	groups = cursor.fetchall()
	final=[]
	for group in groups:
		final.append(group[0])
	addr = json.dumps(final)
	return(addr)


@app.route("/add_address",methods=['GET','POST'])
def add_address():
	group = request.args.get("group")
	address = request.args.get("address")
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT email FROM " + group)
	addresses = cursor.fetchall()
	if( address not in list(map(lambda x:x[0],addresses)) ):
		execution = "INSERT INTO " + group + "(email) VALUES ('" + address + "')"
		cursor.execute(execution)
		conn.commit()
		return("ok")
	else:
		return("address already exists")
	return("error")


@app.route("/delete_address",methods=['GET','POST'])
def delete_address():
	group = request.args.get("group")
	address = request.args.get("address")
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	execution = "DELETE FROM " + group + " WHERE email ='" + address + "'"
	cursor.execute(execution)
	conn.commit()
	return("")

@app.route("/delete_group",methods=['GET','POST'])
def delete_group():
	group = request.args.get("group")
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS " + group)
	conn.commit()
	return("")

@app.route("/test",methods=['GET','POST'])
def test():
	conn_string = "host='localhost' dbname='email_group_sender' user='git' password='12345678'"
	conn = psycopg2.connect(conn_string)
	return("Connected")

@app.route("/create_group",methods=['GET','POST'])
def delete_group():
	group = request.args.get("group")
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("")
	conn.commit()
	return("")





if __name__ == '__main__':
	app.run(port=8080,debug=True)











