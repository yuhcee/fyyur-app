#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
from flask import render_template, request, Response, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from flask_restful import abort
from flask_wtf import Form
from forms import *
from models import app, db, Artist, Venue, Show, format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():

    locations = db.session.query(Venue.city, Venue.state).distinct(
        Venue.city, Venue.state)
    data = []
    for area in locations:
        venues = Venue.query.filter(Venue.state == area.state).filter(
            Venue.city == area.city).all()

        venue_data = []

        for venue in venues:
            venue_data.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len(db.session.query(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all())
            })

            data.append({
                'city': area.city,
                'state': area.state,
                'venues': venue_data
            })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():

    search_term = request.form.get('search_term', '')
    search_result = db.session.query(Venue).filter(
        Venue.name.ilike(f'%{search_term}%')).all()
    count = len(search_result)

    response = {
        "count": count,
        "data": search_result
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    
    venue = Venue.query.filter(Venue.id == venue_id).first()

    past = Show.query.filter(Show.venue_id == venue_id).filter(
        Show.start_time < datetime.now()).join(Artist, Show.artist_id == Artist.id).add_columns(Artist.id, Artist.name, Artist.image_link, Show.start_time).all()

    upcoming = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
        Show.start_time > datetime.now()).join(Artist, Show.artist_id == Artist.id).add_columns(Artist.id, Artist.name, Artist.image_link, Show.start_time).all()

    upcoming_shows = []

    past_shows = []

    for show in upcoming:
        upcoming_shows.append({
            'artist_id': show[1],
            'artist_name': show[2],
            'artist_image_link': str(show[3]),
            'start_time': str(show[4])
        })

    for show in past:
        past_shows.append({
            'artist_id': show[1],
            'artist_name': show[2],
            'artist_image_link': show[3],
            'start_time': str(show[4])
        })

    if venue is None:
        abort(404)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": [venue.genres],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past),
        "upcoming_shows_count": len(upcoming),
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    if "seeking_talent" in request.form and request.form['seeking_talent'] == 'y':
        seeking_talent = True
    else:
        seeking_talent = False

    try:
        venue = Venue(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            website=request.form['website_link'],
            seeking_talent=seeking_talent,
            seeking_description=request.form['seeking_description']
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        print(e)
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    #  Artists
    #  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter(Venue.id == venue_id).first()

    form.city.data = venue.city
    form.name.data = venue.name
    form.phone.data = venue.phone
    form.state.data = venue.state
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.website_link.data = venue.website
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    form = VenueForm()
    venue_to_update = Venue.query.filter(Venue.id == venue_id).first()

    try:
        venue_to_update.name = form.name.data,
        venue_to_update.city = request.form['city']
        venue_to_update.state = request.form['state']
        venue_to_update.address = request.form['address']
        venue_to_update.phone = request.form['phone']
        venue_to_update.genres = request.form.getlist('genres')
        venue_to_update.image_link = request.form['image_link']
        venue_to_update.facebook_link = request.form['facebook_link']
        venue_to_update.website = request.form['website_link'],
        venue_to_update.seeking_talent = form.seeking_talent.data
        venue_to_update.seeking_description = request.form['seeking_description']

        db.session.add(venue_to_update)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully edited!')
    except Exception as e:
        print(e)
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be edited')
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    if "seeking_venue" in request.form and request.form['seeking_venue'] == 'y':
        seeking_venue = True
    else:
        seeking_venue = False

    try:
        artist = Artist(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            website=request.form['website_link'],
            seeking_venue=seeking_venue,
            seeking_description=request.form['seeking_description']
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        print(e)
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():

    shows = Show.query.join(Artist, Artist.id == Show.artist_id).join(
        Venue, Venue.id == Show.venue_id).all()

    data = []

    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=format_datetime(request.form['start_time'], 'full')
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception as e:
        print(e)
        flash('An error occurred. Show could not be listed')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
