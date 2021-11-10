#!/usr/bin/env python3
from ics import Calendar, Event
from ics.parse import ContentLine
import os
import re

input_dir = "../yearly_ics/"
output_dir = "../working/output_ics/"

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

def parse_filename(filename):
    parts = filename.split("_")
    federal_state = parts[0]
    year = parts[1].split(".")[0]
    return federal_state, year

def generate_empty_calender(name, refresh_interval):
    c = Calendar(creator="ics.tools Combinder v1.0")
    c.extra.append(ContentLine(name='NAME', value=name))
    c.extra.append(ContentLine(name='X-WR-CALNAME', value=name))
    c.extra.append(ContentLine(name='REFRESH-INTERVAL', value="VALUE=DURATION:" + refresh_interval))
    c.extra.append(ContentLine(name='X-PUBLISHED-TTL', value="VALUE=DURATION:" + refresh_interval))
    c.extra.append(ContentLine(name='METHOD', value="PUBLISH"))
    return c

states_map = {}

files = os.listdir(input_dir)
files.sort()

for file in files:
    if not file.endswith(".ics"):
        continue
    federal_state, year = parse_filename(file)
    if not federal_state in states_map:
        states_map[federal_state] = generate_empty_calender(re.sub("(^|[-])\s*([a-zA-Z])", lambda p: p.group(0).upper(), federal_state) + " Schulferien", "P1W")
    with open(input_dir + "/" + file, "r") as file1:
        l = file1.read()
    calendar = Calendar(l)
    for event in calendar.events:
        states_map[federal_state].events.add(event)

# write ics fiel for each federal state
for federal_state in states_map:
    with open(output_dir + "/" + federal_state + ".ics", 'w') as file:
        file.writelines(str(states_map[federal_state]))

# write a ics file with all federal states
c = generate_empty_calender("Schulferien deutschlandweit", "P1W")
for federal_state in states_map:
    for event in states_map[federal_state].events:
        c.events.add(event)
with open(output_dir + "/" + "alle.ics", 'w') as file:
    file.writelines(str(c))