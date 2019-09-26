import os
import sys


try:
    from flask import Flask, render_template, redirect, request, url_for
    import requests
    from pymongo import MongoClient
    from bson.objectid import ObjectId
except (ImportError, ModuleNotFoundError) as e:
    print(e, file=sys.stderr)
    print('\x1b[1;31m' + "run pipenv install 'moduleName' " + '\x1b[0m')


os.environ['FLASK_ENV'] = 'development'  # set flask envoirnment variable

app = Flask(__name__)
mongodb_uri = os.getenv(
    'MONGODB_URI', default='mongodb://localhost:27017/playlister')
host = os.environ.get('MONGODB_URI')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
playlists = db.playlists


@app.route('/', methods=['GET'])
def playlists_index():
    """ Show all playlists
    @GET:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
    return render_template('playlists_index.html', playlists=playlists.find())


@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """ Submit a new playlist
    @POST:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/new')
def playlists_new():
    """ Create a new playlist
    @POST:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
    return render_template('playlists_new.html', playlist={}, title='New Playlist')


@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """ Show a single playlist
    @GET:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """ Submit an edited playlist
    @POST:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """ Show the edit form for a playlist.
    @GET:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')


@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """ Delete a playlist
    @GET:
        description:
        responses:
            200:
                description: 
            400:
                description:
    """
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
