# -*- coding: utf-8 -*-
import argparse
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl
import yaml

f = open("./info.yaml", "r")
info = yaml.load(f)

YOUR_NAME = info.YOUR_NAME
FROM_ADDRESS = info.FROM_ADDRESS
MY_PASSWORD = info.MY_PASSWORD
TO_ADDRESS = info.TO_ADDRESS
CC = info.CC
BCC = info.BCC

SUBJECT_START = '{} 勤務開始'.format(YOUR_NAME)
SUBJECT_END = '{}　勤務終了'.format(YOUR_NAME)
TIMESTAMP_PATH = "./TimeStamp"


def create_message(from_addr, to_addr, cc_addrs, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Cc'] = cc_addrs
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addrs, msg):
    #context = ssl.create_default_context()
    smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()

def write_time_stamp(start_time, end_time, rest_start_time, rest_end_time):
    # 今日の日付を記録
    today_stamp = str(datetime.date.today())
    file_path = os.path.join(TIMESTAMP_PATH, today_stamp + ".txt")
    with open(file_path, "w") as f:
        timestamp = "{} {} {} {}".format(start_time, end_time, rest_start_time, rest_end_time)
        f.write(timestamp)

def load_time_stamp():
    # 今日の日付のタイムスタンプを読み出し
    today_stamp = str(datetime.date.today())
    file_path = os.path.join(TIMESTAMP_PATH, today_stamp + ".txt")
    with open(file_path, "r") as f:
        timestamp = f.readlines()[0].split()
        print(timestamp)
    
    return timestamp

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('state', help='start or end')
    parser.add_argument('-s', '--start_time', help='勤務開始時間', default=None)
    parser.add_argument('-e', '--end_time', help='勤務終了時間', default=None)
    parser.add_argument('-rs', '--rest_start_time', help='休憩開始時間', default=None)
    parser.add_argument('-re', '--rest_end_time', help='休憩終了時間', default=None)

    args = parser.parse_args()

    to_addr = TO_ADDRESS
    
    # 開始報告
    if args.state == "start":
        # 休憩あり
        if args.rest_start_time is not None:
            body = '音響・音声データ解析，プログラミング等の業務を{}から{}まで行います．途中休憩は{}から{}まで取る予定です．'.format(args.start_time, 
                                                args.end_time, 
                                                args.rest_start_time, 
                                                args.rest_end_time)
        # 休憩なし
        else:
            body = '音響・音声データ解析，プログラミング等の業務を{}から{}まで行います．途中休憩は取る予定はありません．'.format(args.start_time,
                                                args.end_time)

        subject = SUBJECT_START
        write_time_stamp(args.start_time, args.end_time, args.rest_start_time, args.rest_end_time)
    # 終了報告
    else:
        start_time, end_time, start_rest_time, end_rest_time = load_time_stamp()
        if start_rest_time == "None":
            body = '音響・音声データ解析，プログラミング等の業務を{}から{}まで行いました．途中休憩はありませんでした．'.format(start_time, end_time)
        else:
            body = '音響・音声データ解析，プログラミング等の業務を{}から{}まで行いました．途中休憩は{}から{}まで取りました．'.format(start_time, end_time, start_rest_time, end_rest_time)
        subject = SUBJECT_END

    msg = create_message(FROM_ADDRESS, to_addr, CC, BCC, subject, body)
    send(FROM_ADDRESS, to_addr, msg)
    print("Finish sending !!!")