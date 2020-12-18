#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from collections import defaultdict
import json
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from commons import app, db, migrate, moment
from models import Venue, Artist, Show
import util as util


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.order_by('id').all()
  shows = Show.query.all()

  by_city_dict = defaultdict(list)

  for venue in venues:
    by_city_dict[f'{venue.city},{venue.state}'].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": util.count_number_of_shows_at_venue(venue.id, shows),
      })

  data = [{"city": city_state.split(',')[0], 
           "state": city_state.split(',')[1],
           "venues": venue_list}
          for city_state, venue_list in by_city_dict.items()]

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  name_pattern = request.form.get('search_term', '')
  venues = util.search_by_name_pattern(Venue, name_pattern)
  shows = Show.query.all()

  response={
    "count": len(venues),
    "data": [{
      "id": venue.id,
      "name":  venue.name,
      "num_upcoming_shows": util.count_number_of_shows_at_venue(venue.id, shows),
      } for venue in venues]}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  selected_venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()
  artists = Artist.query.all()

  past_shows = util.list_venue_past_shows(shows)
  past_shows_list = [util.format_show_info_for_venue(show, artists) for show in past_shows]

  upcoming_shows = util.list_venue_upcoming_shows(shows)
  upcoming_shows_list = [util.format_show_info_for_venue(show, artists) for show in upcoming_shows]

  data = {
    "id": selected_venue.id,
    "name": selected_venue.name,
    "genres": selected_venue.genres.split(','),
    "address": selected_venue.address,
    "city": selected_venue.city,
    "state": selected_venue.state,
    "phone": selected_venue.phone,
    "website": selected_venue.website,
    "facebook_link": selected_venue.facebook_link,
    "seeking_talent": selected_venue.seeking_talent,
    "seeking_description": selected_venue.seeking_description,
    "image_link": selected_venue.image_link,
    "past_shows": past_shows_list,
    "upcoming_shows": upcoming_shows_list,
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    venue = Venue(name=request.form.get('name'), 
                  genres=request.form.get('genres'),
                  address=request.form.get('address'),  
                  city=request.form.get('city'),
                  state=request.form.get('state'),
                  phone=request.form.get('phone'),
                  website=request.form.get('website'),
                  facebook_link=request.form.get('facebook_link'),
                  seeking_talent=util.boolean_str_to_bool(request.form.get('seeking_talent')),
                  seeking_description=request.form.get('seeking_description'),
                  image_link=request.form.get('image_link'))
    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.order_by('id').all()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  matching_artists = util.search_by_name_pattern(Artist, request.form.get('search_term', ''))
  shows = Show.query.all()
  
  artist_info_list = []
  for artist in matching_artists:
    upcoming_shows = util.artist_upcoming_shows(artist.id, shows)

    artist_info = {
    "id": artist.id,
    "name": artist.name,
    "num_upcoming_shows": len(upcoming_shows)
    }
    artist_info_list.append(artist_info)

  response={
    "count": len(matching_artists),
    "data": artist_info_list
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id).all()
  venues = Venue.query.all()

  past_shows = util.list_artist_past_shows(shows)
  upcoming_shows = util.list_artist_upcoming_shows(shows)

  artist_info={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(","),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [util.format_show_info_for_artist(show, venues) for show in past_shows],
    "upcoming_shows": [util.format_show_info_for_artist(show, venues) for show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=artist_info)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist={
    "id": artist_id,
    "name": request.form.get("name"),
    "genres": request.form.get("genres", "").split(","),
    "city": request.form.get("city"),
    "state": request.form.get("state"),
    "phone": request.form.get("phone"),
    "website": request.form.get("website"),
    "facebook_link": request.form.get("facebook_link"),
    "seeking_venue": util.boolean_str_to_bool(request.form.get("seeking_venue")),
    "seeking_description": request.form.get("seeking_description"),
    "image_link": request.form.get("image_link")
  }
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
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows_list = Show.query.order_by('start_time').all()

  data = []
  for show in shows_list:
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)
    data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": datetime_to_str(show.start_time)
      })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    new_show = Show(venue_id=request.form.get('venue_id'), 
                    artist_id=request.form.get('artist_id'), 
                    start_time=request.form.get('start_time'))
    db.session.add(new_show)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
    app.run(port=8002, debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
