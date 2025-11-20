import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass


@dataclass
class Card:
    value: str
    suit: str


VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']

SUITS = {
    'Черви': '♥',
    'Бубны': '♦',
    'Трефы': '♣',
    'Пики': '♠'
}

SUIT_COLOR = {
    'Черви': '#FF0000',
    'Бубны': '#FF0000',
    'Трефы': '#000000',
    'Пики': '#000000',
}


class CardGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Генератор игральных карт')
        self.root.geometry('400x300')
        self.root.resizable(False, False)

        pad = 10
        frm = ttk.Frame(root, padding=pad)
        frm.pack(expand=True, fill='both')

        lbl_val = ttk.Label(frm, text='Выберите значение карты:')
        lbl_val.pack(anchor='w', pady=(10, 2))

        self.value_cb = ttk.Combobox(frm, values=VALUES, state='readonly')
        self.value_cb.pack(fill='x')
        self.value_cb.set(VALUES[0])

        lbl_suit = ttk.Label(frm, text='Выберите масть карты:')
        lbl_suit.pack(anchor='w', pady=(12, 2))

        suit_names = [name for name in SUITS]
        self.suit_cb = ttk.Combobox(frm, values=suit_names, state='readonly')
        self.suit_cb.pack(fill='x')
        self.suit_cb.set(suit_names[0])

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(expand=True)

        show_btn = ttk.Button(btn_frame, text='Показать карту', command=self.show_card_modal)
        show_btn.pack(pady=10)

        self.center_window(self.root, 400, 300)

    def center_window(self, win: tk.Toplevel | tk.Tk, width: int, height: int):
        win.update_idletasks()
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        win.geometry(f'{width}x{height}+{x}+{y}')

    def show_card_modal(self):
        val = self.value_cb.get().strip() if (self.value_cb.get().strip().isdigit()) else self.value_cb.get().strip()[0]
        suit_name = self.suit_cb.get().strip()

        if not val or not suit_name:
            messagebox.showwarning('Ошибка', 'Пожалуйста, выберите значение и масть карты.')
            return

        suit_sym = SUITS.get(suit_name, '?')
        card = Card(value=val, suit=suit_name)

        modal = tk.Toplevel(self.root)
        modal.title(f'Ваша карта: {card.value} {card.suit}')
        modal.resizable(False, False)
        modal.transient(self.root)
        modal.grab_set()

        modal.geometry('300x450')
        self.center_window(modal, 300, 450)

        canvas = tk.Canvas(modal, width=300, height=400)
        canvas.pack(pady=10)

        card_w, card_h = 200, 300
        x0 = (300 - card_w) // 2
        y0 = (400 - card_h) // 2
        x1 = x0 + card_w
        y1 = y0 + card_h

        canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline='black')

        color = SUIT_COLOR.get(card.suit, '#000000')
        suit_sym = suit_sym

        try:
            small_font = ('Arial', 24)
            big_font = ('Arial', 48)
        except Exception:
            small_font = ('TkDefaultFont', 24)
            big_font = ('TkDefaultFont', 48)

        pad = 12
        top_left_x = x0 + pad
        top_left_y = y0 + pad
        canvas.create_text(top_left_x, top_left_y, anchor='nw', text=f'{card.value} {suit_sym}', font=small_font, fill=color)

        bottom_right_x = x1 - pad - 55
        bottom_right_y = y1 - pad - 30

        canvas.create_text(bottom_right_x, bottom_right_y, anchor='se', text=f'{card.value} {suit_sym}', font=small_font, fill=color, angle=180)

        center_x = (x0 + x1) // 2
        center_y = (y0 + y1) // 2
        canvas.create_text(center_x, center_y, text=suit_sym, font=big_font, fill=color)

        close_btn = ttk.Button(modal, text='Закрыть', command=lambda: self.close_modal(modal))
        close_btn.pack(pady=(6, 12))

        modal.protocol('WM_DELETE_WINDOW', lambda: self.close_modal(modal))
        modal.wait_window()

    def close_modal(self, modal: tk.Toplevel):
        try:
            modal.grab_release()
        except Exception:
            pass
        modal.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = CardGeneratorApp(root)
    root.mainloop()
