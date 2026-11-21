from functools import reduce

# Кортеж статусів
STATUSES = ("New", "In Progress", "Completed")

# Список проектів
projects = ["Website", "Mobile App", "Database"]

# Список виконавців + посада
executors = {
    "Olena": "Developer",
    "Ivan": "Tester",
    "Maria": "Designer",
    "Petro": "Developer",
}

# Список завдань
tasks = [
    {"id": 1, "title": "Main page layout", "project": "Website",
     "assignee": "Maria", "priority": 2, "hours": 8, "status": "Completed"},
    {"id": 2, "title": "Page layout", "project": "Website",
     "assignee": "Olena", "priority": 3, "hours": 12, "status": "In Progress"},
    {"id": 3, "title": "Login form testing", "project": "Website",
     "assignee": "Ivan", "priority": 4, "hours": 5, "status": "New"},
    {"id": 4, "title": "Authorization screen", "project": "Mobile App",
     "assignee": "Olena", "priority": 5, "hours": 10, "status": "In Progress"},
    {"id": 5, "title": "Application icons", "project": "Mobile App",
     "assignee": "Maria", "priority": 1, "hours": 6, "status": "New"},
    {"id": 6, "title": "Table schema", "project": "Database",
     "assignee": "Petro", "priority": 5, "hours": 15, "status": "Completed"},
    {"id": 7, "title": "Query optimization", "project": "Database",
     "assignee": "Petro", "priority": 3, "hours": 9, "status": "New"},
]


# Допоміжні функції
def print_tasks(task_list):
    """Виводить список завдань у вигляді таблиці."""
    if not task_list:
        print("No tasks found.")
        return
    print(f"{'ID':<4}{'Title':<26}{'Project':<19}{'Assignee':<12}"
          f"{'Priority':<8}{'Hours':<6}{'Status'}")
    print("-" * 85)
    for t in task_list:
        print(f"{t['id']:<4}{t['title']:<26}{t['project']:<19}{t['assignee']:<12}"
              f"{t['priority']:<8}{t['hours']:<6}{t['status']}")


