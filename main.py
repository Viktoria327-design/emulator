import tkinter as tk
from tkinter import scrolledtext
import socket
import getpass
import shlex
import argparse
import os
import sys
import time


class ShellEmulator:

    def __init__(self, root, vfs_path=None, script_path=None):
        self.root = root
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.vfs_path = vfs_path
        self.script_path = script_path

        self.root.title(f"Эмулятор - [{self.username}@{self.hostname}]")
        self.root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, bg="black", fg="white",
            font=("Consolas", 11), insertbackground="white"
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output.configure(state=tk.DISABLED)

        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.prompt_label = tk.Label(
            input_frame, text=f"{self.username}@{self.hostname}:~$ ",
            font=("Consolas", 11), fg="green"
        )
        self.prompt_label.pack(side=tk.LEFT)

        self.command_entry = tk.Entry(
            input_frame, font=("Consolas", 11), bg="black", fg="white",
            insertbackground="white"
        )
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.command_entry.bind("<Return>", self.on_enter)
        self.command_entry.focus_set()

        self.print_line("Эмулятор оболочки запущен.")
        self.print_line(f"Пользователь: {self.username}@{self.hostname}")
        self.print_line(f"VFS: {self.vfs_path}")
        self.print_line(f"Стартовый скрипт: {self.script_path}")
        self.print_line("Введите 'exit' для выхода.")
        self.print_line("")

        if self.script_path:
            self.run_script(self.script_path)

    def print_line(self, text=""):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def on_enter(self, event):
        line = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.print_line(f"{self.username}@{self.hostname}:~$ {line}")
        self.execute(line)

    def parse(self, line):
        try:
            tokens = shlex.split(line)
            return tokens
        except ValueError as e:
            self.print_line(f"Ошибка парсинга: {e}")
            return None

    def execute(self, line):
        line = line.strip()
        if not line:
            return

        tokens = self.parse(line)
        if tokens is None:
            return
        if not tokens:
            return

        command = tokens[0]
        args = tokens[1:]

        if command == "ls":
            self.cmd_ls(args)
        elif command == "cd":
            self.cmd_cd(args)
        elif command == "exit":
            self.cmd_exit(args)
        else:
            self.print_line(f"{command}: команда не найдена")

    def cmd_ls(self, args):
        self.print_line("ls: команда вызвана")
        self.print_line(f"  аргументы: {args}")

    def cmd_cd(self, args):
        self.print_line("cd: команда вызвана")
        self.print_line(f"  аргументы: {args}")

    def cmd_exit(self, args):
        self.print_line("Завершение работы эмулятора...")
        self.root.after(300, self.root.destroy)

    def run_script(self, path):
        if not os.path.exists(path):
            self.print_line(f"Ошибка: скрипт не найден: {path}")
            return

        self.print_line(f"Выполнение скрипта: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            self.print_line(f"Ошибка чтения скрипта: {e}")
            return

        for line in lines:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if line.strip().startswith("#"):
                continue
            self.print_line(f"{self.username}@{self.hostname}:~$ {line}")
            self.execute(line)
            self.root.update()
            time.sleep(0.15)
        self.print_line("Скрипт завершён")
        self.print_line("")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Эмулятор командной строки UNIX-подобной ОС"
    )
    parser.add_argument("--vfs", type=str, default=None,
                        help="Путь к физическому расположению VFS")
    parser.add_argument("--script", type=str, default=None,
                        help="Путь к стартовому скрипту")
    return parser.parse_args()


def main():
    args = parse_args()

    print("Отладочный вывод параметров")
    print(f"VFS: {args.vfs}")
    print(f"Script: {args.script}")

    root = tk.Tk()
    app = ShellEmulator(root, vfs_path=args.vfs, script_path=args.script)
    root.mainloop()


if __name__ == "__main__":
    main()