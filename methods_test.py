from streaming import Userplay, Media, Playlist, Genre, PlaylistHistory
from datetime import date as current_date

def test_user_auth(session):
    user = Userplay(username='user_temp', password_user='password_temp', email='user_temp@example.com')
    session.add(user)
    session.commit()
    query = session.query(Userplay).filter_by(username=user.username, password_user=user.password_user)
    assert query.count() > 0, "User authentication failed"

def test_generate_playlist_history(session):
    genre = Genre(name_genre="test genre")
    session.add(genre)
    session.commit()

    media = Media(name_media="test media", genre_id=genre.id_genre, description_media="This is a test media description")
    session.add(media)
    session.commit()

    first_user = session.query(Userplay).first().id_user
    playlist_history = PlaylistHistory(user_idplay=first_user, media_idplay=media.id_media, date_playisth=current_date.today().strftime('%Y-%m-%d'))
    session.add(playlist_history)
    session.commit()

    assert playlist_history.user_idplay is not None, "User ID should not be None"
    assert playlist_history.media_idplay is not None, "Media ID should not be None"
    assert playlist_history.date_playisth is not None, "Date should not be None"

def test_create_user(session):
    user = Userplay(username='new_user', password_user='new_password', email='new_user@example.com')
    session.add(user)
    session.commit()
    assert user.id_user is not None, "User ID should not be None"

def test_create_media(session):
    genre = Genre(name_genre="test genre 2")
    session.add(genre)
    session.commit()
    
    media = Media(name_media='new_media', genre_id=genre.id_genre, description_media='New media description')
    session.add(media)
    session.commit()
    assert media.id_media is not None, "Media ID should not be None"

def test_create_playlist(session):
    user = Userplay(username='playlist_user', password_user='playlist_password', email='playlist_user@example.com')
    session.add(user)
    session.commit()

    media = Media(name_media='playlist_media', description_media='Playlist media description')
    session.add(media)
    session.commit()

    playlist = Playlist(user_id=user.id_user, media_id=media.id_media, title='My Playlist')
    session.add(playlist)
    session.commit()
    assert playlist.id_playlist is not None, "Playlist ID should not be None"

def test_create_genre(session):
    genre = Genre(name_genre='new_gender')
    session.add(genre)
    session.commit()
    assert genre.id_genre is not None, "Genre ID should not be None"

