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
        self.risk_class = None
        self.user_preference = None

    def get_companies(self, risk_level, preferred_cat):
        companies = []
        for company in self.company_risks:
            if company[3] in preferred_cat and company[6]['risk'] == risk_level:
                # company[3] is category, 6 is dict of risk, sharpe, mean and std
                companies.append(company[2])
        return companies

    def get_best_company_category(self, category):
        highest_ratio = 0
        for company in self.company_risks:
            if company[3] == category and company[6]['sharpe'] > highest_ratio:
                best_company = dict(
                    symbol = company[2],
                    name = company[1],
                    sharpe = company[6]['sharpe'],
                    mean = company[6]['mean']
                )
        return best_company

    def get_suggestions(self, user):
        self.risk_class = self.uc.get_user_class(user)
        self.user_preference = self.prefer.get_preferences(user)
        suggested_companies = self.get_companies(Main.risk_association[self.risk_class], self.user_preference)
        self.portfolio.set_user(user+'.csv')
        current_companies = self.portfolio.get_companies()
        suggestions_wo_current = []
        for company in suggested_companies:
            if company not in current_companies:
                suggestions_wo_current.append(company)
        print(suggestions_wo_current)
        return dict(
            suggestions=suggested_companies,
            preference=self.user_preference,
            ratios=self.portfolio.get_ratio()
        )
