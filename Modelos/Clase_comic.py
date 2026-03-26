from datetime import datetime


class Comic:
    def __init__(self, id_marvel, titulo, imagen, fecha_lanzamiento):
        self.id = id_marvel
        self.titulo = titulo
        self.imagen = imagen
        self.isbn = ""
        self.descripcion = ""
        self.personajes = []  # lista de ids de personajes
        self.creadores = []  # lista de ids de creadores
        self.eventos = []    # lista de ids de eventos
        self.nombres_creadores = []
        self.nombres_personajes = []
        self.detalles_creadores = []
        self.detalles_personajes = []

        # Normalizar fecha a formato MM-AAAA para almacenamiento y display
        self.fecha_lanzamiento = self._normalizar_fecha(fecha_lanzamiento)

    @staticmethod
    def _normalizar_fecha(fecha_raw):
        """Convierte cualquier formato de fecha de Comic Vine a MM-AAAA."""
        if not fecha_raw:
            return ""
        for fmt in ("%Y-%m-%d", "%Y-%m"):
            try:
                dt = datetime.strptime(str(fecha_raw)[:10], fmt)
                return dt.strftime("%m-%Y")
            except ValueError:
                continue
        return str(fecha_raw)

    @property
    def nombre(self):
        return self.titulo or ""

    def obtener_nombre(self):
        return self.titulo or ""

    def obtener_nombre_busqueda(self):
        return self.titulo

    def obtener_fecha(self):
        """Retorna fecha en formato AAAA-MM para que la comparación de strings funcione correctamente."""
        if not self.fecha_lanzamiento:
            return ""
        partes = self.fecha_lanzamiento.split("-")
        if len(partes) == 2:
            return f"{partes[1]}-{partes[0]}"  # MM-AAAA → AAAA-MM (para ordenar)
        return self.fecha_lanzamiento

    def __str__(self):
        return f"Comic: {self.titulo}"
