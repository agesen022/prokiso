# Flask Setup
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
from flask import Flask, jsonify, request, abort
import json
import collections as cl
app = Flask(__name__)

credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
workbook = client.open("新歓スケジュール")
gsheet = client.open("新歓スケジュール").sheet1


def make_json():
    name_list = gsheet.col_values(2)
    pre_start_list = gsheet.col_values(3)
    start_list = []

    for i in range(0, len(pre_start_list)):
        start_list.append(pre_start_list[i].replace(
            "/", "-").replace(" ", "T"))
        if (len(start_list[i]) != 19):
            start_list[i] = start_list[i][:11]+"0"+start_list[i][11:]

    ys = []
    for i in range(1, len(name_list)):
        data = cl.OrderedDict()
        data["title"] = name_list[i]
        data["start"] = start_list[i]
        ys.append(data)

    fw = open('./events.json', 'w')
    json.dump(ys, fw, indent=4)


if __name__ == '__main__':
    make_json()
