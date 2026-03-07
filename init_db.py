# init_db.py
from app import app, db
from models import Usuario, Especialidad, RolUsuario
from werkzeug.security import generate_password_hash

with app.app_context():
    # Eliminar todas las tablas
    print("🗑️  Eliminando tablas antiguas...")
    db.drop_all()
    
    # Crear todas las tablas nuevas
    print("📦 Creando tablas nuevas...")
    db.create_all()
    
    # Crear especialidades
    print("⚕️  Insertando especialidades...")
    especialidades = [
        Especialidad(nombre="Clínica Médica", costo_consulta=15000, duracion_turno=30),
        Especialidad(nombre="Pediatría", costo_consulta=15000, duracion_turno=30),
        Especialidad(nombre="Cardiología", costo_consulta=20000, duracion_turno=45),
        Especialidad(nombre="Dermatología", costo_consulta=18000, duracion_turno=30),
        Especialidad(nombre="Traumatología", costo_consulta=18000, duracion_turno=30),
        Especialidad(nombre="Ginecología", costo_consulta=20000, duracion_turno=45),
    ]
    
    for esp in especialidades:
        db.session.add(esp)
    
    # Crear usuario admin
    print("👤 Creando usuario administrador...")
    admin = Usuario(
        nombre="Admin",
        apellido="Sistema",
        dni="00000000",
        email="admin@consultorio.com",
        telefono="1234567890",
        rol=RolUsuario.ADMIN
    )
    admin.set_password("admin123")
    
    db.session.add(admin)
    db.session.commit()
    
    print("✅ Base de datos inicializada correctamente!")
    print("")
    print("Credenciales del administrador:")
    print("DNI: 00000000")
    print("Password: admin123")