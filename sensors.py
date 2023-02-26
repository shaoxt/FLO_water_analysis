#!/usr/bin/python3

import os
import mysql.connector
from urllib.parse import urlparse, parse_qs

from http.server import BaseHTTPRequestHandler, HTTPServer


def insert_value(cnx, sensor_name, value):
   cursor = cnx.cursor()

   sql = ("INSERT INTO sensor_data (date_created, value, sensor) VALUES (CURRENT_TIMESTAMP(6), %(value)s, %(sensor)s)")

   values = {'value': value, 'sensor': sensor_name}

   # Insert new values
   cursor.execute(sql, values)

   # Make sure data is committed to the database
   cnx.commit()

   cursor.close()


class SensorServer(BaseHTTPRequestHandler):
    def do_POST(self):
        # first we need to parse it
        parsed = urlparse(self.path)
        # get the request path, this new path does not have the query string
        path = parsed.path

        if path == "/api/v1/sensor":

            query_components = parse_qs(urlparse(self.path).query)
            sensor_name = query_components["sensor"]
            value = query_components["value"]

            if len(sensor_name[0]) == 0:
                self.send_response(415)
                self.send_header("Content-type", "text/json")
                self.end_headers()
                self.wfile.write(bytes( "{\"code\": 415, \"message\":\"no label\"}","utf-8"))
            else:
                cnx = mysql.connector.MySQLConnection(user='root', password=os.getenv('MYSQL_PASSWORD', None),
                                                      host='127.0.0.1',
                                                      database='FLO_water')


                insert_value(cnx, sensor_name[0], int(value[0]))

                self.send_response(200)
                self.send_header("Content-type", "text/json")
                self.end_headers()

                self.wfile.write(bytes("{\"code\": 200,\"message\": \"OK\"}", "utf-8"))


if __name__ == '__main__':
    webServer = HTTPServer(("0.0.0.0", 8082), SensorServer)
    print("Server started http://%s:%s" % ("0.0.0.0", 8082))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
