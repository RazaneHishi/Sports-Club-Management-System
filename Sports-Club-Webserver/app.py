from turtle import st
from flask import Flask, jsonify, render_template, redirect, url_for, session, request, abort, flash
import functions
import sqlite3
import datetime
import json
from datetime import date
from copy import deepcopy
# THE BELOW WAS ADDED BY MEL FOR IMAGE UPLOAD
import os
import urllib.request
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "uehwr3493423j4j239k@#323i213ji3123"


# --------------------------- HOMEPAGE ---------------------------

@app.route('/')
def main():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    if 'cart' not in session:
        session['cart'] = {}
    if 'total' not in session:
        session['total'] = 0
    return render_template('HomePage.html', user=user, role=role)


@app.route('/', methods=['POST'])
def addVideo():

    return (redirect(url_for('main')))


def deleteVideo():
    return (redirect(url_for('main')))


def editVideo():
    return (redirect(url_for('main')))
# --------------------------- LOGIN + SIGNUP + LOGOUT ---------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('main'))
    elif request.method == 'POST':
        user = request.form["userName"]
        password = request.form["password"]
        ret = functions.authenticate(user, password)
        if ret == 1:
            return render_template('login.html', error="Username does not exist!")
        elif ret == 2:
            return render_template('login.html', error="Incorrect Password!")
        elif ret == 'FAN' or ret == 'PLAYER' or ret == 'ADMIN':
            session['user'] = user
            session['role'] = ret
            session['cart'] = {}
        return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('main'))
    if request.method == 'POST':
        name = request.form["Name"]
        user = request.form["userName"]
        password = request.form["password"]
        ret = functions.register(name, user, password)
        if ret == 1:
            return render_template('signup.html', error="Username already exists!")
        elif ret == 0:
            session['user'] = user
            session['role'] = 'FAN'
            return redirect(url_for('main'))
    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('main'))


# --------------------------- NEWS ---------------------------


@app.route('/news', methods=['GET', 'POST'])
def getNews():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""

    articles = functions.getArticles()

    if request.method == 'POST':
        if 'readbut' in request.form:
            return redirect(url_for('getArticle', anum=request.form['readbut']))
        elif 'editbut' in request.form:
            return redirect(url_for('editArticle', anum=request.form['editbut']))
        elif 'delbut' in request.form:
            return redirect(url_for('delArticle', anum=request.form['delbut']))
    return render_template('news.html', user=user, role=role, articles=articles, num=len(articles))


@app.route('/news/add', methods=['GET', 'POST'])
def addArticle():
    if 'user' in session:
        user = session['user']
        role = session['role']
        if role != 'ADMIN':
            return redirect(url_for('main'))
        if request.method == 'POST':
            title = request.form['title']
            headline = request.form['headline']
            body = request.form['body']
            functions.addArticle(title, headline, body)
            return redirect(url_for('getNews'), code=303)
        return render_template('addarticle.html', user=user, role=role)
    else:
        return redirect(url_for('main'))


@app.route('/news/article/<anum>', methods=['GET'])
def getArticle(anum):
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    article = functions.getArticle(anum)
    return render_template('article.html', user=user, role=role, article=article)


@app.route('/news/article/edit/<anum>', methods=['GET', 'POST'])
def editArticle(anum):
    if 'user' in session:
        user = session['user']
        role = session['role']
        if role != 'ADMIN':
            return redirect(url_for('main'))
        if request.method == 'POST':
            title = request.form['title']
            headline = request.form['headline']
            body = request.form['body']
            functions.updateArticle(anum, title, headline, body)
            return redirect(url_for('getNews'), code=303)
        article = functions.getArticle(anum)
        return render_template('editarticle.html', user=user, role=role, article=article, anum=anum)
    else:
        return redirect(url_for('main'))


@app.route('/news/article/del/<anum>', methods=['GET', 'POST'])
def delArticle(anum):
    print("HERE IS ", anum)
    if 'user' in session:
        user = session['user']
        role = session['role']
        if role != 'ADMIN':
            return redirect(url_for('main'))
        functions.delArticle(anum)
        return redirect(url_for('getNews'), code=303)
    else:
        return redirect(url_for('main'))