def input_int(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Please enter an integer.")


def choose_from(options, text):
    """Просить обрати значення (проекти, виконавці, статуси)."""
    options = list(options)
    while True:
        value = input(f"{text} {options}: ").strip()
        if value in options:
            return value
        print("Invalid option. Please try again.")


def find_task(task_id):
    """Повертає завдання за id або None."""
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None

def add_task():
    # Новий id = максимальний існуючий + 1
    new_id = max((t["id"] for t in tasks), default=0) + 1
    title = input("Task title: ").strip()
    project = choose_from(projects, "Project")
    assignee = choose_from(executors, "Assignee")
    priority = input_int("Priority (1-5): ")
    hours = input_int("Estimated hours: ")
    tasks.append({"id": new_id, "title": title, "project": project,
                  "assignee": assignee, "priority": priority,
                  "hours": hours, "status": "New"})
    print(f"Task #{new_id} added.")


def delete_task():
    task = find_task(input_int("Enter task ID to delete: "))
    if task:
        tasks.remove(task)
        print("Task deleted.")
    else:
        print("Task with this ID was not found.")


def update_task():
    task = find_task(input_int("Enter task ID to update: "))
    if not task:
        print("Task with this ID was not found.")
        return
    print("What do you want to update? 1 - status, 2 - assignee, 3 - hours")
    choice = input("Your choice: ")
    if choice == "1":
        task["status"] = choose_from(STATUSES, "New status")
    elif choice == "2":
        task["assignee"] = choose_from(executors, "New assignee")
    elif choice == "3":
        task["hours"] = input_int("New number of hours: ")
    else:
        print("Invalid choice.")
        return
    print("Task updated.")


# Пошук і фільтрація
def search_by_title():
    word = input("Enter a word to search: ").lower()
    result = [t for t in tasks if word in t["title"].lower()]
    print_tasks(result)


def filter_tasks():
    print("Filter: 1 - by status, 2 - by assignee, 3 - by project")
    choice = input("Your choice: ")
    if choice == "1":
        value = choose_from(STATUSES, "Status")
        key = "status"
    elif choice == "2":
        value = choose_from(executors, "Assignee")
        key = "assignee"
    elif choice == "3":
        value = choose_from(projects, "Project")
        key = "project"
    else:
        print("Invalid choice.")
        return
    # filter() залишає лише завдання, що відповідають умові
    result = list(filter(lambda t: t[key] == value, tasks))
    print_tasks(result)


# Статистика, групування, агрегація
def show_statistics():
    if not tasks:
        print("No data.")
        return
    hours_list = [t["hours"] for t in tasks]
    print(f"Number of tasks: {len(tasks)}")
    print(f"Average duration: {sum(hours_list) / len(hours_list):.1f} hours")
    longest = max(tasks, key=lambda t: t["hours"])
    shortest = min(tasks, key=lambda t: t["hours"])
    print(f"Longest task: {longest['title']} ({longest['hours']} hours)")
    print(f"Shortest task: {shortest['title']} ({shortest['hours']} hours)")


def group_by(key):
    """Групує завдання за ключем у словник."""
    groups = {}
    for t in tasks:
        groups.setdefault(t[key], []).append(t)
    return groups


def show_grouping():
    key = "project" if input("Group by: 1 - project, 2 - assignee: ") == "1" else "assignee"
    for name, group in group_by(key).items():
        total = sum(t["hours"] for t in group)
        avg_priority = sum(t["priority"] for t in group) / len(group)
        print(f"{name}: tasks - {len(group)}, hours - {total}, "
              f"average priority - {avg_priority:.1f}")


def show_functional():
    # map перетворює години у робочі дні (8 год = 1 день)
    days = list(map(lambda t: (t["title"], round(t["hours"] / 8, 1)), tasks))
    print("Duration in working days (first 3):")
    for title, d in days[:3]:
        print(f"  {title}: {d} days")

    # filter невиконані завдання
    not_done = list(filter(lambda t: t["status"] != "Completed", tasks))
    print(f"\nUncompleted tasks: {len(not_done)}")

    # reduce загальна кількість годин невиконаних завдань
    total = reduce(lambda acc, t: acc + t["hours"], not_done, 0)
    print(f"Remaining working hours: {total}")


def show_sorted():
    print("Sort by: 1 - priority, 2 - hours")
    key = "priority" if input("Your choice: ") == "1" else "hours"
    sorted_tasks = sorted(tasks, key=lambda t: t[key], reverse=True)
    print("Top 3 tasks:")
    print_tasks(sorted_tasks[:3])
    print("\nLast 2 tasks in the list:")
    print_tasks(sorted_tasks[-2:])


# Множини та словники
def assignees_of(project):
    """Множина виконавців проекту."""
    return {t["assignee"] for t in tasks if t["project"] == project}


def show_sets():
    p1 = choose_from(projects, "First project")
    p2 = choose_from(projects, "Second project")
    s1, s2 = assignees_of(p1), assignees_of(p2)
    print(f"Assignees of '{p1}': {s1}")
    print(f"Assignees of '{p2}': {s2}")
    print(f"Union (working in at least one): {s1 | s2}")
    print(f"Intersection (working in both): {s1 & s2}")
    print(f"Difference (only in '{p1}'): {s1 - s2}")
    # Виконавці, які взагалі не мають завдань
    free = set(executors) - {t["assignee"] for t in tasks}
    print(f"Assignees without tasks: {free if free else 'none'}")


def show_frequencies():
    # Словник для підрахунку статусів
    counter = {}
    for t in tasks:
        counter[t["status"]] = counter.get(t["status"], 0) + 1
    print("Number of tasks by status:")
    for status, count in counter.items():
        print(f"  {status}: {count}")

    # Словник індекс: id -- завдання
    index = {t["id"]: t for t in tasks}
    print(f"\nID index: {list(index.keys())}")
    task_id = input_int("Enter ID for quick search: ")
    if task_id in index:
        print_tasks([index[task_id]])
    else:
        print("This ID is not in the index.")


# Меню
def show_menu():
    print("\nTask Management System")
    print("1. Show all tasks")
    print("2. Add a task")
    print("3. Delete a task")
    print("4. Update a task")
    print("5. Search by title")
    print("6. Filter tasks")
    print("7. Statistics (average, min, max)")
    print("8. Grouping and aggregation")
    print("9. map / filter / reduce")
    print("10. Sorting and slicing")
    print("11. Set operations")
    print("12. Frequencies and index")
    print("0. Exit")


def main():
    actions = {
        "1": lambda: print_tasks(tasks),
        "2": add_task,
        "3": delete_task,
        "4": update_task,
        "5": search_by_title,
        "6": filter_tasks,
        "7": show_statistics,
        "8": show_grouping,
        "9": show_functional,
        "10": show_sorted,
        "11": show_sets,
        "12": show_frequencies,
    }
    while True:
        show_menu()
        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        if choice in actions:
            print()
            actions[choice]()
        else:
            print("Invalid menu option.")


if __name__ == "__main__":
    main()
