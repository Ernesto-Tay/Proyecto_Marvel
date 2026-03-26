import json
import os
from pathlib import Path


class Auth:
    def __init__(self):
        self.admin_actual = None
        self.raiz = Path(__file__).resolve().parent.parent
        self.carpeta_datos = self.raiz / "Datos_json"

        # Forzar creación de la carpeta en la raíz
        self.carpeta_datos.mkdir(parents=True, exist_ok=True)

        self._cargar_admin()

    def _cargar_admin(self):
        archivo = self.carpeta_datos / "admin.json"

        if not archivo.exists():
            self._crear_admin_defecto()
            return

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                from Modelos.Clase_admin import Admin
                self.admin = Admin(datos['usuario'], datos['contraseña'])
                self.admin.nombre = datos.get('nombre', 'Administrador')
                self.admin.clave = datos.get('clave', 'fbf84155d27a9d5b213d286a78a11d26ad34a302')
        except Exception as e:
            print(f"Error al cargar admin: {e}")
            self._crear_admin_defecto()

    def _crear_admin_defecto(self):
        from Modelos.Clase_admin import Admin
        self.admin = Admin("admin", "admin123")
        self.admin.clave = "fbf84155d27a9d5b213d286a78a11d26ad34a302"
        self._guardar_admin()
        print(f"Archivo JSON creado en: {self.carpeta_datos / 'admin.json'}")

    def _guardar_admin(self):
        archivo = self.carpeta_datos / "admin.json"
        datos = {
            "usuario": self.admin.usuario,
            "contraseña": self.admin.contraseña,
            "nombre": self.admin.nombre,
            "clave": self.admin.clave }
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2)

    def login(self, usuario, contraseña):
        if usuario == self.admin.usuario and self.admin.verificar_contraseña(contraseña):
            self.admin_actual = self.admin
            return True, "Login exitoso"
        return False, "Usuario o contraseña incorrectos"
