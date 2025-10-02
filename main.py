import tkinter as tk
from tkinter import scrolledtext
import os
import socket
import sys
import argparse

# ЭТАП 1: Базовый REPL с графическим интерфейсом

def get_system_info():
    # Получение информации о системе для заголовка окна
    username = os.getlogin()
    hostname = socket.gethostname()
    return username, hostname

def parse_command(a):
    # Парсер команд и аргументов (Этап 1 - требование 3)
    if a == "exit":
        return "exit", []
    if len(a) == 0:
        return "", []
    
    b = a.split()
    return b[0], b[1:]

def execute_command_stub(cmd, args):
    # Выполнение команд-заглушек (Этап 1 - требование 4,5)
    if cmd == "ls":
        if len(args) > 0:
            return f"ls: заглушка с аргументами {args}"
        else:
            return "ls: заглушка без аргументов"
    elif cmd == "cd":
        if len(args) > 0:
            return f"cd: заглушка с аргументами {args}"
        else:
            return "cd: заглушка без аргументов"
    elif cmd == "exit":
        return "exit: завершение работы"
    else:
        return f"{cmd}: command not found" 

def act(a):
    # Основная функция обработки команд (Этап 1)
    cmd, args = parse_command(a)
    if cmd == "exit":
        exit()
    if cmd == "":
        return ""
    return execute_command_stub(cmd, args)

# ЭТАП 2: Расширенная функциональность с VFS и скриптами

def get_vfs_name(vfs_path):
    """Возвращает имя VFS из пути"""
    return os.path.basename(vfs_path) if vfs_path else "vfs"

def print_debug_info(vfs_path, script_path):
    # Отладочный вывод параметров (Этап 2 - требование 1)
    print(f"Путь к VFS: {vfs_path}")
    print(f"Путь к стартовому скрипту: {script_path}")

def execute_command_real(cmd, args, current_path):
    # Реальное выполнение команд в VFS (Этап 2)
    success = True
    output = ""
    
    if cmd == "ls":
        # Реальное выполнение ls
        try:
            items = os.listdir(current_path)
            output = "\n".join(items) if items else "Директория пуста"
        except OSError as e:
            output = f"Ошибка: {e}"
            success = False
            
    elif cmd == "cd":
        # Реальное выполнение cd
        if len(args) == 0:
            new_path = os.path.abspath("/")
        else:
            new_path = os.path.join(current_path, args[0])
            
        if os.path.exists(new_path) and os.path.isdir(new_path):
            current_path = new_path
            output = f"Текущая директория: {current_path}"
        else:
            output = f"Ошибка: директория не существует"
            success = False
            
    elif cmd == "exit":
        output = "Завершение работы"
        
    else:
        output = f"{cmd}: command not found"
        success = False
        
    return success, output, current_path

def execute_script(script_path, vfs_name, vfs_path):
    # Выполнение стартового скрипта с остановкой при ошибке (Этап 2 - требование 2)
    if not os.path.exists(script_path):
        print(f"ОШИБКА: Скрипт '{script_path}' не найден!")
        return False
    
    success = True
    current_path = vfs_path
    
    with open(script_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Имитация диалога (ввод + вывод)
            status_symbol = "√" if success else "X"
            print(f"{vfs_name} {status_symbol} > {line}")
            
            cmd, args = parse_command(line)
            
            # Реальное выполнение команды
            success, output, current_path = execute_command_real(cmd, args, current_path)
            
            # Показ вывода команды
            if output:
                print(output)
            
            # Остановка при первой ошибке
            if not success:
                print(f"Скрипт остановлен на строке {line_num} из-за ошибки")
                return False
                
    return True

def interactive_mode_cli(vfs_name, vfs_path):
    """Интерактивный режим работы в командной строке (Этап 2)"""
    success_symbol = "√"
    failure_symbol = "X"
    current_path = vfs_path
    
    while True:
        status_symbol = success_symbol
        
        inp = input(f"{vfs_name} {status_symbol} > ")
        cmd, args = parse_command(inp)
        
        print(f"{vfs_name} {status_symbol} > {inp}")
        
        if cmd == "exit":
            print("Завершение работы")
            break
            
        success, output, current_path = execute_command_real(cmd, args, current_path)
        
        if not success:
            status_symbol = failure_symbol
            
        if output:
            print(output)

# ГРАФИЧЕСКИЙ ИНТЕРФЕЙС

def process_command_gui(input_entry, output_text, event=None):
    """Обработка команд в графическом интерфейсе (Этап 1 - требование 6)"""
    a = input_entry.get().strip()
    if not a:
        return
        
    input_entry.delete(0, tk.END)
    output_text.config(state=tk.NORMAL)
    
    # Показываем введенную команду
    output_text.insert(tk.END, f'$ {a}\n')
    
    # Обрабатываем команду
    output = act(a)
    
    # Показываем результат
    if output:
        output_text.insert(tk.END, f'{output}\n')
    
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)

