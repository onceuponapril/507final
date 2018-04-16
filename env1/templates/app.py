from flask import Flask, render_template,request
import fn

# 1.user input city and number of resturant wanna check--TABLE
# 2. sort by rating and price- choose resturants--TABLE
# 3.INPUT YOUR ORIGIN--TABLE:ESTIMATION
#4.MAP

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        user_input_city = request.form['cityname']
        number = request.form['number']

    # else:
    #     cityname = ''
    #     lastname = ''

    # return render_template("hello.html", cityname=user_input_city, number=number)
    return redirect("/yelptable.html")

@app.route("/postentry", methods=["POST"])
def postentry():
    name = request.form["name"]
    message = request.form["message"]
    model.add_entry(name, message)
    return redirect("/")

if __name__ == '__main__':
    # model.init_bball()
    app.run(debug=True)
