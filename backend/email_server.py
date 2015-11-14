#/usr/bin/env python3

from flask import Flask, jsonify

import json
import sys
import datetime
from flask import request
import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


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
	groups_array = json.dumps(groups)
	return(groups_array)

@app.route("/add_group",methods=['GET','POST'])
def add_group():
	group_name = request.args.get("n")
	conn_string = "host='localhost' dbname='email_group_sender' user='postgres' password='12345678'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
	groups = cursor.fetchall()
	if( group_name not in groups ):
		cursor.execute("CREATE TABLE " + group_name + " (email varchar(50))")
		return("ok")
	return("error")


@app.route("/test",methods=['GET','POST'])
def test():
	conn_string = "host='localhost' dbname='email_group_sender' user='git' password='12345678'"
	conn = psycopg2.connect(conn_string)
	return("Connected")





if __name__ == '__main__':
	app.run(port=8080,debug=True)











