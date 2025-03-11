import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, String, ForeignKey, LargeBinary
from eralchemy2 import render_er
from passlib.hash import bcrypt_sha256
from typing import Optional, List

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # Aquí ponemos que el username debe ser único para no repetir y que el límite de carácteres es 50.
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    profile_image: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True) # Almacenamos las imágines de perfil en bytes, haciéndolo opcional y pudiendo dejarse en blanco.

    def encrypt_pass(self, raw_pass: str) -> None: # Para encriptar la contraseña usamos bcrypt_sha256. Pasamos una contraseña y la encriptamos.
        self.password = bcrypt_sha256.hash(raw_pass)

    def verify_pass(self, raw_pass: str) -> bool: # Validamos la contraseña encriptada. Como la comparamos usando bcrypt_sha256 debería dar True.
        return bcrypt_sha256.verify(raw_pass, self.password)

class People(Base):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[str] = mapped_column(nullable=False)
    mass: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="people") # Relación hacia favoritos.

class Planets(Base):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    climate: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="planet") # Relación hacia favoritos.

class Vehicles(Base):
    __tablename__ = 'vehicles'
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(nullable=False)
    manufacturer: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="vehicles") # Relación hacia favoritos.

class Favorites(Base):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    # Estos datos de la tabla vienen de datos de otras tablas, por lo que los definimos.
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    vehicles_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))

    # Relaciones de vuelta a cada una de las tablas anteriores
    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")
    planet: Mapped["Planets"] = relationship(back_populates="favorites")
    vehicle: Mapped["Vehicles"] = relationship(back_populates="favorites")


## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
