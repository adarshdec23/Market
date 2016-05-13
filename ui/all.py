from flask import Flask, render_template
from core.risk import userClassifier, portfolio, company
from core.prediction import rsi
from core import main

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/user')
def all_users():
    uc = userClassifier.Matcher()
    return render_template('all_users.html', user_list=uc.get_all_user_classes())

@app.route('/user/<username>/<risk_class>')
def show_user_profile(username, risk_class):
    m = main.Main()
    results = m.get_suggestions(username)
    return render_template(
        'user.html',
        username=username.capitalize(),
        risk_class=risk_class.capitalize(),
        suggestions=results['suggestions'],
        preference=results['preference'],
        ratios=results['ratios']
    )

@app.route('/company')
def all_companies():
    c = company.SharpeCompany()
    print(c.get_all_company_ratios())
    return render_template('all_companies.html', company_list=c.get_all_company_ratios())

@app.route('/company/<symbol>')
def show_company(symbol):
    c = company.SharpeCompany()
    c.set_company(symbol)
    r = rsi.RSI()
    return render_template(
        'company.html',
        symbol=symbol,
        ratios=c.get_ratio(),
        next_open=c.get_latest_open(),
        med_prediction=r.get_med_analysis_of(symbol)
       )

if __name__ == '__main__':
    app.run(debug=True)