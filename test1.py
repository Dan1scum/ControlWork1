import flet as ft
from datetime import datetime
import os

HISTORY_FILE = "history.txt"


def main(page: ft.Page):
    page.title = "Empire of the Sun"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    greeting_history = []
    favorites = []
    last_name = None

    text_hello = ft.Text("Hello world", size=20)
    history_text = ft.Text("History of greetings:")
    favorites_text = ft.Text("Favorites:")

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            greeting_history = [line.strip() for line in f.readlines()][-5:]
        history_text.value = "History of greetings:\n" + "\n".join(greeting_history)

    def text_name(_):
        nonlocal last_name, greeting_history

        name = name_input.value.strip()
        if not name:
            text_hello.value = "Введите имя!"
            text_hello.color = ft.Colors.RED
            page.update()
            return

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{current_time} - {name}"

        last_name = name

        greeting_history.append(entry)
        greeting_history = greeting_history[-5:]

        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

        text_hello.value = f"{current_time} — hello, {name}!"
        text_hello.color = None
        name_input.value = ""

        history_text.value = "History of greetings:\n" + "\n".join(greeting_history)
        page.update()

    def clear_history(_):
        greeting_history.clear()
        history_text.value = "History of greetings:"
        open(HISTORY_FILE, "w").close()
        page.update()

    def add_to_favorites(_):
        if last_name and last_name not in favorites:
            favorites.append(last_name)
            favorites_text.value = "Favorites:\n" + "\n".join(favorites)
            page.update()

    def show_morning(_):
        filtered = [h for h in greeting_history if int(h[11:13]) < 12]
        history_text.value = "Morning greetings:\n" + "\n".join(filtered)
        page.update()

    def show_evening(_):
        filtered = [h for h in greeting_history if int(h[11:13]) >= 12]
        history_text.value = "Evening greetings:\n" + "\n".join(filtered)
        page.update()

    def switch_icon(_):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHTg
        )
        page.update()

    name_input = ft.TextField(
        label="Введите имя",
        expand=True,
        on_submit=text_name,
    )

    send_button = ft.ElevatedButton("Send", on_click=text_name)
    theme_button = ft.IconButton(icon=ft.Icons.BRIGHTNESS_7, on_click=switch_icon)
    clear_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=clear_history)
    fav_button = ft.IconButton(icon=ft.Icons.STAR, on_click=add_to_favorites)

    morning_btn = ft.TextButton("Утро", on_click=show_morning)
    evening_btn = ft.TextButton("Вечер", on_click=show_evening)

    page.add(
        text_hello,
        ft.Row([name_input, send_button, fav_button, theme_button, clear_button]),
        ft.Row([morning_btn, evening_btn]),
        history_text,
        favorites_text,
    )


ft.app(target=main)