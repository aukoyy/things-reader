import os
from datetime import datetime
from send_things3_todos import send_things3_todos
import things
# /Users/aukoyy/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-N5H2G/Things Database.thingsdatabase
# https://github.com/thingsapi/things.py
# https://github.com/thingsapi/things-cli


todos = things.todos()
print("\nAll available attributes in a todo:")
for key in todos[1].keys():
    print(f"{key}: {todos[1][key]}")
print("\n")

#for todo in todos:
#    print(f"Title: {todo['title']}, Start: {todo.get('start', 'Not set')}")

# TODO: sort todos into inbox, today, anytime, someday and areas
# area = start=Anytime & area_title

print('Today date:', datetime.today().strftime('%Y-%m-%d'))
today_tasks = []
areas = {}
for todo in todos:
    if todo['start_date'] == datetime.today().strftime('%Y-%m-%d'):
        today_tasks.append(todo)
        todos.remove(todo)
    if todo.get('area_title'):
        if todo['area_title'] not in areas:
            areas[todo['area_title']] = []
        areas[todo['area_title']].append(todo)
            
        

print("Today's tasks:")
print("\n".join([todo['title'] for todo in today_tasks]))

print("\nAreas and their tasks:")
for area, tasks in areas.items():
    print(f"\n{area}:")
    for task in tasks:
        print(f"  - {task['title']}")

# Ensure the directory exists before creating the file
output_dir = '/Users/aukoyy/Library/Mobile Documents/com~apple~CloudDocs'
os.makedirs(output_dir, exist_ok=True)



# Convert output_lines to a single string with line breaks
# email_body = "\n\n" + "\n".join(output_lines) + "\n\n"

# send_things3_todos(email_body)

