import sqlite3


# Initialize database and table if not exists
def init_db():
    conn = sqlite3.connect("./todo.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


# Add new task
def add_task(task):
    conn = sqlite3.connect("./todo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    print(f"✅ Task '{task}' added!")


# View tasks list
def view_tasks():
    conn = sqlite3.connect("./todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("📭 Tasks list is empty!")
        return

    print("\n--- Tasks List ---")
    for task in tasks:
        status = "✅" if task[2] else "❌"
        print(f"[{task[0]}] {status} {task[1]}")


# Update task status
def update_task(task_id, completed):
    conn = sqlite3.connect("./todo.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()
    print(
        f"🔄 Task #{task_id} status updated to {'completed' if completed else 'pending'}."
    )


# Delete task
def delete_task(task_id):
    conn = sqlite3.connect("./todo.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"🗑️ Task #{task_id} deleted.")


# Main menu
def main():
    init_db()
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Add new task")
        print("2. View tasks list")
        print("3. Update task status")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            task = input("Task name: ")
            add_task(task)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            task_id = int(input("Task number: "))
            completed = input("Status (1=completed, 0=pending): ")
            update_task(task_id, bool(int(completed)))
        elif choice == "4":
            task_id = int(input("Task number: "))
            delete_task(task_id)
        elif choice == "5":
            print("Exiting program...")
            break
        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()
