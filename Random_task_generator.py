import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random


class TaskGenerator:
    """Класс для управления генератором случайных задач"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Random Task Generator")
        self.root.geometry("900x700")
        self.root.minsize(800, 650)
        self.root.configure(bg="#f0f0f0")
        
        self.tasks = []
        self.history = []
        self.filename = "tasks.json"
        self.history_file = "task_history.json"
        
        # Типы задач
        self.task_types = ["Учёба", "Спорт", "Работа", "Дом", "Хобби", "Другое"]
        
        # Предопределённые задачи
        self.default_tasks = [
            {"text": "Прочитать статью по Python", "type": "Учёба"},
            {"text": "Сделать зарядку 15 минут", "type": "Спорт"},
            {"text": "Проверить рабочую почту", "type": "Работа"},
            {"text": "Убраться в комнате", "type": "Дом"},
            {"text": "Нарисовать скетч", "type": "Хобби"},
            {"text": "Выучить 10 новых слов", "type": "Учёба"},
            {"text": "Пробежать 3 км", "type": "Спорт"},
            {"text": "Составить план на неделю", "type": "Работа"},
            {"text": "Приготовить новое блюдо", "type": "Дом"},
            {"text": "Прочитать главу книги", "type": "Хобби"},
            {"text": "Посмотреть обучающее видео", "type": "Учёба"},
            {"text": "Сделать растяжку", "type": "Спорт"},
            {"text": "Обновить резюме", "type": "Работа"},
            {"text": "Полить цветы", "type": "Дом"},
            {"text": "Написать в дневник", "type": "Хобби"}
        ]
        
        self.create_widgets()
        self.load_tasks()
        self.load_history()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="🎯 Random Task Generator",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1a1a2e"
        )
        title_label.pack(pady=15)
        
        # Фрейм для генерации
        generate_frame = tk.LabelFrame(
            self.root,
            text="Генерация задачи",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        generate_frame.pack(fill="x", padx=20, pady=10)
        
        # Область отображения задачи
        self.task_display = tk.Text(
            generate_frame,
            height=4,
            width=60,
            font=("Arial", 14, "bold"),
            bg="#e3f2fd",
            fg="#1565C0",
            wrap="word",
            relief="solid",
            bd=2
        )
        self.task_display.pack(pady=10, padx=10)
        
        # Тип задачи
        self.label_type = tk.Label(
            generate_frame,
            text="Тип: —",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#666666"
        )
        self.label_type.pack(pady=5)
        
        # Кнопка генерации
        btn_generate = tk.Button(
            generate_frame,
            text="🎲 Сгенерировать задачу",
            command=self.generate_task,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2
        )
        btn_generate.pack(pady=10)
        self.create_tooltip(btn_generate, "Выбрать случайную задачу из коллекции")
        
        # Фрейм для добавления новой задачи
        add_frame = tk.LabelFrame(
            self.root,
            text="Добавить новую задачу",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        add_frame.pack(fill="x", padx=20, pady=10)
        
        # Текст задачи
        tk.Label(add_frame, text="Задача:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, sticky="ne", pady=5)
        self.entry_task = tk.Text(add_frame, width=50, height=2, font=("Arial", 10))
        self.entry_task.grid(row=0, column=1, padx=10, pady=5)
        self.create_tooltip(self.entry_task, "Введите текст задачи")
        
        # Тип задачи
        tk.Label(add_frame, text="Тип:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
        self.combo_type = ttk.Combobox(add_frame, width=25, font=("Arial", 10), 
                                       values=self.task_types, state="readonly")
        self.combo_type.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.combo_type.set("Выберите тип")
        self.create_tooltip(self.combo_type, "Выберите тип задачи")
        
        # Кнопка добавления
        btn_add = tk.Button(
            add_frame,
            text="➕ Добавить задачу",
            command=self.add_task,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        )
        btn_add.grid(row=2, column=0, columnspan=2, pady=10)
        self.create_tooltip(btn_add, "Добавить задачу в коллекцию")
        
        # Фрейм для фильтрации истории
        filter_frame = tk.LabelFrame(
            self.root,
            text="Фильтрация истории",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=10
        )
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Фильтр по типу
        tk.Label(filter_frame, text="Тип задачи:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.filter_type = ttk.Combobox(filter_frame, width=20, font=("Arial", 10),
                                        values=["Все"] + self.task_types, state="readonly")
        self.filter_type.grid(row=0, column=1, padx=5)
        self.filter_type.set("Все")
        self.create_tooltip(self.filter_type, "Фильтр по типу задачи")
        
        # Кнопки фильтрации
        btn_filter = tk.Button(
            filter_frame,
            text="🔍 Применить",
            command=self.apply_filter,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_filter.grid(row=0, column=2, padx=10)
        self.create_tooltip(btn_filter, "Применить фильтры")
        
        btn_reset = tk.Button(
            filter_frame,
            text="🔄 Сбросить",
            command=self.reset_filter,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_reset.grid(row=0, column=3, padx=10)
        self.create_tooltip(btn_reset, "Сбросить все фильтры")
        
        # История (Listbox)
        history_frame = tk.Frame(self.root, bg="#ffffff")
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(history_frame, text="📜 История сгенерированных задач:", 
                font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=5, pady=5)
        
        self.history_listbox = tk.Listbox(
            history_frame,
            font=("Arial", 10),
            bg="#f9f9f9",
            fg="#333333",
            selectbackground="#4CAF50",
            selectforeground="white",
            relief="solid",
            bd=2
        )
        self.history_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        btn_clear = tk.Button(
            btn_frame,
            text="🗑️ Очистить историю",
            command=self.clear_history,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_clear.pack(side="left", padx=5)
        self.create_tooltip(btn_clear, "Удалить всю историю")
        
        btn_save = tk.Button(
            btn_frame,
            text="💾 Сохранить",
            command=self.save_data,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_save.pack(side="left", padx=5)
        self.create_tooltip(btn_save, "Сохранить данные в JSON")
        
        # Статус бар
        self.status_label = tk.Label(
            self.root,
            text=f"Задач в коллекции: 0 | В истории: 0",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="white",
            pady=5
        )
        self.status_label.pack(fill="x", side="bottom")
    
    def create_tooltip(self, widget, text):
        """Создание подсказки для виджета"""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        tooltip.withdraw()
        
        label = tk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack()
        
        def show_tooltip(event):
            tooltip.deiconify()
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.wm_geometry(f"+{x}+{y}")
        
        def hide_tooltip(event):
            tooltip.withdraw()
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def validate_input(self, text, task_type):
        """Проверка корректности ввода"""
        
        if not text.strip():
            messagebox.showerror("Ошибка", "Введите текст задачи!")
            return False
        
        if not task_type or task_type == "Выберите тип":
            messagebox.showerror("Ошибка", "Выберите тип задачи!")
            return False
        
        return True
    
    def generate_task(self):
        """Генерация случайной задачи"""
        
        if not self.tasks:
            messagebox.showwarning("Внимание", "Коллекция пуста! Добавьте задачи.")
            return
        
        # Выбор случайной задачи
        task = random.choice(self.tasks)
        
        # Отображение
        self.task_display.delete("1.0", tk.END)
        self.task_display.insert("1.0", task["text"])
        
        self.label_type.config(text=f"Тип: {task['type']}")
        
        # Добавление в историю
        history_entry = f"{task['text'][:40]}... — {task['type']}"
        self.history.append({
            "text": task["text"],
            "type": task["type"],
            "full_display": history_entry
        })
        
        self.update_history()
        self.save_data()
        
        self.status_label.config(
            text=f"Задач в коллекции: {len(self.tasks)} | В истории: {len(self.history)}"
        )
    
    def add_task(self):
        """Добавление новой задачи"""
        
        text = self.entry_task.get("1.0", tk.END).strip()
        task_type = self.combo_type.get()
        
        if not self.validate_input(text, task_type):
            return
        
        task = {
            "text": text,
            "type": task_type
        }
        
        self.tasks.append(task)
        self.save_data()
        
        # Очистка полей
        self.entry_task.delete("1.0", tk.END)
        self.combo_type.set("Выберите тип")
        
        messagebox.showinfo("Успех", f"Задача добавлена!")
        self.status_label.config(
            text=f"Задач в коллекции: {len(self.tasks)} | В истории: {len(self.history)}"
        )
    
    def apply_filter(self):
        """Применение фильтрации истории"""
        
        type_filter = self.filter_type.get()
        
        self.history_listbox.delete(0, tk.END)
        
        for item in self.history:
            # Фильтр по типу
            if type_filter and type_filter != "Все":
                if type_filter != item["type"]:
                    continue
            
            self.history_listbox.insert(tk.END, item["full_display"])
    
    def reset_filter(self):
        """Сброс фильтров"""
        
        self.filter_type.set("Все")
        self.update_history()
    
    def update_history(self):
        """Обновление списка истории"""
        
        self.history_listbox.delete(0, tk.END)
        
        for item in self.history:
            self.history_listbox.insert(tk.END, item["full_display"])
    
    def clear_history(self):
        """Очистка истории"""
        
        confirm = messagebox.askyesno("Подтверждение", "Удалить всю историю?")
        
        if confirm:
            self.history = []
            self.update_history()
            self.save_data()
            messagebox.showinfo("Успех", "История очищена!")
            self.status_label.config(
                text=f"Задач в коллекции: {len(self.tasks)} | В истории: {len(self.history)}"
            )
    
    def save_data(self):
        """Сохранение данных в JSON"""
        
        try:
            # Сохранение коллекции задач
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
            
            # Сохранение истории
            with open(self.history_file, "w", encoding="utf-8") as file:
                json.dump(self.history, file, ensure_ascii=False, indent=4)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_tasks(self):
        """Загрузка задач из JSON"""
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {e}")
                self.tasks = self.default_tasks.copy()
        else:
            # Если файла нет, используем предопределённые задачи
            self.tasks = self.default_tasks.copy()
            self.save_data()
    
    def load_history(self):
        """Загрузка истории из JSON"""
        
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as file:
                    self.history = json.load(file)
                self.update_history()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
                self.history = []
        else:
            self.history = []
        
        self.status_label.config(
            text=f"Задач в коллекции: {len(self.tasks)} | В истории: {len(self.history)}"
        )


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
