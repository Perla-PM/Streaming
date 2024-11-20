from flask import Flask, send_from_directory, jsonify, request, redirect, url_for, render_template, abort
from db_integration import Userplay, Playlist, Media, Genre, PlaylistHistory, Session
import os
from datetime import datetime

app = Flask(__name__, template_folder='static/html')
app.config['UPLOAD_FOLDER'] = 'static/upload'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/user/login', methods=['POST'])
def login():
    session = Session()
    data = request.json
    user = session.query(Userplay).filter_by(username=data['username'], password_user=data['password']).first()
    session.close()
    if user:
        return jsonify({"status": "success", "user": user.username})
    else:
        return jsonify({"status": "failure"}), 401

@app.route('/add_media', methods=['GET', 'POST'])
def upload_image():
    session = Session()
    if request.method == 'POST':
        file = request.files['file']
        description = request.form['description']

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_media = Media(name_media=filename, description_media=description)
            session.add(new_media)
            session.commit()

            # Adding media to PlaylistHistory
            user_id = request.form.get('user_id')  # Ensure you have user_id in the form
            if user_id:
                new_history = PlaylistHistory(user_id=user_id, media_id=new_media.id_media, date_playlist=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                session.add(new_history)
                session.commit()

            session.close()
            return redirect(url_for('display_images'))

    session.close()
    return render_template('add_media.html')

@app.route('/display_media')
def display_images():
    session = Session()
    media_list = session.query(Media).all()
    session.close()
    return render_template('display_media.html', media_list=media_list)

@app.route('/image/<int:media_id>')
def get_image(media_id):
    session = Session()
    media = session.query(Media).filter_by(id_media=media_id).first()
    session.close()
    if media:
        filename = media.name_media
        try:
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        except FileNotFoundError:
            abort(404)
    else:
        abort(404)

@app.route('/update_media/<int:media_id>', methods=['GET', 'POST'])
def update_media(media_id):
    session = Session()
    media = session.query(Media).filter_by(id_media=media_id).first()

    if request.method == 'POST':
        new_name = request.form['name_media']
        new_description = request.form['description_media']

        if media:
            media.name_media = new_name
            media.description_media = new_description
            session.commit()
            session.close()

            # Adding media update to PlaylistHistory
            user_id = request.form.get('user_id')  # Ensure you have user_id in the form
            if user_id:
                new_history = PlaylistHistory(user_id=user_id, media_id=media_id, date_playlist=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                session.add(new_history)
                session.commit()

            return redirect(url_for('display_images'))
        else:
            session.close()
            abort(404)

    session.close()
    return render_template('update_media.html', media=media)

@app.route('/delete_media/<int:media_id>', methods=['POST'])
def delete_media(media_id):
    session = Session()
    media = session.query(Media).filter_by(id_media=media_id).first()

    if media:
        session.delete(media)
        session.commit()

        # Removing media from PlaylistHistory
        session.query(PlaylistHistory).filter_by(media_id=media_id).delete()
        session.commit()

        session.close()
        return redirect(url_for('display_images'))
    else:
        session.close()
        abort(404)

# Función para añadir una playlist
@app.route('/add_playlist', methods=['GET', 'POST'])
def add_playlist():
    if request.method == 'POST':
        title = request.form.get('title')
        user_id = request.form.get('user_id')
        media_id = request.form.get('media_id')  # Obtener media_id del formulario

        # Validar user_id
        if not user_id or not user_id.isdigit():
            return abort(400, description="Invalid User ID.")
        
        # Validar media_id
        media_id = int(media_id) if media_id and media_id.isdigit() else None  # Convertir a entero o None
        user_id = int(user_id)  # Convertir user_id a entero

        session = Session()
        new_playlist = Playlist(title=title, user_id=user_id, media_id=media_id)
        session.add(new_playlist)

        # Agregar al historial
        new_history = PlaylistHistory(user_id=user_id, media_id=media_id, date_playlist=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        session.add(new_history)

        session.commit()
        session.close()
        return redirect(url_for('display_playlists'))

    return render_template('add_playlist.html')



# Función para actualizar una playlist
@app.route('/update_playlist/<int:playlist_id>', methods=['GET', 'POST'])
def update_playlist(playlist_id):
    session = Session()
    playlist = session.query(Playlist).filter_by(id_playlist=playlist_id).first()

    if request.method == 'POST':
        new_title = request.form.get('title')
        user_id = request.form.get('user_id')

        # Validar user_id
        if user_id and user_id.isdigit():
            user_id = int(user_id)  # Convertir user_id a entero
            playlist.user_id = user_id  # Actualizar el user_id en la playlist

        if playlist:
            playlist.title = new_title
            session.commit()
            session.close()
            return redirect(url_for('display_playlists'))
        else:
            session.close()
            abort(404)

    session.close()
    return render_template('update_playlist.html', playlist=playlist)


# Función para eliminar una playlist
@app.route('/delete_playlist/<int:playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    session = Session()
    playlist = session.query(Playlist).filter_by(id_playlist=playlist_id).first()

    if playlist:
        session.delete(playlist)
        session.commit()

        # Removing playlist from PlaylistHistory
        session.query(PlaylistHistory).filter_by(user_id=playlist.user_id).delete()
        session.commit()

        session.close()
        return redirect(url_for('display_playlists'))
    else:
        session.close()
        abort(404)

# Función para mostrar todas las playlists
@app.route('/playlist')
def display_playlists():
    session = Session()
    playlists = session.query(Playlist).all()
    session.close()
    return render_template('display_playlist.html', playlists=playlists)

# Función para ver los detalles de una playlist
@app.route('/playlist/<int:playlist_id>')
def playlist_details(playlist_id):
    session = Session()
    playlist = session.query(Playlist).filter_by(id_playlist=playlist_id).first()
    session.close()
    
    if playlist:
        return render_template('playlist_details.html', playlist=playlist)
    else:
        abort(404)

# Función para guardar historial
@app.route('/add_to_history/<int:media_id>', methods=['POST'])
def add_to_history(media_id):
    user_id = request.form.get('user_id')
    
    if not user_id:
        return abort(400, description="User ID is required.")

    session = Session()
    new_history = PlaylistHistory(user_id=user_id, media_id=media_id, date_playlist=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    session.add(new_history)
    session.commit()
    session.close()
    return redirect(url_for('display_media'))

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
