from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class Userplay(Base):
    __tablename__ = 'userplay'
    id_user = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_user = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    
    # Define relationships with Playlist and PlaylistHistory
    playlists = relationship('Playlist', back_populates='user')
    history = relationship('PlaylistHistory', back_populates='user')

class Genre(Base):
    __tablename__ = 'genre'
    id_genre = Column(Integer, primary_key=True)
    name_genre = Column(String(100), nullable=False)
    
    # Define relationship with Media
    media = relationship('Media', back_populates='genre')

class Media(Base):
    __tablename__ = 'media'
    id_media = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.id_genre'))
    name_media = Column(String(100), nullable=False)
    description_media = Column(String(1000), nullable=False)
    
    # Define relationships with Playlist and PlaylistHistory
    genre = relationship('Genre', back_populates='media')
    playlists = relationship('Playlist', back_populates='media')
    history = relationship('PlaylistHistory', back_populates='media')

class Playlist(Base):
    __tablename__ = 'playlist'
    id_playlist = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('userplay.id_user'))
    media_id = Column(Integer, ForeignKey('media.id_media'))
    title = Column(String(100), nullable=False)
    
    # Define relationships with Userplay and Media
    user = relationship('Userplay', back_populates='playlists')
    media = relationship('Media', back_populates='playlists')

class PlaylistHistory(Base):
    __tablename__ = 'playlist_history'

    id_history = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('userplay.id_user'))
    media_id = Column(Integer, ForeignKey('media.id_media'))
    date_playlist = Column(String(100))

    # Define relationships with Userplay and Media
    user = relationship('Userplay', back_populates='history')
    media = relationship('Media', back_populates='history')

    def __init__(self, user_id, media_id, date_playlist):
        self.user_id = user_id
        self.media_id = media_id
        self.date_playlist = date_playlist

# Create the database
DATABASE_URL = "mysql+pymysql://root:gapecm250320@localhost/Streaming_DS"
engine = create_engine(DATABASE_URL)

# Verify the connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection to the database was successful!")
except Exception as e:
    print(f"An error occurred: {e}")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

