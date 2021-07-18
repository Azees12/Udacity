import datetime
from sqlalchemy.orm import backref
from models import Genre,Show
from app import db, format_datetime


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship(
        'Genre', secondary=Genre.artist_genre_table, backref=db.backref('artists'))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(200))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(300), default="")
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist {self.id} name: {self.name}>'


def getArtists():
    data = []
    artists = Artist.query.all()

    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

    return data


def getArtist(id):
    artist = Artist.query.get(id)
    current_time = datetime.datetime.now()

    shows_upcoming = Show.Show.query.join(Artist).filter(Artist.id == id).filter(Show.Show.start_time  > current_time)
    shows_past = Show.Show.query.join(Artist).filter(Artist.id == id).filter(Show.Show.start_time  < current_time )
       
    upcoming_shows = []
    past_shows  = []

    for shows in shows_upcoming:
        data = {
            "venue_id": shows.venue_id,
            "venue_name": shows.venue.name,
            "venue_image_link": shows.venue.image_link,
            "start_time": format_datetime(str(shows.start_time))
        }
        upcoming_shows.append(data)

    for shows in shows_past:
        data = {
            "venue_id": shows.venue_id,
            "venue_name": shows.venue.name,
            "venue_image_link": shows.venue.image_link,
            "start_time": format_datetime(str(shows.start_time))
        }
        past_shows.append(data)


    genres = [genre.name for genre in artist.genres]

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }
    return data


def getArtistS(search):
    artists = Artist.query.filter(Artist.name.ilike(f'%{search}%'))

    data = {
        "count": artists.count(),
        "data": artists
    }

    return data


def editArtist(id, name, phone, state, city, genres, image, facebook):
    status = False
    try:
        artist = Artist.query.get(id)
        artist.name = name
        artist.phone = phone
        artist.state = state
        artist.city = city
        artist.image_link = image
        artist.facebook_link = facebook
        db.session.commit()
        status = True

        artist.genres = []

        # Checking if the genre exists if not creating it.
        for genre in genres:
            IsGenre = Genre.Genre.query.filter_by(name=genre).one_or_none()
            if IsGenre:
                artist.genres.append(IsGenre)
            else:
                Genre.Genre.addGenre(genre)
                artist.genres.append(IsGenre)
    except:
        db.session.rollback()

    finally:
        db.session.close()
        return status


def addArtist(name, phone, state, city, genres, image, facebook, seeking_venue, seeking_description, website):
    status = False
    print(name, phone, state, city, genres, image, facebook,
          seeking_venue, seeking_description, website)
    try:

        artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,

            website=website,
            image_link=image,
            facebook_link=facebook)

        print(genres)
        for genre in genres:
            IsGenre = Genre.Genre.query.filter_by(name=genre).one_or_none()

            if IsGenre:

                artist.genres.append(IsGenre)

            else:
                newGenre = Genre.Genre(name=genre)
                print(newGenre.name)
                db.session.add(newGenre)
                artist.genres.append(newGenre)

        db.session.add(artist)
        db.session.commit()
        status = True

    except:
        db.session.rollback()
    finally:
        db.session.close()
        return status


def removeArtist(id):
    status = False
    try:
        artist = Artist.query.get(id)
        db.session.delete(artist)
        db.session.commit()
        status = True
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return status
