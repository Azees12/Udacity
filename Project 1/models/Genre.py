from app import db


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


def addGenre(name):
    newGenre = Genre(name=name)
    db.session.add(newGenre)


artist_genre_table = db.Table('artist_genre_table',
                              db.Column('genre_id', db.Integer, db.ForeignKey(
                                  'Genre.id'), primary_key=True),
                              db.Column('artist_id', db.Integer, db.ForeignKey(
                                  'Artist.id'), primary_key=True)
                              )

venue_genre_table = db.Table('venue_genre_table',
                             db.Column('genre_id', db.Integer, db.ForeignKey(
                                 'Genre.id'), primary_key=True),
                             db.Column('venue_id', db.Integer, db.ForeignKey(
                                 'Venue.id'), primary_key=True)
                             )
