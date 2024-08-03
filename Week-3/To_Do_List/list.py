tasks = []

def addTask(taskName):
    Task = {"description": taskName, "complete": False}
    tasks.append(Task)
    print(f"\nAdded task: '{taskName}'")

def deleteTask(task):
    if 0 <= task < len(tasks):
        deleteTask = tasks.pop(task)
        print(f"\nDeleted task: '{deleteTask['description']}'")
    else:
        print(f"\nTask number {task} not found.")

def viewTasks():
    if not tasks:
        print("\nNo tasks to display.")
    else:
        for idx, Task in enumerate(tasks):
            status = "Complete" if Task["complete"] else "Incomplete"
            print(f"\n{idx + 1}. Task: '{Task['description']}' - Status: {status}")

def markAsComplete(task):
    if 0 <= task < len(tasks):
        tasks[task]["complete"] = True
        print(f"\nMarked task as complete: '{tasks[task]['description']}'")
    else:
        print(f"\nTask number {task} not found.")

def main():
    while True:
        print("\nTo-Do List Application")
        print("1. Add a task")
        print("2. Display tasks")
        print("3. Mark task as complete")
        print("4. Delete a task")
        print("5. Exit")
        choice = input("\nChoose an option (1-5): ")

        if choice == '1':
            taskName = input("\nEnter the task: ")
            addTask(taskName)
        elif choice == '2':
            viewTasks()
        elif choice == '3':
            viewTasks() 
            task = int(input("\nEnter the task number to mark as complete: ")) - 1
            markAsComplete(task)
        elif choice == '4':
            viewTasks()
            task = int(input("\nEnter the task number to delete: ")) - 1
            deleteTask(task)
        elif choice == '5':
            print("Exiting the application.......")
            break
        else:
            print("\nInvalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()