# --------------------------- TEAMS ---------------------------


@app.route('/teams/<team>')
def getTeam(team):
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    if team == "womenfb":
        players = functions.getPlayers(team)
        return(render_template('womenfb.html', user=user, role=role, players=players))
    elif team == "womenbb":
        players = functions.getPlayers(team)
        return(render_template('womenbb.html', user=user, role=role, players=players))
    elif team == "menfb":
        players = functions.getPlayers(team)
        return(render_template('menfb.html', user=user, role=role, players=players))
    elif team == "menbb":
        players = functions.getPlayers(team)
        return(render_template('menbb.html', user=user, role=role, players=players))

    return(redirect(url_for('main')))


@app.route('/<team>/addPlayer', methods=['POST'])
def addPlayer(team):
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None

    name = request.form["playerNameAdd"]
    age = request.form["playerAgeAdd"]
    position = request.form["playerPositionAdd"]
    points = request.form["playerPointsAdd"]
    assists = request.form["playerAssistsAdd"]

    if team == "womenfb":
        players = functions.getPlayers(team)
        functions.addPlayerWomenfb(name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "womenbb":
        players = functions.getPlayers(team)
        functions.addPlayerWomenbb(name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "menfb":
        players = functions.getPlayers(team)
        functions.addPlayerMenfb(name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "menbb":
        players = functions.getPlayers(team)
        functions.addPlayerMenbb(name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    return(redirect(url_for('main')))


@app.route('/<team>/deletePlayer', methods=['POST'])
def deletePlayer(team):
    if 'user' in session:
        user = session['user']
    else:
        user = None

    playerid = request.form["playerIdDelete"]

    if team == "womenfb":
        players = functions.getPlayers(team)
        functions.deletePlayer(playerid)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "womenbb":
        players = functions.getPlayers(team)
        functions.deletePlayer(playerid)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "menfb":
        players = functions.getPlayers(team)
        functions.deletePlayer(playerid)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "menbb":
        players = functions.getPlayers(team)
        functions.deletePlayer(playerid)
        return(redirect(url_for('getTeam', team=team)))

    return(redirect(url_for('main')))


@app.route('/<team>/editPlayer', methods=['POST'])
def editPlayer(team):

    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None

    id = request.form["playerIdEdit"]
    name = request.form["playerNameEdit"]
    age = request.form["playerAgeEdit"]
    position = request.form["playerPositionEdit"]
    points = request.form["playerPointsEdit"]
    assists = request.form["playerAssistsEdit"]

    if team == "womenfb":
        players = functions.getPlayers(team)
        functions.editPlayerWomenfb(id, name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "womenbb":
        players = functions.getPlayers(team)
        functions.editPlayerWomenbb(id, name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "menfb":
        players = functions.getPlayers(team)
        functions.editPlayerMenfb(id, name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    elif team == "menbb":
        players = functions.getPlayers(team)
        functions.editPlayerMenbb(id, name, age, position, points, assists)
        return(redirect(url_for('getTeam', team=team)))

    return(redirect(url_for('main')))


@app.route('/<team>/<string:userid>', methods=['POST'])
def processUserID(userid, team):

    userid = json.loads(userid)
    id = userid
    print(id)
    return(redirect(url_for('getTeam', team=team, id=id)))
# --------------------------- FIXTURES ---------------------------


@app.route('/fixtures')
def getFixtures():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ''
    team = request.args.get('team')
    if team is None:
        team = 'womenbb'
    today = date.today()
    standing = functions.getStanding(team)
    games = functions.getGames()
    return render_template('fixtures.html', user=user, role=role, games=games, standing=standing, today=today)


@app.route('/addGame', methods=['POST'])
def addGames():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None

    sport = request.form["sportAdd"]
    club1 = request.form["club1Add"]
    club2 = request.form["club2Add"]
    homeScore = request.form["homeScoreAdd"]
    awayScore = request.form["awayScoreAdd"]
    date = request.form["dateAdd"]

    functions.addGames(sport, club1, club2, homeScore, awayScore, date)
    return(redirect(url_for('getFixtures')))


@app.route('/editGames', methods=['POST'])
def editGames():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
    ID = request.form["gameid"]
    sport = request.form["sportEdit"]
    club1 = request.form["club1Edit"]
    club2 = request.form["club2Edit"]
    homeScore = request.form["homeScoreEdit"]
    awayScore = request.form["awayScoreEdit"]
    date = request.form["dateEdit"]
    functions.editGames(ID, sport, club1, club2, homeScore, awayScore, date)
    return(redirect(url_for('getFixtures')))


@app.route('/deleteGames', methods=['POST'])
def deleteGames():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
    ID = request.form["deleteid"]
    functions.deleteGames(ID)
    return(redirect(url_for('getFixtures')))
# --------------------------- SHOP ---------------------------


@app.route('/shop', methods=['GET', 'POST'])
def getShop():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""

    items = functions.getItem()
    if request.method == 'POST':
        if 'addcartbut' in request.form:
            return redirect(url_for('addItemCart', itemid=request.form["itemid"]))

    return render_template('shop.html', user=user, role=role, items=items)


@app.route('/shop/additemcart/<itemid>')
def addItemCart(itemid):
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    dict = session['cart']
    if itemid not in dict:
        dict[itemid] = 1
    else:
        dict[itemid] += 1
    session['cart'] = dict
    print("in add item cart")
    print(session['cart'])
    return(redirect(url_for('getShop')))


@app.route('/shop/additem', methods=['POST'])
def addItem():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None

    name = request.form["itemNameAdd"]
    price = request.form["itemPriceAdd"]
    stock = request.form["itemStockAdd"]

    functions.addItem(name, stock, price)

    return(redirect(url_for('getShop')))


@app.route('/shop/deleteItem', methods=['POST'])
def deleteItem():
    if 'user' in session:
        user = session['user']
    else:
        user = None

    itemid = request.form["itemidRemove"]

    functions.deleteItem(itemid)

    return(redirect(url_for('getShop')))


@app.route('/shop/editItem', methods=['GET', 'POST'])
def editItem():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
    ID = request.form["item_id"]
    name = request.form['itemNameEdit']

    price = request.form['itemPriceEdit']
    stock = request.form['itemStockEdit']

    functions.editItem(ID, name, price, stock)
    return (redirect(url_for('getShop')))

# --------------------------- TICKETS ---------------------------


@app.route('/tickets', methods=['GET', 'POST'])
def getTicket():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""

    tickets = functions.getTicket()
    # print(tickets)
    if request.method == 'POST':
        if 'addticketcartbut' in request.form:
            return redirect(url_for('addTicketCart', ticketid=request.form["ticketid"]))
    return render_template('tickets.html', user=user, role=role, tickets=tickets)

# MILIA


@app.route('/tickets/addticketcart/<ticketid>')
def addTicketCart(ticketid):
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    dict = session['cart']
    if ticketid not in dict:
        dict[ticketid] = 1
    else:
        dict[ticketid] += 1
    session['cart'] = dict
    print(session['cart'])
    return(redirect(url_for('getTicket')))


@app.route('/ticket/addticket', methods=['POST'])
def addTicket():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""

    oppteam = request.form["oppTeamAdd"]
    tickettime = request.form["ticketTimeAdd"]
    arena = request.form["arenaAdd"]
    price = request.form["ticketPriceAdd"]
    stock = request.form["ticketStockAdd"]

    functions.addTicket(oppteam, tickettime, arena, price, stock)

    return(redirect(url_for('getTicket')))


@app.route('/ticket/deleteTicket', methods=['POST'])
def deleteTicket():
    if 'user' in session:
        user = session['user']
    else:
        user = None
        role = ""

    ticketid = request.form["ticketidRemove"]

    functions.deleteTicket(ticketid)

    return(redirect(url_for('getTicket')))


@app.route('/tickets/editTicket', methods=['GET', 'POST'])
def editTicket():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    ID = request.form["ticketid"]

    oppteam = request.form["oppTeamEdit"]
    tickettime = request.form["ticketTimeEdit"]
    arena = request.form["arenaEdit"]
    price = request.form["ticketPriceEdit"]
    stock = request.form["ticketStockEdit"]
    functions.editTicket(ID, oppteam, tickettime, arena, price, stock)
    return (redirect(url_for('getTicket')))

# --------------------------- CART + CHECKOUT ---------------------------


@app.route('/cart/checkout', methods=['GET', 'POST'])
def getCheckout():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    total = session['total']
    return render_template('checkout.html', user=user, role=role, total=total)


@app.route('/cart', methods=['GET', 'POST'])
def getCart():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    cartitems = []
    dict = session['cart']
    print(dict)
    for item in dict:
        cartitem = functions.getCartItem(item)
        amount = (dict[str(cartitem[0][0])],)
        cartitems.append(cartitem[0]+amount)
    print(cartitems)
    shopitems = []
    ticketitems = []
    total = 0
    for item in cartitems:
        if int(item[0]) < 0:
            ticketitems.append(item)
            total = total + int(item[4])*int(item[6])
        else:
            shopitems.append(item)
            total = total + int(item[2])*int(item[4])
    session['total'] = total

    print(ticketitems, shopitems)
    return render_template('cart.html', user=user, role=role, ticketitems=ticketitems, shopitems=shopitems, total=total, cartitems=cartitems)


@app.route('/cart/RemoveAll', methods=['POST'])
def RemoveAll():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    session['cart'] = {}
    return (redirect(url_for('getCart')))


@app.route('/cart/quantity', methods=['POST'])
def getQuantity():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    arr = session['cart']
    itemid = request.form['quantityitemid']
    quantity = request.form['quantity']
    print(quantity)
    price = 0
    for item in arr:
        if item[0] == itemid:
            price = item[4]

    tot = session['total']
    tot = tot + (quantity * price)
    session['total'] = tot

    print(session['total'])

    return (redirect(url_for('getCart')))


@app.route('/cart/update', methods=['POST'])
def updateCart():
    cartitems = []
    dict = session['cart']
    print(dict)
    for item in dict:
        cartitem = functions.getCartItem(item)
        amount = (dict[str(cartitem[0][0])],)
        cartitems.append(cartitem[0]+amount)
    print(cartitems)
    shopitems = []
    ticketitems = []
    strs = []
    for item in cartitems:
        if int(item[0]) < 0:
            ticketitems.append(item)
        else:
            shopitems.append(item)
        strs.append((item[0], str(item[0])+"quantity"))
    for x in strs:
        if x[1] in request.form:
            dict[str(x[0])] = request.form[x[1]]
    session['cart'] = dict
    return redirect(url_for('getCart'))
# --------------------------- PROFILE ---------------------------


@app.route('/profile')
def getProfile():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    return render_template('profile_edit_prof.html', user=user, role=role)


@app.route('/profile/settings')
def getProfileSetting():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    conn = sqlite3.connect('database/430Group4.db')
    cursor = conn.cursor()
    cursor.execute("select password from users WHERE username='" + user+"'")
    res = cursor.fetchall()[0][0]
    return render_template('profile_account_settings.html', user=user, role=role, oldpass=res)


@app.route('/profile/change', methods=['POST'])
def changeProfile():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        return redirect(url_for('main'))

    username = request.form['newuser']
    functions.changeUser(user, username)
    session['user'] = username
    return redirect(url_for('getProfile'))


@app.route('/profile/settings/change', methods=['POST'])
def changeProfileSetting():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        return redirect(url_for('main'))

    oldpassword = request.form['oldpwd']
    password = request.form['password']
    functions.changePassword(user, password)
    return redirect(url_for('getProfileSetting'))


# --------------------------- HONORS FOOTBALL---------------------------

@app.route('/honorsfb', methods=['GET', 'POST'])
def getHonorsFB():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""

    trophies = []
    trophies = functions.getTrophyBS("football")
    today_year = date.today().year
    return render_template('honorsfb.html', user=user, role=role, trophies=trophies, today_year=today_year)


@app.route('/honorsfb/addTrophyF', methods=['POST'])
def addTrophyF():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    if role != 'ADMIN':
        return redirect(url_for('main'))
    title = request.form["title_add"]
    year = request.form["year_add"]
    functions.addTrophiesB(title, year, "football")
    return(redirect(url_for('getHonorsFB')))


@app.route('/honorsfb/deleteTrophyF', methods=['POST'])
def deleteTrophyF():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
    trophy_id = request.form["trophy_id_delete"]
    functions.deleteTrophyB(trophy_id, "football")
    return(redirect(url_for('getHonorsFB')))


@app.route('/honorsfb/editTrophyF', methods=['GET', 'POST'])
def editTrophyF():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
    ID = request.form["trophy_id"]
    title = request.form['titleEdit']
    year = request.form['yearEdit']
    functions.editTrophy(ID, title, year, "football")
    return (redirect(url_for('getHonorsFB')))


# --------------------------- HONORS BASKETBALL ---------------------------


@app.route('/honorsbb', methods=['GET', 'POST'])
def getHonorsBB():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    trophies = []
    trophies = functions.getTrophyBS("basketball")
    today_year = date.today().year
    return render_template('honorsbb.html', user=user, role=role, trophies=trophies, today_year=today_year)


# -------- UPLOAD ----------
UPLOAD_FOLDER = "static/uploads"
# THE BELOW WAS ADDED BY MEL FOR IMAGE UPLOAD
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('honorsbb.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/honorsbb/addTrophyB', methods=['POST'])
def addTrophyB():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""
    if role != 'ADMIN':
        return redirect(url_for('main'))
    title = request.form["title_add"]
    year = request.form["year_add"]
    trophyB = []
    for i in range(1, 6):
        trophyB.append(functions.getTrophyB(i, "basketball"))
    functions.addTrophiesB(title, year, "basketball")
    return(redirect(url_for('getHonorsBB')))


@app.route('/honorsbb/deleteTrophyB', methods=['POST'])
def deleteTrophyB():
    if 'user' in session:
        user = session['user']
    else:
        user = None
    trophy_id = request.form["trophy_id_delete"]
    functions.deleteTrophyB(trophy_id, "basketball")
    return(redirect(url_for('getHonorsBB')))


@app.route('/honorsbb/editTrophyB', methods=['GET', 'POST'])
def editTrophyB():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
    ID = request.form["trophy_id"]
    title = request.form['titleEdit']
    year = request.form['yearEdit']
    functions.editTrophy(ID, title, year, "basketball")
    return (redirect(url_for('getHonorsBB')))


'''@app.route('/honorsbb/editing', methods=['GET', 'GPOST'])
def showEdit():
    trophies_json = []
    trophies_json = functions.getTrophyBS("basketball")
    trophies_json=jsonify(trophies_json)
    return (redirect(url_for('getHonorsBB')))'''
# -------------------------- COMMUNITY -------------------------------


@app.route('/community', methods=['GET', 'POST'])
def getCommunity():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""

    posts = functions.getPosts()
    return render_template('community.html', user=user, role=role, posts=posts)


@app.route('/community/addPost', methods=['POST'])
def postCommunity():
    if 'user' in session:
        user = session['user']
        role = session['role']
    else:
        user = None
        role = ""

    if user is not None:
        dateposted = datetime.datetime.now().date()
        body = request.form['body']
        functions.addPost(user, dateposted, body)

    return(redirect(url_for('getCommunity')))


@app.route('/community/clearPosts', methods=['GET', 'POST'])
def delCommunity():
    if 'user' in session:
        user = session['user']
        role = session['role']
        if role != 'ADMIN':
            return(redirect(url_for('getCommunity')))
    else:
        return(redirect(url_for('getCommunity')))

    functions.deletePosts()
    return(redirect(url_for('getCommunity')))


if __name__ == "__main__":
    app.run(debug=True)
