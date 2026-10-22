# main.py
import flet as ft
from app.ui import ScraperUI
from core.version import APP_TITLE


def main(page: ft.Page):
    page.title = APP_TITLE
    page.theme_mode = ft.ThemeMode.DARK

    # Instanciamos la interfaz gráfica principal
    ScraperUI(page)


if __name__ == "__main__":
    # Usamos ft.run(main) que es el estándar actual en Flet
    ft.run(main)