import os
from send_things3_todos import send_things3_todos
import things
from datetime import datetime

# /Users/aukoyy/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-N5H2G/Things Database.thingsdatabase
# https://github.com/thingsapi/things.py
# https://github.com/thingsapi/things-cli


todos = things.todos()
print("\nAll available attributes in a todo:")
for key in todos[1].keys():
    print(f"{key}: {todos[1][key]}")
print("\n")



output_string = ''

output_string += '=== INBOX ===\n'
for todo in things.inbox():
    output_string += " - " + todo['title'] + "\n"

today_tasks = things.today()
output_string += '\n=== TODAY ===\n'
for todo in today_tasks:
    output_string += " - " + todo['title'] + "\n"

upcoming_todos = things.upcoming()
upcoming_todos.sort(key=lambda todo: todo.get('start_date', ''))  
output_string += '\n=== UPCOMING ===\n'
today = datetime.now().date()
for todo in upcoming_todos:
    start_date = datetime.fromisoformat(todo['start_date']).date()
    days_until = (start_date - today).days
    time_label = f"[{days_until}d]"
    output_string += f" - {time_label} {todo['title']}\n"

output_string += '\n=== ANYTIME ===\nskipping projects\n'
for todo in things.anytime():
    if not todo.get('project_title'):
      output_string += " - "
      output_string += todo['title'] + '\n'
      

output_string += '\n=== AREAS ===\n'
output_string += 'Not implemented yet'
# print(things.areas())
        

print('Output: ')
print(output_string)



# Ensure the directory exists before creating the file
output_dir = '/Users/aukoyy/Library/Mobile Documents/com~apple~CloudDocs'
output_dir2 = '/Users/aukoyy/My Drive'
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, 'things_todo.txt'), 'w') as f:
    f.write(output_string)

# does not work
with open(os.path.join(output_dir2, 'things_todo.txt'), 'w') as f:
    f.write(output_string)

# Convert output_lines to a single string with line breaks
email_body = "\n\n" + output_string + "\n\n"
send_things3_todos(email_body)

