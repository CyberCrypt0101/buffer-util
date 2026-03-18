import flet as ft
import base64
import os
from cryptography.hazmat.primitives import hashes as h
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as PBK
from cryptography.fernet import Fernet as F

def _x(p, s):
    v = os.getenv("S_REF", "default_00x_system_call")
    c = p + v
    k = PBK(
        algorithm=h.SHA256(),
        length=32,
        salt=s,
        iterations=600000,
    )
    return base64.urlsafe_b64encode(k.derive(c.encode()))

def main(page: ft.Page):
    page.title = "Slayer Crypt"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    v1 = ft.TextField(label="Secret Key", password=True, width=350, text_align="center")
    v2 = ft.TextField(label="Secret Message", multiline=True, min_lines=3, width=350)
    v3 = ft.TextField(label="Special Message", read_only=True, multiline=True, width=350)

    def _a(e):
        if not v1.value or not v2.value: return
        try:
            s = os.urandom(16)
            r = _x(v1.value, s)
            m = F(r)
            z = m.encrypt(v2.value.encode())
            v3.value = base64.b64encode(s + z).decode()
        except:
            v3.value = "Status: 404"
        page.update()

    def _b(e):
        try:
            r_d = base64.b64decode(v2.value.encode())
            s = r_d[:16]
            b = r_d[16:]
            r = _x(v1.value, s)
            m = F(r)
            v3.value = m.decrypt(b).decode()
        except:
            v3.value = "DO NOT TRY TO BE OVER SMART BUDDY!!!!"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Slayer Crypt", size=24, weight="bold", color="grey"),
            ft.Text("Warning: FBI has entered the chat", size=28, color="red"),
            ft.Divider(height=12, color="transparent"),
            v1,
            v2,
            ft.Row([
                ft.ElevatedButton("Encrypt", on_click=_a, width=150),
                ft.ElevatedButton("Decrypt", on_click=_b, width=150),
            ], alignment="center"),
            v3,
        ], horizontal_alignment="center", spacing=16)
    )

ft.app(target=main)
