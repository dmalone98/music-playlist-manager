from flask import Flask, flash, render_template, request, redirect, url_for
from db.db import db, Song, Playlist
import os

app = Flask(__name__)
app.secret_key = 'mpm-app-MMXXIII' 

# Get the project's root directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database and specify the path to the database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'music_manager.db')

db.init_app(app)

# Used once to create the database
#with app.app_context():
#    db.create_all()

@app.route('/')
def index():
    songs = Song.query.all()  # Retrieve all songs from the database
    return render_template('index.html', songs=songs)

from flask import request, redirect, url_for

from flask import render_template

##########
# Songs
##########

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    song = None
    form_action = '/add_song'
    action_text = 'Add'

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        duration = request.form['duration']

        # Create a new Song instance and add it to the database
        new_song = Song(title=title, artist=artist, duration=duration)
        db.session.add(new_song)
        db.session.commit()

        #flash('Song added successfully', 'success')
        return redirect(url_for('index'))  # Redirect to the index page after adding the song
    else:
        return render_template('song_form.html', song=song, form_action=form_action, action_text=action_text)

    
@app.route('/edit_song/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    # Fetch the song from the database using song_id
    song = Song.query.get_or_404(song_id)
    form_action = f'/edit_song/{song_id}'
    action_text = 'Update'

    if request.method == 'POST':
        # Handle form submission with updated song details
        song.title = request.form['title']
        song.artist = request.form['artist']
        song.duration = request.form['duration']

        # Save the changes to the database
        db.session.commit()

        flash('Song updated successfully', 'success')
        return redirect(url_for('index'))  # Redirect to the index page after adding the song
    else:
        return render_template('song_form.html', song=song, form_action=form_action, action_text=action_text)
    
@app.route('/delete_song/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    if song:
        db.session.delete(song)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)