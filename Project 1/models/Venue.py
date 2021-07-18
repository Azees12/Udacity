import datetime
from operator import itemgetter
from models import Show, Genre
from app import db, format_datetime


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    genres = db.relationship(
        'Genre', secondary=Genre.venue_genre_table, backref=db.backref('venues'))
    address = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(200))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(300), default="")
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue {self.id} name: {self.name}>'


def addVenue(name, city, state, address, phone, image_link, genres, facebook_link, seeking_description, website, seeking_talent):
    status = False
    try:
        print('here3')
        venue = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            seeking_description=seeking_description,
            website=website,
            seeking_talent=seeking_talent)

        # Checking if the genre exists if not creating it.
        for genre in genres:
            IsGenre = Genre.Genre.query.filter_by(name=genre).one_or_none()
            if IsGenre:
                venue.genres.append(IsGenre)
            else:
                newGenre = Genre.Genre(name=genre)
                print(newGenre.name)
                db.session.add(newGenre)
                venue.genres.append(newGenre)

        db.session.add(venue)
        db.session.commit()

        status = True

    except:
        db.session.rollback()
    finally:
        db.session.close()
        return status


def getVenues():

    venues = Venue.query.all()

    data = []   # dict of venues where city, state and venues are keys

    # Creating a set of unique combitions of citys and states
    cities_states = set()
    for venue in venues:
        cities_states.add((venue.city, venue.state))  # Add tuple

    # Ordering the set of city states
    cities_states = list(cities_states)
    cities_states.sort(key=itemgetter(1, 0))   # Order by By state then city

    now = datetime.date.today()    # Date to be compared

    # Adding the venues to the approaiate city state
    for loc in cities_states:
        venues_list = []
        for venue in venues:
            if (venue.city == loc[0]) and (venue.state == loc[1]):

                # Upcoming showws check.
                venue_shows = Show.Show.query.filter_by(
                    venue_id=venue.id).all()
                num_upcoming = 0
                for show in venue_shows:
                    if show.start_time > now:
                        num_upcoming += 1

                venues_list.append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": num_upcoming
                })

        data.append({
            "city": loc[0],
            "state": loc[1],
            "venues": venues_list
        })

    return data


def getVenue(venue_id):
    venue = Venue.query.get(venue_id)
    shows = venue.shows

    past_shows = []  # dictionary of all artists shows

    upcoming_shows = []  # dictionary of all artists shows that have not yet passed occured

    current_time = datetime.datetime.now()

    # Sorting artists shows based on todays date
    for show in shows:
        data = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
        }
        if show.start_time > current_time:
            upcoming_shows.append(data)
        else:
            past_shows.append(data)

    genres = [genre.name for genre in venue.genres]  # Extracting genre names

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres,
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
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return data


def getSearchV(search):
    # Querying Search term
    venues = Venue.query.filter(Venue.name.ilike(f'%{search}%'))
    data = {
        "count": venues.count(),
        "data": venues
    }
    return data


def editVenue(id, name, genres, city, state, address, phone, facebook, website, image, seeking_t, seeking_d):
    status = False

    try:
        venue = Venue.query.get(id)
        venue.name = name
        venue.genres = genres
        venue.city = city
        venue.state = state
        venue.address = address
        venue.phone = phone
        venue.facebook_link = facebook
        venue.website = website
        venue.image_link = image
        venue.seeking_talent = seeking_t
        venue.seeking_description = seeking_d
        db.session.commit()
        status = True

        venue.genres = []

        # Checking if the genre exists if not creating it.
        for genre in genres:
            IsGenre = Genre.query.filter_by(name=genre).one_or_none()
            if IsGenre:
                venue.genres.append(IsGenre)
            else:
                Genre.addGenre(genre)
                venue.genres.append(IsGenre)
    except:
        db.session.rolllback()
    finally:
        db.session.close()
        return status
