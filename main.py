from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.clock import Clock

import sqlite3
from datetime import datetime, timedelta

DB_FILE = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS funds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fund_id INTEGER,
                    amount REAL,
                    item TEXT,
                    note TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (fund_id) REFERENCES funds(id)
                )''')
    conn.commit()
    conn.close()

class ExpenseApp(App):
    def build(self):
        init_db()
        return MainLayout()

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.fund_spinner = Spinner(text='選擇資金欄', size_hint=(1, None), height=40)
        self.refresh_fund_list()

        btn_add_fund = Button(text='新增資金欄', size_hint=(1, None), height=40, on_press=self.add_fund_popup)
        self.expense_list = Label(text='', size_hint_y=None)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.expense_list)

        btn_add_expense = Button(text='新增支出', size_hint=(1, None), height=40, on_press=self.add_expense_popup)
        btn_show_summary = Button(text='本月摘要', size_hint=(1, None), height=40, on_press=self.show_summary)

        self.add_widget(self.fund_spinner)
        self.add_widget(btn_add_fund)
        self.add_widget(btn_add_expense)
        self.add_widget(btn_show_summary)
        self.add_widget(scroll)

        Clock.schedule_once(lambda dt: self.refresh_expenses(), 0.5)

    def refresh_fund_list(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT name FROM funds")
        funds = [row[0] for row in c.fetchall()]
        conn.close()
        self.fund_spinner.values = funds

    def add_fund_popup(self, instance):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        input_name = TextInput(hint_text="資金欄名稱")
        btn_confirm = Button(text='確認新增', size_hint_y=None, height=40)

        layout.add_widget(input_name)
        layout.add_widget(btn_confirm)

        popup = App.get_running_app().popup_cls(title="新增資金欄", content=layout)
        btn_confirm.bind(on_press=lambda x: self.save_fund(input_name.text, popup))
        popup.open()

    def save_fund(self, name, popup):
        if name.strip():
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO funds (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            self.refresh_fund_list()
            popup.dismiss()

    def add_expense_popup(self, instance):
        if not self.fund_spinner.text or self.fund_spinner.text == '選擇資金欄':
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        input_amount = TextInput(hint_text="金額", input_filter='float')
        input_item = TextInput(hint_text="品項")
        input_note = TextInput(hint_text="備註（可留空）")
        btn_confirm = Button(text='確認新增', size_hint_y=None, height=40)

        layout.add_widget(input_amount)
        layout.add_widget(input_item)
        layout.add_widget(input_note)
        layout.add_widget(btn_confirm)

        popup = App.get_running_app().popup_cls(title="新增支出", content=layout)
        btn_confirm.bind(on_press=lambda x: self.save_expense(input_amount.text, input_item.text, input_note.text, popup))
        popup.open()

    def save_expense(self, amount, item, note, popup):
        try:
            amount = float(amount)
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT id FROM funds WHERE name = ?", (self.fund_spinner.text,))
            fund_id = c.fetchone()[0]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("INSERT INTO expenses (fund_id, amount, item, note, timestamp) VALUES (?, ?, ?, ?, ?)",
                      (fund_id, amount, item, note, timestamp))
            conn.commit()
            conn.close()
            popup.dismiss()
            self.refresh_expenses()
        except ValueError:
            pass  # 金額格式錯誤

    def refresh_expenses(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            SELECT f.name, e.amount, e.item, e.note, e.timestamp
            FROM expenses e
            JOIN funds f ON e.fund_id = f.id
            ORDER BY e.timestamp DESC
        ''')
        rows = c.fetchall()
        conn.close()

        text = '\n'.join([f"[{row[4][:10]}] {row[0]} - ${row[1]} - {row[2]} ({row[3]})" for row in rows])
        self.expense_list.text = text

    def show_summary(self, instance):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        now = datetime.now()
        this_month = now.strftime('%Y-%m')
        last_month = (now.replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
        c.execute("SELECT SUM(amount), DATE(timestamp) FROM expenses WHERE strftime('%Y-%m', timestamp) = ? GROUP BY DATE(timestamp)", (last_month,))
        days = c.fetchall()
        conn.close()

        if days:
            total = sum(day[0] for day in days)
            most = max(days, key=lambda x: x[0])
            summary = f"{last_month} 總支出: ${total:.2f}\n支出最多日: {most[1]} (${most[0]:.2f})"
        else:
            summary = f"{last_month} 沒有任何支出紀錄"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text=summary))
        btn_close = Button(text='關閉', size_hint_y=None, height=40)
        layout.add_widget(btn_close)

        popup = App.get_running_app().popup_cls(title="本月摘要", content=layout)
        btn_close.bind(on_press=popup.dismiss)
        popup.open()

# 適配手機，使用 KivyMD 可以換成 Snackbar 或 Dialogs
from kivy.uix.popup import Popup
class CustomApp(ExpenseApp):
    def popup_cls(self, title, content):
        return Popup(title=title, content=content, size_hint=(0.9, 0.6))

if __name__ == '__main__':
    CustomApp().run()
