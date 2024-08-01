from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/joy_of_painting'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models

class Episode(db.Model):
    __tablename__ = 'episodes'
    episode_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    painting_img_src = db.Column(db.String(255))
    painting_yt_src = db.Column(db.String(255))
    air_date = db.Column(db.Date)

class Color(db.Model):
    __tablename__ = 'colors'
    color_id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(255), nullable=False)
    color_hex = db.Column(db.String(255), nullable=False)

class SubjectMatter(db.Model):
    __tablename__ = 'subject_matters'
    subject_matter_id = db.Column(db.Integer, primary_key=True)
    subject_matter_name = db.Column(db.String(255), nullable=False)

class EpisodeColor(db.Model):
    __tablename__ = 'episode_colors'
    episode_color_id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.episode_id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.color_id'), nullable=False)

class EpisodeSubjectMatter(db.Model):
    __tablename__ = 'episode_subject_matters'
    episode_subject_matter_id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.episode_id'), nullable=False)
    subject_matter_id = db.Column(db.Integer, db.ForeignKey('subject_matters.subject_matter_id'), nullable=False)

# Helper function to convert query results to dictionary
def query_to_dict(query_result):
    return [dict(row) for row in query_result]

# API Endpoints

@app.route('/episodes', methods=['GET'])
def get_episodes():
    month = request.args.get('month')
    subjects = request.args.getlist('subject')
    colors = request.args.getlist('color')
    filter_type = request.args.get('filter_type', 'all')  # 'all' or 'any'
    
    query = db.session.query(Episode).distinct()

    if month:
        query = query.filter(db.extract('month', Episode.air_date) == int(month))

    if subjects:
        subject_query = db.session.query(Episode).join(EpisodeSubjectMatter).join(SubjectMatter).filter(SubjectMatter.subject_matter_name.in_(subjects))
        if filter_type == 'all':
            query = query.intersect(subject_query)
        else:
            query = query.union(subject_query)

    if colors:
        color_query = db.session.query(Episode).join(EpisodeColor).join(Color).filter(Color.color_name.in_(colors))
        if filter_type == 'all':
            query = query.intersect(color_query)
        else:
            query = query.union(color_query)

    episodes = query_to_dict(query.all())

    return jsonify(episodes)

if __name__ == "__main__":
    app.run(debug=True)
