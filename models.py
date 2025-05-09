from sqlalchemy import Column, Integer, String, ForeignKey, Date, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

Base = declarative_base()

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    libros = relationship('Libro', back_populates='autor')

class Libro(Base):
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    autor_id = Column(Integer, ForeignKey('autores.id'))
    prestado = Column(Integer, default=0)  # 0 = disponible, 1 = prestado
    autor = relationship('Autor', back_populates='libros')
    prestamos = relationship('Prestamo', back_populates='libro')

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    prestamos = relationship('Prestamo', back_populates='usuario')

class Prestamo(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True)
    libro_id = Column(Integer, ForeignKey('libros.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_prestamo = Column(Date, default=datetime.date.today)
    fecha_devolucion = Column(Date, nullable=True)
    libro = relationship('Libro', back_populates='prestamos')
    usuario = relationship('Usuario', back_populates='prestamos')

engine = create_engine('sqlite:///biblioteca.db')
Session = sessionmaker(bind=engine)
# se hizo cambios en la consola 