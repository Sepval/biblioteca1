from models import Base, engine

# Crea todas las tablas definidas en models.py
Base.metadata.create_all(engine)

print("✅ Base de datos creada con éxito.")
