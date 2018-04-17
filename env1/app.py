
from flask import Flask, render_template,request,redirect
import fn
import test

# 1.user input city and number of resturant wanna check--TABLE
# 2. sort by rating and price- choose resturants--TABLE
# 3.INPUT YOUR ORIGIN--TABLE:ESTIMATION
#4.MAP

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect('/hello')
    else:
        return render_template("index.html")


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        pass
        # except:
        #     return render_template("hello.html", cityname=input_city)#,error_message='')
    else:
        input_city = ''
        return render_template("hello.html")


@app.route('/yelptable',methods=['GET', 'POST'])
def yelptable():
    if request.method == 'POST':
        # sortby = request.form['sortby']
        # cityname=hello().city
        input_city = request.form['cityname']
        # number = request.form['number']
        # go check DB
        # try:
        yelp_db=fn.Yelpeat(input_city).get_data()
        # yelp_db=test.get_data(input_city)
        return render_template("yelptable.html",city=input_city,list_of_res=yelp_db)
        # city=hello().request.form['cityname']
        # Yelpeat().sorteat(sortby)
    else:
        return render_template("yelptable.html")


      # list_of_res=fn.Yelpeat(city).get_data()
#     # name = request.form["name"]
#     # message = request.form["message"]
#     # model.add_entry(name, message)return render_template("hello.html", city=city)

@app.route('/lyftlist',methods=['GET', 'POST'])
def lyft():
    if request.method == "POST":
        eatid_list=request.form.getlist('store')
        origin=request.form['user_location']
        lyft = fn.lyft_data()
        lyft.create_table(origin)
    return

# @app.route('/lyft/',methods=['GET', 'POST'])
# def lyft():
#     return


if __name__ == '__main__':
    # model.init_bball()
    app.run(debug=True)