def create_gui():
    # Создание графического интерфейса (Этап 1 - требование 1,2)
    root = tk.Tk()
    username, hostname = get_system_info()
    root.title(f"эмулятор - [{username}@{hostname}]")

    # Основной фрейм
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Текстовое поле для вывода
    output_text = scrolledtext.ScrolledText(main_frame, height=20, width=70, font=("Courier", 10))
    output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    output_text.config(state=tk.DISABLED)

    # Начальное сообщение с примерами
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"Эмулятор командной строки - [{username}@{hostname}]\n")
    output_text.insert(tk.END, "Доступные команды: ls, cd, exit\n")
    output_text.insert(tk.END, "Пример: ls -l, cd /home, exit\n")
    output_text.insert(tk.END, "-" * 50 + "\n")
    output_text.config(state=tk.DISABLED)

    # Фрейм для ввода
    input_frame = tk.Frame(main_frame)
    input_frame.pack(fill=tk.X)

    prompt_label = tk.Label(input_frame, text="$ ", font=("Courier", 10))
    prompt_label.pack(side=tk.LEFT)

    input_entry = tk.Entry(input_frame, font=("Courier", 10))
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    # Привязка обработчика команд
    input_entry.bind('<Return>', lambda event: process_command_gui(input_entry, output_text, event))

    enter_button = tk.Button(input_frame, text="Enter", 
                           command=lambda: process_command_gui(input_entry, output_text))
    enter_button.pack(side=tk.RIGHT)

    input_entry.focus()
    return root

def run_gui_mode():
    """Запуск в режиме графического интерфейса (Этап 1)"""
    root = create_gui()
    root.mainloop()

def run_cli_mode():
    """Запуск в режиме командной строки с параметрами (Этап 2)"""
    parser = argparse.ArgumentParser(description='Эмулятор VFS')
    parser.add_argument('--vfs', required=True, help='Путь к физическому расположению VFS')
    parser.add_argument('--script', help='Путь к стартовому скрипту')
    parser.add_argument('--gui', action='store_true', help='Запуск в графическом режиме')
    
    args = parser.parse_args()
    
    if args.gui:
        run_gui_mode()
        return
    
    # Создание VFS директории
    os.makedirs(args.vfs, exist_ok=True)
    
    vfs_name = get_vfs_name(args.vfs)
    
    # Отладочный вывод параметров
    print_debug_info(args.vfs, args.script)
    
    # Выполнение стартового скрипта (если указан)
    script_success = True
    if args.script:
        script_success = execute_script(args.script, vfs_name, args.vfs)

    # Переход в интерактивный режим после успешного выполнения скрипта
    if script_success:
        interactive_mode_cli(vfs_name, args.vfs)

def run_simple_repl():
    """Простой REPL режим (для тестирования Этапа 1 в консоли)"""
    print("Простой REPL режим (Этап 1)")
    print("Доступные команды: ls, cd, exit")
    print("-" * 40)
    
    while True:
        a = input("$ ")
        result = act(a)
        if result:
            print(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Режим командной строки с параметрами (Этап 2)
        run_cli_mode()
    else:
        print("Выберите режим работы:")
        print("1 - Графический интерфейс (Этап 1)")
        print("2 - Консольный режим с параметрами (Этап 2)")
        print("3 - Простой REPL (тестирование)")
        
        choice = input("Ваш выбор (1/2/3): ").strip()
        
        if choice == "1":
            run_gui_mode()
        elif choice == "2":
            print("Использование: python script.py --vfs /path/to/vfs [--script script.sh]")
            print("Пример: python script.py --vfs ./my_vfs --script test.sh")
        elif choice == "3":
            run_simple_repl()
        else:
            print("Неверный выбор")