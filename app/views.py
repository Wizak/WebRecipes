from app import app, db, render_template, request, Response, session
from app.models import User, Category, Recipe, Description

from sqlalchemy import desc
from fuzzywuzzy import fuzz


def search_query(search):
    recipe_query = Recipe.query.all() 
    titles = [r.title for r in recipe_query]
    orders = {title: fuzz.WRatio(search, title) for title in titles}
    sort_orders = sorted(orders.items(), key=lambda x: x[1], reverse=True)
    return sort_orders if len(sort_orders) <= 4 else sort_orders[:4]


def check_user(user_name):
    return User.query.filter(User.username == user_name).scalar() 


def check_recipe(title):
    return Recipe.query.filter(Recipe.title == title).scalar() 


def check_category(title):
    return Category.query.filter(Category.title == title).scalar() 


def add_user(*args):
    query_user = check_user(args[0])
    if not query_user:
        user = User(username=args[0], first_name=args[1], last_name=args[2], email=args[3], password=args[4])
        db.session.add(user)
        db.session.commit()
    else:
        return True


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        try:
            search = request.form['search']
            titles = search_query(search)
            return render_template('search.html', titles=titles)
        except KeyError:
            pass
    return render_template('edit.html')

    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        try:
            search = request.form['search']
            titles = search_query(search)
            return render_template('search.html', titles=titles)
        except KeyError:
            pass
    return render_template('edit.html')

    
def add_recipe(*args):
    query_recipe = check_recipe(args[0])
    query_user = check_user(args[1])
    query_category = check_category(args[2])
    print(f'{query_user = }, {query_category = }')
    if not query_recipe:
        recipe = Recipe(title=args[0], user_id=query_user.id, category_id=query_category.id)
        db.session.add(recipe)
        db.session.commit()
    else:
        return True


def add_description(*args):
    query_recipe = check_recipe(args[3])
    if query_recipe:
        description = Description(photo=args[0], components=args[1], description=args[2], recipe_id=query_recipe.id)
        db.session.add(description)
        db.session.commit()


def search_fav():
    fav_recipe = Recipe.query.order_by(desc(Recipe.likes)).all()
    fav_category = set(Category.query.filter(Category.id == r.category_id).one() for r in fav_recipe)
    slides = [{'category': c.title, 'description': c.subtitle} for c in fav_category]
    return slides


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            search = request.form['search']
            titles = search_query(search)
            return render_template('search.html', titles=titles)
        except KeyError:
            pass
    return render_template('home.html', slides=search_fav())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        if not all([user_name, first_name, last_name, email, password]):
            return render_template('register.html')
        check = add_user(
            user_name, 
            first_name, 
            last_name, 
            email, 
            password
        )
        if not check:
            return render_template('login.html')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        check = check_user(user_name)
        if check:
            if check.password == password:
                dictionar = {'user_name': user_name, 'password': password, 'authed_in': 'True', 'likes': ''}
                for key in dictionar:
                    session[key] = dictionar[key]
                return render_template('home.html', slides=search_fav())
    return render_template('login.html')


@app.route('/logout')
def logout():
    lister = ['user_name', 'password', 'authed_in', 'likes']
    for key in lister:
        session.pop(key, None)
    return render_template('home.html', slides=search_fav())


@app.route('/show', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        try:
            search = request.form['search']
            titles = search_query(search)
            return render_template('search.html', titles=titles)
        except KeyError:
            pass
    categorys = Category.query.all()
    cards = [{'title': c.title, 'subtitle': c.subtitle} for c in categorys]
    return render_template('show.html', cards=cards)


@app.route('/show/<title>', methods=['GET', 'POST'])
def show_category(title):
    if request.method == 'POST':
        try:
            search = request.form['search']
            titles = search_query(search)
            return render_template('search.html', titles=titles)
        except KeyError:
            pass
    cat_id = check_category(title).id
    rec_query = Recipe.query.filter_by(category_id=cat_id).all()
    recipes = [r.title for r in rec_query]
    return render_template('show_category.html', recipes=recipes)


@app.route('/recipe/<title>', methods=['GET', 'POST'])
def show_recipe(title):
    if request.method == 'POST':
        try:
            search = request.form['search']
            titles = search_query(search)
            return render_template('search.html', titles=titles)
        except KeyError:
            pass
    query_recipe = check_recipe(title)
    des_query = Description.query.filter_by(recipe_id=query_recipe.id).one()
    rid = str(query_recipe.id)
    cookies = session.get('likes')
    truth = None
    if cookies:
        cs = cookies.split()
        if rid in cs:
            truth = 'dislike'
        else:
            truth = 'like'   
    else:
        truth = 'like'       
    recipe = {
        'title': query_recipe.title,
        'likes': query_recipe.likes,
        'time': query_recipe.date_time.strftime('%B %d, %Ys'),
        'components': des_query.components.splitlines(),
        'description': des_query.description
        }
    if request.method == 'POST':
        title = request.form['title']
        if cookies:
            if rid in cs:
                query_recipe.likes -= 1
                db.session.add(query_recipe)
                db.session.commit()
                del cs[cs.index(rid)]
                truth = 'like' 
                cookies = ' '.join(cs)
                session.pop('likes', None)
                session['likes'] = cookies
                return render_template('show_recipe.html', recipe=recipe, truth=truth)
            else:
                query_recipe.likes += 1
                db.session.add(query_recipe)
                db.session.commit()
                truth = 'dislike' 
                cookies += f' {rid}'
                session.pop('likes', None)
                session['likes'] = cookies
                return render_template('show_recipe.html', recipe=recipe, truth=truth)    
        else:
            query_recipe.likes += 1
            db.session.add(query_recipe)
            db.session.commit()
            truth = 'dislike' 
            cookies += f' {rid}'
            session.pop('likes', None)
            session['likes'] = cookies
            return render_template('show_recipe.html', recipe=recipe, truth=truth)
    return render_template('show_recipe.html', recipe=recipe, truth=truth)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            search = request.form['search']
            titles = search_query(search)
            return render_template('search.html', titles=titles)
        except KeyError:
            pass
        title = request.form['title']
        components = request.form['components']
        description = request.form['description']
        category = request.form['category']
        photo = request.files['photo'].read()
        username = session.get('user_name')
        add_recipe(title, username, category)
        add_description(photo, components, description, title)
        return render_template('add.html')
    category_query = Category.query.all()
    categorys = [c.title for c in category_query]
    return render_template('add.html', categorys=categorys)


@app.route('/show_recipe/<title>')
def recipe_photo(title):
    query_recipe = Recipe.query.filter_by(title=title).one()
    query_desc = Description.query.filter_by(recipe_id=query_recipe.id).one()
    frame = query_desc.photo
    formating = (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(formating, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/show_category/<title>')
def category_photo(title):
    frame = Category.query.filter_by(title=title).one().photo
    formating = (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(formating, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/carousel_photo/<title>')
def carousel_photo(title):
    fav_recipe = Recipe.query.order_by(desc(Recipe.likes)).all()
    cs = [Category.query.filter(Category.id == r.category_id).one() for r in fav_recipe]
    for c in cs:
        if c.title == title:
            frame = c.photo
    formating = (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(formating, mimetype='multipart/x-mixed-replace; boundary=frame')
