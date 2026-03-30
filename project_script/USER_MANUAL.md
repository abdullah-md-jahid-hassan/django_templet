# Project Prompts Automation Toolkit - User Manual

This manual provides a comprehensive guide on how to use the `prsc` (Project Script) CLI tool, including a list of all available commands, their variations, and instructions on how to extend the toolkit by adding new customized commands.

## Available Commands

The CLI tool is invoked using the entry point `prsc.py` followed by the specific command. You can always run the tool with `--help` to see available options:

```bash
python prsc.py --help
```

### 1. `copy_env`
This command is used to safely copy environment variables from a source `.env` file to a destination file. By default, it will **only copy the keys** (variable names) up to the `=` sign and exclude the actual values, ensuring that no sensitive credentials are leaked.

#### Usage Syntax:
```bash
python prsc.py copy_env [-h] [--with-values] source destination
```

#### Positional Arguments:
- `source`: The path to the source `.env` file (e.g., `./.env.example`).
- `destination`: The path to the destination file where the output will be written (e.g., `./.env`).

#### Variations and Options:
- **Default (Keys Only):**
  Copies only the variable keys.
  *(Example: `DB_PASSWORD=secret` becomes `DB_PASSWORD=`)*
  ```bash
  python prsc.py copy_env ./.env.example ./.env
  ```
- **Copy with Values (`--with-values`):**
  Copies both the keys and their exact values, preserving formatting and comments. 
  ```bash
  python prsc.py copy_env ./.env.example ./.env --with-values
  ```
- **Help (`-h` or `--help`):**
  Shows help information specifically for the `copy_env` command.
  ```bash
  python prsc.py copy_env --help
  ```

---

## How to Add a New Command

The `prsc` CLI is designed to be highly modular and extensible. It employs a dynamic discovery system, meaning you **do not** need to modify any core files like `main.py` or `prsc.py` to add new functionality.

To add a new command, you simply create a new Python script inside the `cli/commands/` directory.

### Step-by-Step Guide

1. **Navigate to the Commands Directory:**
   Go to the `cli/commands/` folder located inside `project_script`.

2. **Create a New Python File:**
   Create a file named according to your command's purpose, for example, `my_custom_task.py`. The file name does not dictate the command name, but it should be descriptive.

3. **Define Your Command Logic:**
   Open the new file and follow this structural template to register your command and define its behavior.

   ```python
   # cli/commands/my_custom_task.py
   import argparse
   
   # 1. Define the Handler Function
   # This function executes the core logic when your command is run.
   def handle_my_custom_task(args: argparse.Namespace) -> None:
       """
       Handler function for my_custom_task.
       Access parsed arguments via the 'args' object.
       """
       print(f"Executing my custom task for target: {args.target}")
       
       # Use utilities if needed:
       # from utilities.system_utils import detect_os
       # print(f"Running on OS: {detect_os()}")

   # 2. Register the Command
   # The dynamic loader will automatically call this function.
   def register_command(subparsers: argparse._SubParsersAction) -> None:
       """
       Registers this specific command with the main CLI engine.
       """
       
       # The first argument "run_task" is the actual command name users will type
       parser = subparsers.add_parser(
           "run_task", 
           help="A brief description of what run_task does."
       )
       
       # Add expected arguments and options
       parser.add_argument(
           "target",
           type=str,
           help="The main target to run the task against."
       )
       
       # Optional flags
       parser.add_argument(
           "-v", "--verbose",
           action="store_true",
           help="Enable verbose output mode."
       )
       
       # Map your custom handler function to be triggered by this parser
       parser.set_defaults(func=handle_my_custom_task)
   ```

4. **Test Your New Command:**
   Now, navigate back to the root `project_script` directory where `prsc.py` lives. When you run the help command, the CLI will automatically detect and list your new command:

   ```bash
   python prsc.py --help
   ```

   You can then run your script using the command name defined in your parser (e.g., `run_task`):

   ```bash
   python prsc.py run_task my_example_target --verbose
   ```

### Utilizing Core Utilities
When building the logic for your handlers, it is highly recommended to leverage the existing helper functions in the `utilities/` folder to ensure cross-platform compatibility and secure execution:
- `utilities.system_utils`: functions like `detect_os()`, `is_windows()`, `is_linux()`.
- `utilities.file_utils`: File manipulation functions safely handling encodings and read/write loops.
- `utilities.command_utils`: Shell execution functions (`run_command`) designed for robust cross-platform terminal processing.
