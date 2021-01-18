#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
import logging
from datetime import datetime
from logging import Formatter, FileHandler
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
)
from flask_moment import Moment
from flask_wtf import Form
from forms import (
    ShowForm,
    VenueForm,
    ArtistForm,
)
from sqlalchemy import cast, Date
from flask_migrate import Migrate
from models import (
    db,
    Venue,
    Artist,
    Show,
)


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app: Flask = Flask(__name__)
moment: Moment = Moment(app)
app.config.from_object("config")
db.init_app(app)
migrate: Migrate = Migrate(app, db, compare_type=True)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value

    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

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
    # replace with real venues data.
    # num_shows should be aggregated based on number of upcoming shows per venue.

    # fetch all venue locations
    data = []
    venues = Venue.query.all()
    places = Venue.query.distinct(Venue.city, Venue.state).all()

    for place in places:
        data.append({
            "city": place.city,
            "state": place.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name,
            } for venue in venues if venue.city == place.city and venue.state == place.state],
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term')
    data = []
    response = {}

    # search venue by name
    # venues_found = db.session.query(Venue).filter(
    #     Venue.name.ilike(f"%{search_term}%")).all()

    # search venue by city and state
    try:
        city_term, state_term = search_term.split(', ')
        venues_found = db.session.query(Venue).filter(
            Venue.city.ilike(f"%{city_term}%")).filter(Venue.state.ilike(f"%{state_term}%")).all()
        for venue in venues_found:
            data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all()),
            })

        response = {
            "count": len(venues_found),
            "data": data,
        }
    except:
        flash(f"wrong format, should be 'city, state'")

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    data = []

    upcoming_shows = db.session.query(Show).join(Venue).join(Artist).filter(
        Show.venue_id == venue_id, Show.start_time > datetime.now()).all()
    past_shows = db.session.query(Show).join(Venue).join(Artist).filter(
        Show.venue_id == venue_id, Show.start_time < datetime.now()).all()

    upcoming_shows_info = []
    past_shows_info = []

    for show in upcoming_shows:
        upcoming_shows_info.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time,
        })

    for show in past_shows:
        past_shows_info.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time,
        })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows_info,
        "upcoming_shows": upcoming_shows_info,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # insert form data as a new Venue record in the db, instead
    # modify data to be the data object returned from db insertion
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    form = VenueForm(request.form, meta={"csrf": False})

    if form.validate_on_submit():
        try:
            venue: Venue = Venue()
            form.populate_obj(venue)
            db.session.add(venue)
            db.session.commit()
            # on successful db insert, flash success
            flash(f"Venue {request.form.get('name')} was successfully listed!")
        except ValueError as e:
            print(sys.exc_info())
            db.session.rollback()
            # on unsuccessful db insert, flash an error instead.
            flash(f"An error occurred: {str(e)}")
        finally:
            db.session.close()

    else:
        error_msg = []
        for field, error in form.errors.items():
            error_msg.append(f"{field}: {str(error)}")
        flash(f"Error occurred: {str(error_msg)}")

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
    # Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        # on successful db delete, flash success
        flash(f"Venue {venue_id} was successfully deleted!")
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # replace with real data returned from querying the database
    artists = Artist.query.order_by(Artist.id).all()
    data = []

    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term')
    data = []
    response = {}

    # search artist by name
    # artists_found = db.session.query(Artist).filter(
    #     Artist.name.ilike(f"%{search_term}%")).all()

    # search artist by city and state
    try:
        city_term, state_term = search_term.split(', ')
        artists_found = db.session.query(Artist).filter(
            Artist.city.ilike(f"%{city_term}%")).filter(Artist.state.ilike(f"%{state_term}%")).all()
        for artist in artists_found:
            data.append({
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": len(db.session.query(Show).filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all()),
            })

        response = {
            "count": len(artists_found),
            "data": data,
        }
    except:
        flash(f"wrong format, should be 'city, state'")

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # replace with real venue data from the venues table, using venue_id
    artist = Artist.query.get(artist_id)
    data = []

    upcoming_shows = db.session.query(Show).join(Venue).join(Artist).filter(
        Show.artist_id == artist_id, Show.start_time > datetime.now()).all()
    past_shows = db.session.query(Show).join(Venue).join(Artist).filter(
        Show.artist_id == artist_id, Show.start_time < datetime.now()).all()

    upcoming_shows_info = []
    past_shows_info = []

    for show in upcoming_shows:
        upcoming_shows_info.append({
            "venue_id": show.venue_id,
            "vanue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time,
        })

    for show in past_shows:
        past_shows_info.append({
            "venue_id": show.venue_id,
            "vanue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time,
        })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows_info,
        "upcoming_shows": upcoming_shows_info,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    # populate form with fields from artist with ID <artist_id>
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website.data = artist.website
    form.facebook_link.data = artist.facebook_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    try:
        artist = Artist.query.get(artist_id)

        artist.name = request.form.get('name')
        artist.genres = request.form.getlist('genres')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.website = request.form.get('website')
        artist.facebook_link = request.form.get('facebook_link')
        artist.seeking_venue = bool(request.form.get('seeking_venue'))
        artist.seeking_description = request.form.get('seeking_description')
        artist.image_link = request.form.get('image_link')

        db.session.commit()
        # on successful db update, flash success
        flash(f"Artist {artist_id} was successfully updated!")
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    venue = Venue.query.get(venue_id)

    # populate form with values from venue with ID <venue_id>
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.website.data = venue.website
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    try:
        venue = Venue.query.get(venue_id)

        venue.name = request.form.get('name')
        venue.genres = request.form.getlist('genres')
        venue.address = request.form.get('address')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.phone = request.form.get('phone')
        venue.website = request.form.get('website')
        venue.facebook_link = request.form.get('facebook_link')
        venue.seeking_talent = bool(request.form.get('seeking_talent'))
        venue.seeking_description = request.form.get('seeking_description')
        venue.image_link = request.form.get('image_link')

        db.session.commit()
        # on successful db update, flash success
        flash(f"Venue {venue_id} was successfully updated!")
    except:
        print(sys.exc_info())
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
    # called upon submitting the new artist listing form
    # insert form data as a new Venue record in the db, instead
    # modify data to be the data object returned from db insertion

    form = ArtistForm(request.form, meta={"csrf": False})

    if form.validate_on_submit():
        try:
            artist: Artist = Artist()
            form.populate_obj(artist)
            db.session.add(artist)
            db.session.commit()
            # on successful db insert, flash success
            flash(
                f"Artist {request.form.get('name')} was successfully listed!")
        except ValueError as e:
            print(sys.exc_info())
            db.session.rollback()
            # on unsuccessful db insert, flash an error instead.
            flash(f"An error occurred: {str(e)}")
        finally:
            db.session.close()

    else:
        error_msg = []
        for field, error in form.errors.items():
            error_msg.append(f"{field}: {str(error)}")
        flash(f"Error occurred: {str(error_msg)}")

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # replace with real venues data.
    # num_shows should be aggregated based on number of upcoming shows per venue.
    shows = db.session.query(Show).join(Venue).join(Artist).all()
    data = []

    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time,
            "end_time": show.end_time,
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/search', methods=['POST'])
def search_shows():
    search_term = request.form.get('search_term')
    search_date = datetime.today().date()

    try:
        search_date = datetime.strptime(search_term, '%Y-%m-%d')
    except:
        flash(f"wrong date format, should be yyyy-mm-dd, search for today's show")

    shows_found = db.session.query(Show).filter(
        cast(Show.start_time, Date) == search_date).all()
    data = []

    for show in shows_found:
        data.append({
            "id": show.id,
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time,
        })

    response = {
        "count": len(shows_found),
        "data": data,
    }

    return render_template('pages/search_shows.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # insert form data as a new Show record in the db, instead
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    form = ShowForm(request.form, meta={"csrf": False})

    if form.validate_on_submit():
        try:
            show: Show = Show()
            form.populate_obj(show)
            db.session.add(show)
            db.session.commit()
            # on successful db insert, flash success
            flash(f"A show was successfully listed!")
        except ValueError as e:
            print(sys.exc_info())
            db.session.rollback()
            # on unsuccessful db insert, flash an error instead.
            flash(f"An error occurred: {str(e)}")
        finally:
            db.session.close()

    else:
        error_msg = []
        for field, error in form.errors.items():
            error_msg.append(f"{field}: {str(error)}")
        flash(f"Error occurred: {str(error_msg)}")

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
