
from flask import Flask, render_template,request,redirect
import fn
import test

# 1.user input city and number of resturant wanna check--TABLE
# 2. sort by rating and price- choose resturants--TABLE
# 3.INPUT YOUR ORIGIN--TABLE:ESTIMATION
#4.MAP

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/hello')


@app.route('/hello/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        input_city = request.form['cityname']
        # number = request.form['number']
        # go check DB
        # try:
        yelp_db=fn.Yelpeat(input_city).get_data()
        # yelp_db=test.get_data(input_city)
        return render_template("yelptable.html", city=input_city,list_of_res=yelp_db)
        # except:
        #     return render_template("hello.html", cityname=input_city)#,error_message='')
    else:
            input_city = ''
            return render_template("hello.html", cityname=input_city)
    # return redirect("/yelptable.html")

@app.route('/yelptable',methods=['GET', 'POST'])
def yelptable():
      city=hello().request.form['cityname']
      return yelptable
      # list_of_res=fn.Yelpeat(city).get_data()
#     # name = request.form["name"]
#     # message = request.form["message"]
#     # model.add_entry(name, message)return render_template("hello.html", city=city)

if __name__ == '__main__':
    # model.init_bball()
    app.run(debug=True)
