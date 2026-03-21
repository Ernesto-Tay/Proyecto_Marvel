class Admin:
    def __init__(self, usuario, contraseña):
        self.usuario = usuario
        self.contraseña = contraseña
        self.nombre = "Administrador"

    def verificar_contraseña(self, contraseña):
        return self.contraseña == contraseña

    def __str__(self):
        return f"Admin: {self.usuario}"