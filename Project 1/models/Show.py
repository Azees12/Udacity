from app import db, format_datetime


class Show (db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>'


def getShows():
    data = []
    shows = Show.query.all()

    for show in shows:

        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
        })

    return data


def createShow(artist_id, venue_id, time):
    status = False
    try:
        show = Show(
            artist_id=artist_id,
            venue_id=venue_id,
            start_time=time
        )
        db.session.add(show)
        db.session.commit()
        status = True
    except:
        db.session.rollback()
    finally:
        return status
