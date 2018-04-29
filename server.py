from flask import Flask,render_template,request,url_for, session, flash
from os import path
import sqlite3

ROOT = path.dirname(path.realpath(__file__))

app =Flask(__name__)


@app.route('/')
def start_page():
    return render_template("index.html")

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/services')
def services_page():
    return render_template("services.html")

@app.route('/contact')
def contact_page():
    return render_template("contact.html")

@app.route('/plans')
def plans_page():
    return render_template("pricing.html")

@app.route('/register')
def register_page():
    return render_template("register.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/addcard')
def add_card():
    return render_template("addcard.html",data = session["fname"])

@app.route('/paybill')
def pay_bill():
    return render_template("pay.html",data = session["fname"])

@app.route('/payment')
def make_payment():
    return render_template("payment.html",data = session["plan"])

@app.route('/maintain')
def under_maintenance():
    return render_template("maintain.html")

@app.route('/carddetails')
def card_details():
    return render_template("carddetails.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dash.html", data=[session["fname"], session["validity"]])






@app.route('/result',methods=['POST'])
def register_user():
    fname, lname, email, mobile, password, address, area, city, pin, purpose, dataplan, visit = request.form["form-first-name"],request.form["form-last-name"],request.form["form-email"],request.form["form-mobile"],request.form["form-password"],request.form["form-address"],request.form["form-area"],request.form["form-city"],request.form["form-pin"],request.form["form-purpose"],request.form["form-plan"],request.form["form-date"]
    con = sqlite3.connect(path.join(ROOT, "user_credentials.db"))
    con.execute("INSERT INTO credentials (fname,lname,email,mobile,password,address,area,city,pin,purpose,dataplan,visit) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(fname, lname, email, mobile, password, address, area, city, pin, purpose, dataplan, visit)) #"+fname+","+lname+","+email+","+mobile+","+password+","+address+","+area+","+city+","+pin+","+purpose+","+dataplan+","+visit+")")
    con.commit()
    con.close()
    return render_template("index.html")

@app.route('/validate',methods=['POST'])
def login_validate():
    mobile = request.form["log-mobile"]
    given_pass = request.form["log-password"]
    con = sqlite3.connect(path.join(ROOT, "user_credentials.db"))
    cur = con.cursor()
    cur.execute("SELECT password,fname,validity,dataplan from credentials where mobile = ?",(mobile,))
    rows = cur.fetchall()
    fname = list(rows)[0][1]
    validity = list(rows)[0][2]
    plan = list(rows)[0][3]
    con.close()

    if len(list(rows)) == 0:
        error = "Invalid Mobile or Password. Try again"
        return render_template("login.html", error=error)

    if list(rows)[0][0] == given_pass:
        session["fname"] = fname
        session["mobile"] = mobile
        session["validity"] = validity
        session["plan"] = plan
        return render_template("dash.html",data = [session["fname"],session["validity"]])
    else:
        error = "Invalid Mobile or Password. Try again"
        return render_template("login.html",error = error)

@app.route('/cardadded',methods=['POST'])
def enter_card():
    card_no = request.form["card-no"]
    card_name = request.form["card-name"]
    card_date = request.form["card-date"]
    card_cvv = request.form["card-cvv"]
    con = sqlite3.connect(path.join(ROOT, "user_credentials.db"))
    cur = con.cursor()
    cur.execute("INSERT INTO card_details (card_no,card_name,expire,cvc) VALUES (?,?,?,?)",(card_no,card_name,card_date,card_cvv))
    con.commit()
    con.close()
    return render_template("dash.html",data = [session["fname"],session["validity"]])

@app.route('/payverify',methods=['POST'])
def pay_verified():
    card_no = request.form["card-no"]
    card_name = request.form["card-name"]
    card_date  = request.form["card-date"]
    card_cvv = request.form["card-cvv"]

    #print("Form Data:",card_no,card_name,card_date,card_cvv)

    fname = session["fname"]
    mobile = session["mobile"]


    #print("Session Data",fname,mobile)

    con = sqlite3.connect(path.join(ROOT, "user_credentials.db"))
    cur = con.cursor()
    cur.execute("SELECT dataplan,validity from credentials where mobile = ?", (mobile,))
    rows = cur.fetchall()
    plan = list(rows)[0][0]
    validity = list(rows)[0][1]


    #print("Plan",plan)

    cur1 = con.cursor()
    cur1.execute("SELECT card_name,expire,cvc,balance from card_details where card_no = ?", (card_no,))
    rows = cur1.fetchall()
    #print(list(rows))

    if len(list(rows)) == 0:
        flash("Unsuccessful: Invalid Credentials")
        return render_template("dash.html",data = [session["fname"],session["validity"]])

    e_name = list(rows)[0][0]
    e_expire = list(rows)[0][1]
    e_cvc = list(rows)[0][2]
    e_balance = list(rows)[0][3]

    #print("DB Data",e_name,e_expire,e_cvc,e_balance)

    if int(e_balance) < int(plan):
        flash("Transaction Failed: Insufficient Balance")
        return render_template("dash.html",data = [session["fname"],session["validity"]])

    if card_name == e_name and card_date == e_expire and card_cvv == e_cvc:
        deduct = int(e_balance) - int(plan)
        #print(deduct)
        cur2 = con.cursor()
        cur2.execute("UPDATE card_details SET balance = ? where card_no = ?",(deduct,card_no))
        cur3 = con.cursor()
        cur3.execute("UPDATE credentials SET validity = ? where mobile = ?", (int(validity) + 30, mobile))
        con.commit()
        con.close()
        session["validity"] = int(validity) + 30
        flash("Transaction Successful")

    else:
        flash("Transaction Failed: Invalid Credentials")

    return render_template("dash.html",data=[session["fname"],session["validity"]])
    con.close()






if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
