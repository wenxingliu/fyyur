import datetime as dt


def search_by_name_pattern(class_obj, name_pattern):
	search = "%{}%".format(name_pattern)
	matching_obj_list = class_obj.query.filter(class_obj.name.like(search)).order_by('id').all()
	return matching_obj_list


def count_number_of_shows_at_venue(venue_id, shows):
	return len([show for show in shows if show.venue_id == venue_id])


def list_venue_past_shows(shows, timestamp=None):
	timestamp = None or dt.datetime.utcnow()
	past_shows = [show for show in shows if show.start_time < timestamp]
	return past_shows


def list_venue_upcoming_shows(shows, timestamp=None):
	timestamp = None or dt.datetime.utcnow()
	upcoming_shows = [show for show in shows if show.start_time >= timestamp]
	return upcoming_shows


def list_artist_upcoming_shows(shows, timestamp=None):
	timestamp = None or dt.datetime.utcnow()
	upcoming_shows = [show for show in shows if show.start_time >= timestamp]
	return upcoming_shows


def list_artist_past_shows(shows, timestamp=None):
	timestamp = None or dt.datetime.utcnow()
	past_shows = [show for show in shows if show.start_time < timestamp]
	return past_shows


def find_matching_artist(artist_id, artists):
	for artist in artists:
		if artist.id == artist_id:
			return artist


def find_matching_venue(venue_id, venues):
	for venue in venues:
		if venue.id == venue_id:
			return venue


def datetime_to_str(datetime_obj, format="%Y-%m-%dT%H:%M:%S.%fZ"):
	return datetime_obj.strftime(format)


def format_show_info_for_venue(show, artists):
	artist = find_matching_artist(show.artist_id, artists)
	show_info = {
		"artist_id": show.artist_id,
		"artist_name": artist.name,
		"artist_image_link": artist.image_link,
		"start_time": datetime_to_str(show.start_time)
		}
	return show_info


def format_show_info_for_artist(show, venues):
	venue = find_matching_venue(show.venue_id, venues)
	show_info = {
		"venue_id": show.venue_id,
		"venue_name": venue.name,
		"venue_image_link": venue.image_link,
		"start_time": datetime_to_str(show.start_time)
		}
	return show_info


def boolean_str_to_bool(bool_str) -> bool:
	if bool_str == 'Yes':
		return True
	else:
		return False

def bool_to_boolean_str(bool_val: bool):
	if bool_val:
		return "Yes"
	else:
		return "No"
