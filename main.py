# Part 1/12 - Khaled Nageh: Project Intro + Abstract Base Class (BaseSeat)
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import math
import json
import os

# Lecture 6: Abstract Base Class
class BaseSeat(ABC):
    @abstractmethod
    def book(self, canvas):
        pass

# Part 2/12 - Omar Mohammed: Multiple Inheritance (Clickable, Highlightable, SpecialSeat)
# Lecture 6: Multiple Inheritance
class Clickable:
    def click(self):
        print(f"Clicked on {self}")

class Highlightable:
    def highlight(self):
        print(f"Highlighted {self}")

class SpecialSeat(Clickable, Highlightable, BaseSeat):
    def __init__(self, seat):
        self._seat = seat

    def book(self, canvas):
        self._seat.book(canvas)

# Part 3/12 - mohamed mahmoud: Seat class (attributes + constructor)
# Lecture 1–4: Core Class with Static Members, Constructors, Encapsulation
class Seat(BaseSeat):
    _count = 0
    PRICES = {
        "premium": 25.0,
        "standard": 18.0,
        "value": 12.0,
        "reserved": 30.0,
        "obstructed": 10.0,
        "handicap": 15.0,
    }

    def __init__(self, canvas, seat_id, x, y, seat_type, color, update_callback, w=20, h=15, angle_deg=0, price=None):
        self.__seat_id = seat_id
        self.__x, self.__y = x, y
        self.__booked = False
        self.seat_type = seat_type
        self.color = color
        self.__price = price if price is not None else Seat.PRICES.get(seat_type, 0)
        self.update_callback = update_callback
        self.w, self.h = w, h
        self.angle_deg = angle_deg

        Seat._count += 1
        self.draw(canvas)

# Part 4/12 - Mohamed Ashraf : Factory Constructor + Destructor
    @classmethod
    def from_dict(cls, data, canvas, seat_colors, update_callback):
        st = data.get('seat_type', 'standard')
        color = seat_colors.get(st, 'gray')
        s = cls(canvas, data['seat_id'], data.get('x', 0), data.get('y', 0), st, color, update_callback,
                data.get('w', 20), data.get('h', 15), data.get('angle_deg', 0), data.get('price'))
        if data.get('booked'):
            s.book(canvas)
        return s

    def __del__(self):
        print(f"Seat {self.__seat_id} destroyed")

# Part 5/12 - Yaseen ashraf: Properties + Encapsulation
    @property
    def seat_id(self): return self.__seat_id

    @property
    def booked(self): return self.__booked

    @booked.setter
    def booked(self, val):
        if not isinstance(val, bool):
            raise ValueError("Booked flag must be a boolean")
        self.__booked = val

    @property
    def price(self): return self.__price

    @price.setter
    def price(self, val):
        if val < 0:
            raise ValueError("Price must be non-negative")
        self.__price = val

# Part 6/12 - AlamElhoda Elbeltagy: Static members + Static method
    @staticmethod
    def total_seats():
        return Seat._count

# Part 7/12 - Moaz Abu lailla: draw() + on_click()
    def draw(self, canvas):
        angle = math.radians(self.angle_deg)
        cx, cy = self.__x + self.w / 2, self.__y + self.h / 2
        coords = []
        for dx, dy in [(-self.w/2, -self.h/2), (self.w/2, -self.h/2),
                       (self.w/2, self.h/2), (-self.w/2, self.h/2)]:
            rx = cx + dx * math.cos(angle) - dy * math.sin(angle)
            ry = cy + dx * math.sin(angle) + dy * math.cos(angle)
            coords.extend((rx, ry))
        fill = self.color if not self.__booked else "red"
        self._shape = canvas.create_polygon(coords, fill=fill, outline="black", tags=self.__seat_id)
        canvas.create_text(cx, cy, text=self.__seat_id, font=("Arial", 8), tags=self.__seat_id)
        canvas.tag_bind(self.__seat_id, "<Button-1>", lambda e: self.on_click(canvas))

    def on_click(self, canvas):
        if self.__booked:
            messagebox.showinfo("Already Booked", f"Seat {self.__seat_id} is already booked.")
        else:
            if messagebox.askyesno("Book Seat", f"Book seat {self.__seat_id} for ${self.__price:.2f}?"):
                self.book(canvas)

# Part 8/12 - Abdelrahman Bayoumi: book(), reset(), to_dict(), load_state
    def book(self, canvas):
        self.__booked = True
        canvas.itemconfig(self._shape, fill="red")
        self.update_callback()

    def reset(self, canvas):
        self.__booked = False
        canvas.itemconfig(self._shape, fill=self.color)
        self.update_callback()

    def to_dict(self):
        return {
            'seat_id': self.__seat_id,
            'booked': self.__booked,
            'seat_type': self.seat_type,
            'x': self.__x, 'y': self.__y,
            'w': self.w, 'h': self.h,
            'angle_deg': self.angle_deg,
            'price': self.__price
        }

    def load_state(self, state, canvas):
        if state.get('booked'):
            self.book(canvas)

# Part 9/12 - Eslam Samir: Operator Overloading (__add__)
    def __add__(self, other):
        if isinstance(other, Seat):
            return self.price + other.price
        raise TypeError("Can only add Seat to Seat")

