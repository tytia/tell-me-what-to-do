# Tell me what to do
A simple console application that tells you what to do when you're too indecisive.  
  
Tasks are structured like a file tree, where you can add subtasks inside any task.
When choosing a task, the program will only choose tasks that do not contain any subtasks (i.e. leaf tasks)

## Download
In the [latest release](https://github.com/tytia/tell-me-what-to-do/releases/tag/v1.0.0), download "Tell-me-what-to-do.zip".  
  
Alternatively, you could compile from source with PyInstaller.

## Start menu
Here you can choose to edit your tasks or change the timer length.
![start menu](readme-images/start_menu.png)

## Edit tasks
Here you can add, remove and rename your tasks.
![edit tasks](readme-images/edit_tasks.png)

## After a task is chosen
A timer will tick down, which can be cancelled by pressing Ctrl+C.
![chosen task](readme-images/chosen_task.png)
