from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.style import Style

# Purple theme configuration
PURPLE_THEME = {
    "primary": Style(color="bright_magenta", bold=True),
    "secondary": Style(color="purple4"),
    "accent": Style(color="medium_purple"),
    "success": Style(color="green"),
    "error": Style(color="red")
}

class TaskTracker:
    """Main application class for the Task Tracker"""
    
    def __init__(self):
        self.tasks = []
        self.console = Console()
        self.running = True
        
    def run(self):
        """Main application loop"""
        try:
            while self.running:
                self.display_menu()
        except KeyboardInterrupt:
            self.console.print("\n[purple]Goodbye![/]")
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/]")

    def display_menu(self):
        """Display the main menu and handle user input"""
        self.console.clear()
        self.console.print(Panel("[bold]TASK TRACKER[/]", style=PURPLE_THEME["primary"]))
        
        # Create menu options
        menu_table = Table.grid(padding=(0, 2))
        menu_table.add_row("1", "View Tasks")
        menu_table.add_row("2", "Add New Task")
        menu_table.add_row("3", "Mark Task Complete")
        menu_table.add_row("4", "Exit")
        
        self.console.print(menu_table, style=PURPLE_THEME["accent"])
        
        # Get user choice with validation
        choice = Prompt.ask("\n[purple]Select an option[/]", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            self.view_tasks()
        elif choice == "2":
            self.add_task()
        elif choice == "3":
            self.mark_complete()
        elif choice == "4":
            self.running = False
            self.console.print("[purple]Goodbye![/]")

    def view_tasks(self):
        """Display all tasks in a formatted table"""
        self.console.clear()
        self.console.print(Panel("[bold]TASK LIST[/]", style=PURPLE_THEME["primary"]))
        
        if not self.tasks:
            self.console.print("[italic]No tasks found[/]\n", style=PURPLE_THEME["secondary"])
            Prompt.ask("[bold]Press Enter to continue[/]", default="")
            return
        
        # Create tasks table
        table = Table(show_header=True, header_style=PURPLE_THEME["primary"])
        table.add_column("ID", width=4)
        table.add_column("Task", style=PURPLE_THEME["accent"])
        table.add_column("Status", justify="center")
        
        for i, task in enumerate(self.tasks, 1):
            status = "✅" if task["completed"] else "❌"
            table.add_row(str(i), task["description"], status)
        
        self.console.print(table)
        Prompt.ask("\n[bold]Press Enter to continue[/]", default="")

    def add_task(self):
        """Add a new task to the tracker"""
        self.console.clear()
        self.console.print(Panel("[bold]ADD NEW TASK[/]", style=PURPLE_THEME["primary"]))
        
        # Get task description with validation
        description = Prompt.ask("\n[purple]Enter task description[/]")
        if not description.strip():
            self.console.print("[red]Error: Task description cannot be empty![/]")
            Prompt.ask("\n[bold]Press Enter to continue[/]", default="")
            return
            
        self.tasks.append({"description": description, "completed": False})
        self.console.print(f"\n[green]✓ Added:[/] {description}")
        Prompt.ask("\n[bold]Press Enter to continue[/]", default="")

    def mark_complete(self):
        """Mark a task as completed"""
        self.console.clear()
        self.console.print(Panel("[bold]MARK TASK COMPLETE[/]", style=PURPLE_THEME["primary"]))
        
        if not self.tasks:
            self.console.print("[italic]No tasks to mark as complete[/]\n", style=PURPLE_THEME["secondary"])
            Prompt.ask("[bold]Press Enter to continue[/]", default="")
            return
        
        self.view_tasks()
        
        # Get task ID with validation
        try:
            task_id = IntPrompt.ask(
                "\n[purple]Enter task ID to mark complete[/]",
                show_choices=False,
                show_default=False
            )
            
            if task_id < 1 or task_id > len(self.tasks):
                raise ValueError("Invalid task ID")
                
            if self.tasks[task_id-1]["completed"]:
                self.console.print(f"[yellow]⚠ Task {task_id} is already completed![/]")
            else:
                self.tasks[task_id-1]["completed"] = True
                self.console.print(f"\n[green]✓ Marked task {task_id} as complete![/]")
                
        except ValueError:
            self.console.print(f"[red]Error: Please enter a valid task ID (1-{len(self.tasks)})[/]")
        
        Prompt.ask("\n[bold]Press Enter to continue[/]", default="")

if __name__ == "__main__":
    app = TaskTracker()
    app.run()