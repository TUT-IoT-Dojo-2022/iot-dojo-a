from flask import Flask, request, render_template, jsonify
import time
import statistics
import json
import requests
data = request.get_json(force=True)
distance = data['distance']
name = data['device']
dist_db = []
for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
dist_mode = statistics.mode(dist_db)
print("inseam: " + str(dist_mode) + "cm(" ")")
