import datetime as dt


def search_by_name_pattern(class_obj, name_pattern):
	search = "%{}%".format(name_pattern)
	matching_obj_list = class_obj.query.filter(class_obj.name.like(search)).order_by('id').all()
	return matching_obj_list


def count_number_of_shows_at_venue(venue_id, shows):
	return len([show for show in shows if show.venue_id == venue_id])


def list_past_shows(venue_id, shows, timestamp=None):
	timestamp = None or dt.datetime.utcnow()
	past_shows = [show for show in shows 
				  if show.venue_id == venue_id and show.start_time < timestamp]
	return past_shows


def list_upcoming_shows(venue_id, shows, timestamp=None):
	timestamp = None or dt.datetime.utcnow()
	upcoming_shows = [show for show in shows 
					  if show.venue_id == venue_id and show.start_time >= timestamp]
	return upcoming_shows

def _find_matching_artist(artist_id, artists):
	for artist in artists:
		if artist.id == artist_id:
			return artist


def datetime_to_str(datetime_obj, format="%Y-%m-%dT%H:%M:%S.%fZ"):
	return datetime_obj.strftime(format)


def format_show_info(show, artists):
	artist = _find_matching_artist(show.artist_id, artists)
	show_info = {
		"artist_id": show.artist_id,
		"artist_name": artist.name,
		"artist_image_link": artist.image_link,
		"start_time": datetime_to_str(show.start_time)
		}
	return show_info
