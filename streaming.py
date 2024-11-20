from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime

Base = declarative_base()

class Userplay(Base):
    __tablename__ = 'userplay'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password_user = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    playlists = relationship('Playlist', back_populates='user')
    playlist_histories = relationship('PlaylistHistory', back_populates='user')

class Playlist(Base):
    __tablename__ = 'playlist'
    id_playlist = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('userplay.id_user'), nullable=False)
    media_id = Column(Integer, ForeignKey('media.id_media'), nullable=False)
    title = Column(String(100), nullable=False)
    user = relationship('Userplay', back_populates='playlists')
    media = relationship('Media')

class Media(Base):
    __tablename__ = 'media'
    id_media = Column(Integer, primary_key=True, autoincrement=True)
    genre_id = Column(Integer, ForeignKey('genre.id_genre'))
    name_media = Column(String(100), nullable=False)
    description_media = Column(String(1000))
    playlist_histories = relationship('PlaylistHistory', back_populates='media')

class Genre(Base):
    __tablename__ = 'genre'
    id_genre = Column(Integer, primary_key=True, autoincrement=True)
    name_genre = Column(String(100), nullable=False, unique=True)
    media = relationship('Media', backref='genre')

class PlaylistHistory(Base):
    __tablename__ = 'playlist_history'
    id_history = Column(Integer, primary_key=True, autoincrement=True)
    user_idplay = Column(Integer, ForeignKey('userplay.id_user'), nullable=False)
    media_idplay = Column(Integer, ForeignKey('media.id_media'), nullable=False)
    date_playisth = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('Userplay', back_populates='playlist_histories')
    media = relationship('Media', back_populates='playlist_histories')

# Crear la base de datos
DATABASE_URL = "mysql+pymysql://root:gapecm250320@localhost/streaming_ds"
engine = create_engine(DATABASE_URL)

# Verificar la conexión
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection to the database was successful!")
except Exception as e:
    print(f"An error occurred: {e}")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)