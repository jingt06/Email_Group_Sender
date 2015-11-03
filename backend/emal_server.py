#/usr/bin/env python3

from flask import Flask, jsonify

import json
import sys
from flask import request

app = Flask(__name__)


@app.route("/main",methods=['GET','POST'])
def main():
	usr = request.args.get("usr")
	psd = request.args.get("psd")
	sbj = request.args.get("sbj")
	txt = request.args.get("txt")
	rcv = request.args.get("rcv")
	server = smtplib.SMTP("smtp.live.com",587)
	server.ehlo()
	server.starttls()
	server.login(usr, psd)
	msg = MINEMultipart()
	msg.attach(txt)
	msg['subject'] = sbj
	msg['From'] = usr
	msg['To'] = ";".join(rcv)
	server.sendmail(usr, rcv, msg.as_string())
	server.quit()

	return("ok")


if __name__ == '__main__':
	app.run(port=8080)