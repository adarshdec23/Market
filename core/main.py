from core.risk import userClassifier, portfolio
from core.preference import main as preference
from config import main
import pickle

class Main:

    risk_association=dict(
        aggressive='high',
        moderate='moderate',
        conservative='low'
    )

    def __init__(self):
        self.uc = userClassifier.Matcher()
        self.prefer = preference.UserPreference()
        file = open(main.path+'upinkai/company.pkl', 'rb')
        self.company_risks = pickle.load(file)
        self.portfolio = portfolio.Portfolio()

    def get_companies(self, risk_level, preferred_cat):
        companies = []
        for company in self.company_risks:
            if company[3] in preferred_cat and company[6]['risk'] == risk_level:
                # company[2] is category, 6 is dict of risk, sharpe, mean and std
                companies.append(company[2])
        return companies


    def get_suggestions(self, user):
        user_class = self.uc.get_user_class(user)
        print(user_class)
        user_preference = self.prefer.get_preferences(user)
        user_companies = self.get_companies(Main.risk_association[user_class], user_preference)
        return user_companies
