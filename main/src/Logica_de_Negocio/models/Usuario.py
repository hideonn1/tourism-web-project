class Usuario:
    def __init__(self,
                  id_usuario,
                  rut,
                  nombres,
                  apellido_paterno,
                  apellido_materno,
                  email,
                  contraseña_hash,
                  telefono,
                  fecha_nacimiento,
                  fecha_registro,
                  rol="Cliente"):
        
        self.id_usuario = id_usuario
        self.rut = rut
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.email = email
        self.contraseña_hash = contraseña_hash
        self.contraseña = contraseña_hash 
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_registro = fecha_registro
        self.rol = rol

    def __str__(self):
        return (f"Usuario ID: {self.id_usuario}, "
                f"Nombre: {self.nombres} {self.apellido_paterno}, "
                f"Email: {self.email}")

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "rut": self.rut,
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "fecha_nacimiento": str(self.fecha_nacimiento),
            "fecha_registro": str(self.fecha_registro),
            "rol": self.rol
        }
