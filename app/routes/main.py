from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from app.models.models import Game, Genre, Review
from app.forms.customer_forms import GameSearchForm
from sqlalchemy import func
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Get featured games (highest rated)
    featured_games = db.session.query(
        Game,
        func.coalesce(func.avg(Review.rating), 0).label('avg_rating')
    ).outerjoin(Review).group_by(Game).order_by(
        func.coalesce(func.avg(Review.rating), 0).desc()
    ).limit(6).all()

    # Get latest games
    latest_games = Game.query.order_by(Game.release_year.desc()).limit(6).all()

    # Get all genres for navigation
    genres = Genre.query.all()

    return render_template('main/index.html',
                         featured_games=featured_games,
                         latest_games=latest_games,
                         genres=genres)

@bp.route('/games')
def games():
    form = GameSearchForm(request.args)
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Populate genre choices
    genres = Genre.query.all()
    # Add genre attribute to form if missing
    if not hasattr(form, 'genre'):
        form.genre = None
    if hasattr(form, 'genre') and hasattr(form.genre, 'choices'):
        form.genre.choices = [('0', 'All Genres')] + [(str(g.id), g.name) for g in genres]

    # Base query
    query = Game.query

    # Apply filters
    if hasattr(form, 'search_query') and form.search_query:
        search = f"%{form.search_query}%"
        query = query.filter(Game.title.ilike(search))

    if hasattr(form, 'genre') and form.genre and form.genre != '0':
        query = query.filter(Game.genre_id == form.genre)

    if hasattr(form, 'min_price') and form.min_price is not None:
        query = query.filter(Game.price >= form.min_price)

    if hasattr(form, 'max_price') and form.max_price is not None:
        query = query.filter(Game.price <= form.max_price)

    # Apply sorting
    sort = request.args.get('sort', 'title_asc')
    if sort == 'title_asc':
        query = query.order_by(Game.title.asc())
    elif sort == 'title_desc':
        query = query.order_by(Game.title.desc())
    elif sort == 'price_asc':
        query = query.order_by(Game.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Game.price.desc())
    elif sort == 'release_year_desc':
        query = query.order_by(Game.release_year.desc())
    elif sort == 'release_year_asc':
        query = query.order_by(Game.release_year.asc())
    elif sort == 'rating_desc':
        query = query.join(Review).group_by(Game.id).order_by(func.avg(Review.rating).desc())

    # Execute query with pagination
    games = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('main/games.html',
                         games=games,
                         form=form,
                         current_sort=sort)



@bp.route('/games/<int:id>')
def game_detail(id):
    game = Game.query.get_or_404(id)
    
    # Get average rating
    avg_rating = db.session.query(func.avg(Review.rating)).filter(
        Review.game_id == id
    ).scalar() or 0
    
    # Get reviews with customer info
    reviews = Review.query.filter_by(game_id=id).order_by(
        Review.review_date.desc()
    ).all()
    
    # Get similar games (same genre)
    similar_games = Game.query.filter(
        Game.genre_id == game.genre_id,
        Game.id != game.id
    ).limit(4).all()

    return render_template('main/game_detail.html',
                         game=game,
                         avg_rating=round(avg_rating, 1),
                         reviews=reviews,
                         similar_games=similar_games)

@bp.route('/genre/<int:id>')
def genre_games(id):
    genre = Genre.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    games = Game.query.filter_by(genre_id=id).paginate(page=page, per_page=12)
    return render_template('main/genre_games.html',
                         genre=genre,
                         games=games)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.games'))

    games = Game.query.filter(
        Game.title.ilike(f'%{query}%')
    ).all()

    return render_template('main/search_results.html',
                         games=games,
                         query=query)

@bp.route('/api/games/search')
def api_search_games():
    query = request.args.get('q', '')
    games = Game.query.filter(
        Game.title.ilike(f'%{query}%')
    ).limit(5).all()
    
    return jsonify([{
        'id': game.id,
        'title': game.title,
        'price': float(game.price),
        'image_url': game.image_url
    } for game in games])
