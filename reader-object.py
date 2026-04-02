import os
from send_things3_todos import send_things3_todos
import things
from datetime import datetime

# /Users/aukoyy/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-N5H2G/Things Database.thingsdatabase
# https://github.com/thingsapi/things.py
# https://github.com/thingsapi/things-cli


def get_things_todos():
    """Get all Things3 todos organized by category and return as formatted string"""
    todos = things.todos()
    output = {}

    for todo in things.inbox():
        output['inbox'] = output.get('inbox', []) + [todo['title']]

    today_tasks = things.today()
    for todo in today_tasks:
        output['today'] = output.get('today', []) + [todo['title']]

    upcoming_todos = things.upcoming()
    upcoming_todos.sort(key=lambda todo: todo.get('start_date', ''))  
    today = datetime.now().date()
    for todo in upcoming_todos:
        start_date = datetime.fromisoformat(todo['start_date']).date()
        days_until = (start_date - today).days
        if days_until <= 7:
            weekday = start_date.strftime('%A')
            time_label = f"[{weekday}]"
        else:
            time_label = f"[{days_until}d]"
        output['upcoming'] = output.get('upcoming', []) + [f"{time_label} {todo['title']}"]

    for todo in things.anytime():
        if not todo.get('project_title'):
            # Only add if not already in today
            today_titles = set(output.get('today', []))
            if todo['title'] not in today_titles:
                output['anytime'] = output.get('anytime', []) + [todo['title']]

    for todo in things.someday():
        output['someday'] = output.get('someday', []) + [todo['title']]
    
    return to_string(output)

def to_string(output):
    output_string = ''
    if 'inbox' in output:
        output_string += '=== INBOX ===\n'
        for title in output['inbox']:
            output_string += "[  ] " + title + "\n"
    if 'today' in output:
        output_string += '\n=== TODAY ===\n'
        for title in output['today']:
            output_string += "[  ] " + title + "\n"
    if 'upcoming' in output:
        output_string += '\n=== UPCOMING ===\n'
        for title in output['upcoming']:
            output_string += "[  ] " + title + "\n"
    if 'anytime' in output:
        output_string += '\n=== ANYTIME ===\n'
        for title in output['anytime']:
            output_string += "[  ] " + title + "\n"
    if 'someday' in output:
        output_string += '\n=== SOMEDAY ===\n'
        for title in output['someday']:
            output_string += "[  ] " + title + "\n"
    return output_string

if __name__ == "__main__":
    todos_text = get_things_todos()
    print(todos_text)
    send_things3_todos(todos_text)
