from streaming import Userplay, Playlist, Media, Genre

def test_query_users(session):
    users = session.query(Userplay).all()
    assert len(users) >= 1  # Debe haber al menos un usuario
    for user in users:
        assert user.username is not None
        assert user.email is not None

def test_query_media(session):
    media_files = session.query(Media).all()
    assert len(media_files) >= 3  # Debe haber al menos tres archivos de medios
    for media in media_files:
        assert media.name_media is not None
        assert media.description_media is not None

def test_query_genre(session):
    genres = session.query(Genre).all()
    assert len(genres) >= 3  # Debe haber al menos tres géneros
    for genre in genres:
        assert genre.name_genre is not None

def test_query_playlist(session):
    playlists = session.query(Playlist).all()
    assert len(playlists) >= 2  # Debe haber al menos dos listas de reproducción
    for playlist in playlists:
        assert playlist.title is not None
        assert playlist.user_id is not None




