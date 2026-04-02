import sqlite3
import os
from datetime import datetime
from send_things3_todos import send_things3_todos

# /Users/aukoyy/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-N5H2G/Things Database.thingsdatabase
# https://github.com/thingsapi/things.py
# https://github.com/thingsapi/things-cli

db_path = '/Users/aukoyy/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-N5H2G/Things Database.thingsdatabase/main.sqlite'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Get all todos
cursor.execute("SELECT title, notes, start, deadline, area, project, startDate FROM TMTask WHERE status = 0 AND trashed = 0")
todos = cursor.fetchall()

# Ensure the directory exists before creating the file
output_dir = '/Users/aukoyy/Library/Mobile Documents/com~apple~CloudDocs'
os.makedirs(output_dir, exist_ok=True)

output_lines = []
with open(os.path.join(output_dir, 'things_todo.txt'), 'w') as f:
    for todo in todos:
        output = f"[{todo[2]}] {todo[0]}"
        if todo[1]:
            output += f", Notes: {todo[1]}"
        if todo[3]:
            output += f", Deadline: {todo[3]}"
        if todo[6]:
            output += f", StartDate: {datetime.fromtimestamp(todo[6]).strftime('%Y-%m-%d')}" if todo[6] else ""
        """ if todo[4]:
            output += f", Area: {todo[4]}"
        if todo[5]:
            output += f", Project: {todo[5]}" """
        output_lines.append(output)

    for line in output_lines:
        print(line)
        f.write(line + '\n')


# Convert output_lines to a single string with line breaks
email_body = "\n\n" + "\n".join(output_lines) + "\n\n"

send_things3_todos(email_body)

connection.close()
