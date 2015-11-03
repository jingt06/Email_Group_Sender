#/usr/bin/env python3

from flask import Flask, jsonify

import json
import sys
import datetime
from flask import request

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


@app.route("/main",methods=['GET','POST'])
def main():
	usr = request.args.get("usr")
	psd = request.args.get("psd")
	sbj = request.args.get("sbj")
	txt = request.args.get("txt")
	rcv = request.args.get("rcv")
	if usr is None or psd is None or sbj is None or txt is None or rcv is None:
		result = {
			"success" : False,
			"error" : "some information not specified",
			"serverTime" : str(datetime.datetime.now)
		}
		return  json.dumps(result,ensure_ascii=False,indent=4)

	usr="genetao06@hotmail.com"
	psd="tj.1994.12.06"
	server = smtplib.SMTP("smtp.live.com",587)
	server.ehlo()
	server.starttls()
	server.login(usr, psd)
	msg = MIMEMultipart()
	msg.attach(MIMEText(txt,'plain','utf-8'))
	msg['subject'] = sbj
	msg['From'] = usr
	msg['To'] = rcv
	server.sendmail(usr, rcv, msg.as_string())
	server.quit()

	return("ok")


if __name__ == '__main__':
	app.run(port=8080,debug=True)