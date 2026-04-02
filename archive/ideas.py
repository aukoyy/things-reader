# /Users/aukoyy/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-N5H2G/Things Database.thingsdatabase
# https://github.com/thingsapi/things.py
# https://github.com/thingsapi/things-cli

import sqlite3
import os
from collections import defaultdict
from send_things3_todos import send_things3_todos
import things


todos = things.todos()
print(todos[0])

db_path = '/Users/aukoyy/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-N5H2G/Things Database.thingsdatabase/main.sqlite'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Get all todos with their area and list info
cursor.execute("""
    SELECT 
        t.title,
        t.notes,
        t.start,
        t.deadline,
        CASE
            WHEN t.start = 1 THEN 'Today'
            WHEN t.start = 2 THEN 'Upcoming'
            WHEN t.start = 0 AND t.area IS NULL THEN 'Inbox'
            WHEN t.start = 0 AND t.area IS NOT NULL THEN 'Anytime'
            ELSE 'Someday'
        END as list_name,
        COALESCE(a.title, '') as area_name
    FROM TMTask t
    LEFT JOIN TMArea a ON t.area = a.uuid
    WHERE t.status = 0 AND t.trashed = 0
    ORDER BY list_name, area_name, t.title
""")
todos = cursor.fetchall()

# Get column names
cursor.execute("PRAGMA table_info(TMTask)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

# Get all todos with column names
cursor.execute("""
    SELECT * FROM TMTask WHERE status = 0 AND trashed = 0
""")
all_todos = cursor.fetchall()

# Create list of dicts with column names as keys
todos_with_fields = []
for todo in all_todos:
    todo_dict = dict(zip(column_names, todo))
    todos_with_fields.append(todo_dict)

print("Todos with field names:")
""" for todo in todos_with_fields:
    print(todo) """



# Group todos by list and area
grouped_todos = defaultdict(lambda: defaultdict(list))
for todo in todos:
    title, notes, start, deadline, list_name, area_name = todo
    if area_name and list_name == 'Anytime':
        grouped_todos[area_name][''].append((title, notes, deadline))
    else:
        grouped_todos[list_name][''].append((title, notes, deadline))

# Ensure the directory exists before creating the file
output_dir = '/Users/aukoyy/Library/Mobile Documents/com~apple~CloudDocs'
os.makedirs(output_dir, exist_ok=True)

output_lines = []

    # Process standard lists first in specific order
list_order = ['Inbox', 'Today', 'Upcoming', 'Anytime', 'Someday']
    
for list_name in list_order:
    if list_name in grouped_todos:
        output_lines.append(f"\n=== {list_name} ===")
        for area_name, todos in grouped_todos[list_name].items():
            if area_name:
                output_lines.append(f"\n--- {area_name} ---")
            for title, notes, deadline in todos:
                output = title
                if notes:
                    output += f" (Notes: {notes})"
                if deadline:
                    output += f" (Deadline: {deadline})"
                output_lines.append(output)
    
# Process areas (which are separate from standard lists)
for area_name in sorted(grouped_todos.keys()):
    if area_name not in list_order:
        output_lines.append(f"\n=== {area_name} ===")
        for _, todos in grouped_todos[area_name].items():
            for title, notes, deadline in todos:
                output = title
                if notes:
                    output += f" (Notes: {notes})"
                if deadline:
                    output += f" (Deadline: {deadline})"
                output_lines.append(output)

    # Write to file and print
    #for line in output_lines:
    #    print(line)
    #    f.write(line + '\n')

#with open(os.path.join(output_dir, 'things_todo.txt'), 'w') as f:
# print("\n".join(output_lines))

# Convert output_lines to a single string with line breaks
# email_body = "\n".join(output_lines)

# Import and use the email sending function

# send_things3_todos(email_body)

connection.close()
