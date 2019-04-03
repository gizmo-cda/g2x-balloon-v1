# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
os.chdir(r'C:\programming\sources\g2x-balloon-v1')

import importlib
import socketserver
import kmlgps; importlib.reload(kmlgps)
import rest_server; importlib.reload(rest_server)
import relpos as _relpos; importlib.reload(_relpos)

kmlgps.GizmoHq.altitude_above_ground_m
kml_bytes = kmlgps.GizmoHq.kml_gizmo_hq().encode()
#tgps = kmlgps.TwoGps()

#print(tgps.gen_kml_byte_str())

south_east_lon = _relpos.LatLonDHMS(deg=116, minute=47, second=44.21, hemisphere='W')
# south_east_lon.conv_deghms_2_radians() * 180 / 3.14

if True:
    PORT = 8000
    with socketserver.TCPServer(
                # server_address=("127.0.0.1", PORT),
                server_address=("", PORT),
                RequestHandlerClass=rest_server.StoreHandler,
                # directory=TWO_GPS.state_dir,
            ) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever(poll_interval=0.5)