# Part 10/12 - Mohannad: Inheritance (PremiumSeat, StandardSeat, ValueSeat)
class PremiumSeat(Seat):
    def get_price(self):
        return super().price * 1.5

class StandardSeat(Seat):
    def get_price(self):
        return super().price

class ValueSeat(Seat):
    def get_price(self):
        return super().price * 0.8

# Part 11/12 - Mohamed Elkassas: CinemaScreen class
class CinemaScreen:
    def __init__(self, canvas, seat_colors, update_callback):
        self.canvas = canvas
        self.seat_colors = seat_colors
        self.update_callback = update_callback
        self.seats = []

    def add_seat(self, seat_id, x, y, seat_type, w=20, h=15, angle_deg=0):
        color = self.seat_colors.get(seat_type, 'gray')
        s = Seat(self.canvas, seat_id, x, y, seat_type, color, self.update_callback, w, h, angle_deg)
        self.seats.append(s)

    def book_all(self):
        for s in self.seats:
            s.book(self.canvas)

    def reset_all(self):
        for s in self.seats:
            s.reset(self.canvas)

    def get_summary(self):
        booked = [s for s in self.seats if s.booked]
        lines, total = [], 0
        for s in booked:
            price = s.get_price() if hasattr(s, 'get_price') else s.price
            lines.append(f"{s.seat_id}: ${price:.2f}")
            total += price
        return "\n".join(lines), total

    def save_bookings(self, filename='bookings.json'):
        with open(filename, 'w') as f:
            json.dump([s.to_dict() for s in self.seats], f)

    def load_bookings(self, filename='bookings.json'):
        if os.path.exists(filename):
            with open(filename) as f:
                state_map = {d['seat_id']: d for d in json.load(f)}
                for s in self.seats:
                    if s.seat_id in state_map:
                        s.load_state(state_map[s.seat_id], self.canvas)

    def get_total_price(self):
        return sum((s.get_price() if hasattr(s, 'get_price') else s.price) for s in self.seats if s.booked)

# Part 12/12 - Amr El Sayed: GUI Class (CinemaApp) + UI Layout + Buttons + Summary
class CinemaApp:
    def __init__(self, root):
        self.root = root
        root.title("Cinema Seat Booking")
        root.geometry("1280x720")

        self.canvas = tk.Canvas(root, width=1280, height=720)
        self.canvas.pack()
        img = Image.open('seating_chart.jpg').resize((1280, 720), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg)

        self.total_label = tk.Label(root, text='Total: $0.00', font=('Arial', 12, 'bold'), bg='white')
        self.total_label.place(x=20, y=10)

        self.seat_colors = {
            'premium': '#FFFD55', 'standard': 'purple', 'value': 'green',
            'reserved': '#39107B', 'obstructed': 'maroon', 'handicap': '#a6ffae'
        }

        self.screen = CinemaScreen(self.canvas, self.seat_colors, self.update_total)
        self.draw_layout()
        self.screen.load_bookings()
        self.update_total()
        self.draw_legend()

        tk.Button(root, text='🎟️ Book All', command=self.screen.book_all).place(x=1050, y=20)
        tk.Button(root, text='🔁 Reset All', command=self.screen.reset_all).place(x=1150, y=20)
        tk.Button(root, text='📂 Save', command=self.screen.save_bookings).place(x=1050, y=60)
        tk.Button(root, text='📂 Load', command=self.screen.load_bookings).place(x=1150, y=60)
        tk.Button(root, text='📋 Summary', command=self.show_summary).place(x=1100, y=100)

    def draw_layout(self):
        for i in range(2):
            self.screen.add_seat(f'VIP_{i+1}', 550 + i * 30, 580, 'reserved', w=24, h=18)
        for i in range(6):
            self.screen.add_seat(f'P1_{i+1}', 500 + i * 20, 300, 'premium')
            self.screen.add_seat(f'P2_{i+1}', 700 - i * 20, 300, 'premium')
        for r in range(2):
            for c in range(8):
                self.screen.add_seat(f'V{r+1}_{c+1}', 450 + c * 20, 350 + r * 30, 'value')
                self.screen.add_seat(f'V{r+3}_{c+1}', 750 - c * 20, 350 + r * 30, 'value')
        for r in range(3):
            for c in range(10):
                self.screen.add_seat(f'S{r+1}_{c+1}', 400 + c * 30, 500 + r * 30, 'standard')

    def draw_legend(self):
        x0, y0 = 20, 50
        for idx, (stype, col) in enumerate(self.seat_colors.items()):
            self.canvas.create_rectangle(x0, y0 + idx * 20, x0 + 15, y0 + 15 + idx * 20, fill=col, outline='black')
            self.canvas.create_text(x0 + 25, y0 + 7 + idx * 20, anchor='w', text=stype.title(), font=('Arial', 8))

    def update_total(self):
        total = self.screen.get_total_price()
        self.total_label.config(text=f'Total: ${total:.2f}')

    def show_summary(self):
        summary, total = self.screen.get_summary()
        messagebox.showinfo('Booking Summary', f"{summary}\n\nTotal: ${total:.2f}")

if __name__ == '__main__':
    root = tk.Tk()
    app = CinemaApp(root)
    root.mainloop()
