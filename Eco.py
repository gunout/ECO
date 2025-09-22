import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AfriqueCommuneFinanceAnalyzer:
    def __init__(self, commune_name, pays):
        self.commune = commune_name
        self.pays = pays
        self.colors = ['#008000', '#FFD700', '#DC143C', '#0000FF', '#FF4500', 
                      '#4B0082', '#00CED1', '#FF69B4', '#32CD32', '#8B4513']
        
        self.start_year = 2002
        self.end_year = 2025
        
        # Configuration des devises par pays
        self.devise_config = self._get_devise_config()
        self.devise = self.devise_config["devise"]
        self.symbole = self.devise_config["symbole"]
        self.taux_change = self.devise_config["taux_change"]  # 1€ = X devise locale
        
        # Configuration spécifique à chaque commune africaine
        self.config = self._get_commune_config()
        
    def _get_devise_config(self):
        """Retourne la configuration des devises par pays"""
        devises = {
            "Sénégal": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "Côte d'Ivoire": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "Cameroun": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "Gabon": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "Maroc": {"devise": "Dirham", "symbole": "MAD", "taux_change": 11},
            "Tunisie": {"devise": "Dinar", "symbole": "TND", "taux_change": 3.3},
            "Algérie": {"devise": "Dinar", "symbole": "DZD", "taux_change": 145},
            "Nigeria": {"devise": "Naira", "symbole": "NGN", "taux_change": 1600},
            "Ghana": {"devise": "Cedi", "symbole": "GHS", "taux_change": 15},
            "Kenya": {"devise": "Shilling", "symbole": "KES", "taux_change": 160},
            "Afrique du Sud": {"devise": "Rand", "symbole": "ZAR", "taux_change": 20},
            "RDC": {"devise": "Franc Congolais", "symbole": "CDF", "taux_change": 2700},
            "Mali": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "Burkina Faso": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "Bénin": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "Togo": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655},
            "default": {"devise": "Franc CFA", "symbole": "FCFA", "taux_change": 655}
        }
        
        return devises.get(self.pays, devises["default"])
    
    def _get_commune_config(self):
        """Retourne la configuration spécifique pour chaque commune africaine"""
        configs = {
            # Villes capitales
            "Dakar": {
                "population_base": 1200000,
                "budget_base": 85000,  # en millions de FCFA
                "type": "capitale",
                "specialites": ["administration", "port", "commerce", "education", "sante"]
            },
            "Abidjan": {
                "population_base": 4800000,
                "budget_base": 120000,
                "type": "economique",
                "specialites": ["port", "commerce", "industrie", "finance", "transport"]
            },
            "Yaoundé": {
                "population_base": 2800000,
                "budget_base": 75000,
                "type": "politique",
                "specialites": ["administration", "education", "culture", "agriculture"]
            },
            "Lagos": {
                "population_base": 15000000,
                "budget_base": 450000,  # en millions de Naira
                "type": "megapole",
                "specialites": ["commerce", "port", "industrie", "technologie", "finance"]
            },
            "Accra": {
                "population_base": 2500000,
                "budget_base": 95000,  # en millions de Cedis
                "type": "capitale",
                "specialites": ["administration", "commerce", "port", "education", "tourisme"]
            },
            "Nairobi": {
                "population_base": 4500000,
                "budget_base": 180000,  # en millions de Shillings
                "type": "regionale",
                "specialites": ["technologie", "commerce", "diplomatie", "transport", "tourisme"]
            },
            "Kinshasa": {
                "population_base": 17000000,
                "budget_base": 950000,  # en millions de Francs Congolais
                "type": "megapole",
                "specialites": ["administration", "commerce", "port_fluvial", "mines", "agriculture"]
            },
            "Johannesburg": {
                "population_base": 6000000,
                "budget_base": 280000,  # en millions de Rands
                "type": "economique",
                "specialites": ["mines", "finance", "commerce", "industrie", "tourisme"]
            },
            "Casablanca": {
                "population_base": 3700000,
                "budget_base": 180000,  # en millions de Dirhams
                "type": "economique",
                "specialites": ["port", "industrie", "commerce", "finance", "tourisme"]
            },
            "Alger": {
                "population_base": 3500000,
                "budget_base": 220000,  # en millions de Dinars
                "type": "capitale",
                "specialites": ["administration", "port", "industrie", "commerce", "culture"]
            },
            
            # Villes secondaires
            "Saint-Louis": {
                "population_base": 180000,
                "budget_base": 12000,
                "type": "historique",
                "specialites": ["tourisme", "culture", "peche", "education"]
            },
            "Bouaké": {
                "population_base": 740000,
                "budget_base": 28000,
                "type": "interieure",
                "specialites": ["agriculture", "commerce", "transport", "education"]
            },
            "Douala": {
                "population_base": 3000000,
                "budget_base": 95000,
                "type": "economique",
                "specialites": ["port", "industrie", "commerce", "transport", "logistique"]
            },
            "Kumasi": {
                "population_base": 2100000,
                "budget_base": 45000,
                "type": "culturelle",
                "specialites": ["culture", "commerce", "agriculture", "artisanat"]
            },
            "Mombasa": {
                "population_base": 1200000,
                "budget_base": 55000,
                "type": "portuaire",
                "specialites": ["port", "tourisme", "commerce", "transport_maritime"]
            },
            "Lubumbashi": {
                "population_base": 2000000,
                "budget_base": 85000,
                "type": "miniere",
                "specialites": ["mines", "commerce", "industrie", "transport"]
            },
            "Cape Town": {
                "population_base": 4400000,
                "budget_base": 195000,
                "type": "touristique",
                "specialites": ["tourisme", "port", "vin", "technologie", "culture"]
            },
            "Marrakech": {
                "population_base": 930000,
                "budget_base": 65000,
                "type": "touristique",
                "specialites": ["tourisme", "culture", "artisanat", "commerce"]
            },
            "Tunis": {
                "population_base": 640000,
                "budget_base": 48000,
                "type": "capitale",
                "specialites": ["administration", "tourisme", "culture", "education", "sante"]
            },
            
            # Communes rurales
            "Tamba": {
                "population_base": 85000,
                "budget_base": 3500,
                "type": "rurale",
                "specialites": ["agriculture", "elevage", "artisanat", "commerce_local"]
            },
            "Korhogo": {
                "population_base": 290000,
                "budget_base": 9500,
                "type": "rurale",
                "specialites": ["agriculture", "culture", "artisanat", "commerce_regional"]
            },
            "Garoua": {
                "population_base": 600000,
                "budget_base": 18000,
                "type": "rurale",
                "specialites": ["agriculture", "elevage", "commerce", "transport_fluvial"]
            },
            "Tamale": {
                "population_base": 370000,
                "budget_base": 12500,
                "type": "rurale",
                "specialites": ["agriculture", "commerce", "education", "sante_regionale"]
            },
            
            # Configuration par défaut
            "default": {
                "population_base": 50000,
                "budget_base": 2500,
                "type": "locale",
                "specialites": ["agriculture", "commerce_local", "services", "artisanat"]
            }
        }
        
        return configs.get(self.commune, configs["default"])
    
    def _convert_to_local_currency(self, amount_eur):
        """Convertit un montant d'euros en devise locale"""
        return amount_eur * self.taux_change
    
    def generate_financial_data(self):
        """Génère des données financières pour la commune africaine"""
        print(f"🏛️ Génération des données financières pour {self.commune}, {self.pays}...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Annee': [date.year for date in dates]}
        
        # Données démographiques (croissance africaine très forte)
        data['Population'] = self._simulate_population(dates)
        data['Menages'] = self._simulate_households(dates)
        
        # Recettes communales en devise locale
        data['Recettes_Totales'] = self._simulate_total_revenue(dates)
        data['Impots_Locaux'] = self._simulate_tax_revenue(dates)
        data['Subventions_Etat'] = self._simulate_state_grants(dates)
        data['Aide_Internationale'] = self._simulate_international_aid(dates)
        data['Autres_Recettes'] = self._simulate_other_revenue(dates)
        
        # Dépenses communales en devise locale
        data['Depenses_Totales'] = self._simulate_total_expenses(dates)
        data['Fonctionnement'] = self._simulate_operating_expenses(dates)
        data['Investissement'] = self._simulate_investment_expenses(dates)
        data['Charge_Dette'] = self._simulate_debt_charges(dates)
        data['Personnel'] = self._simulate_staff_costs(dates)
        
        # Indicateurs financiers
        data['Epargne_Brute'] = self._simulate_gross_savings(dates)
        data['Dette_Totale'] = self._simulate_total_debt(dates)
        data['Taux_Endettement'] = self._simulate_debt_ratio(dates)
        data['Taux_Fiscalite'] = self._simulate_tax_rate(dates)
        
        # Investissements spécifiques adaptés à l'Afrique
        data['Investissement_Agriculture'] = self._simulate_agriculture_investment(dates)
        data['Investissement_Infrastructures'] = self._simulate_infrastructure_investment(dates)
        data['Investissement_Sante'] = self._simulate_health_investment(dates)
        data['Investissement_Education'] = self._simulate_education_investment(dates)
        data['Investissement_Eau'] = self._simulate_water_investment(dates)
        data['Investissement_Energie'] = self._simulate_energy_investment(dates)
        data['Investissement_Mines'] = self._simulate_mining_investment(dates)
        data['Investissement_Tourisme'] = self._simulate_tourism_investment(dates)
        
        df = pd.DataFrame(data)
        
        # Ajouter des tendances spécifiques au contexte africain
        self._add_african_trends(df)
        
        return df
    
    def _simulate_population(self, dates):
        """Simule la population de la commune (croissance africaine très forte)"""
        base_population = self.config["population_base"]
        
        population = []
        for i, date in enumerate(dates):
            # Croissance démographique africaine (très forte)
            if self.config["type"] == "megapole":
                growth_rate = 0.045  # Croissance très forte dans les mégapoles
            elif self.config["type"] == "capitale":
                growth_rate = 0.042  # Croissance forte dans les capitales
            elif self.config["type"] == "rurale":
                growth_rate = 0.035  # Croissance rurale plus modérée
            else:
                growth_rate = 0.040  # Croissance moyenne
                
            growth = 1 + growth_rate * i
            population.append(base_population * growth)
        
        return population
    
    def _simulate_households(self, dates):
        """Simule le nombre de ménages (taille moyenne plus grande en Afrique)"""
        base_households = self.config["population_base"] / 5.5  # Taille des ménages plus grande
        
        households = []
        for i, date in enumerate(dates):
            growth = 1 + 0.035 * i  # Croissance forte
            households.append(base_households * growth)
        
        return households
    
    def _simulate_total_revenue(self, dates):
        """Simule les recettes totales de la commune en devise locale"""
        base_revenue = self._convert_to_local_currency(self.config["budget_base"])
        
        revenue = []
        for i, date in enumerate(dates):
            # Croissance économique africaine (variable selon le type)
            if self.config["type"] == "economique":
                growth_rate = 0.065  # Croissance très forte dans les pôles économiques
            elif self.config["type"] == "miniere":
                growth_rate = 0.072  # Croissance explosive dans les zones minières
            elif self.config["type"] == "rurale":
                growth_rate = 0.048  # Croissance rurale plus modérée
            else:
                growth_rate = 0.058  # Croissance moyenne
                
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.12)  # Plus de volatilité
            revenue.append(base_revenue * growth * noise)
        
        return revenue
    
    def _simulate_tax_revenue(self, dates):
        """Simule les recettes fiscales en devise locale"""
        base_tax = self._convert_to_local_currency(self.config["budget_base"] * 0.25)  # Part faible des impôts
        
        tax_revenue = []
        for i, date in enumerate(dates):
            growth = 1 + 0.045 * i  # Croissance moyenne
            noise = np.random.normal(1, 0.15)  # Forte volatilité
            tax_revenue.append(base_tax * growth * noise)
        
        return tax_revenue
    
    def _simulate_state_grants(self, dates):
        """Simule les subventions de l'État (très importantes en Afrique)"""
        base_grants = self._convert_to_local_currency(self.config["budget_base"] * 0.45)  # Part importante
        
        grants = []
        for i, date in enumerate(dates):
            year = date.year
            # Augmentation variable selon les politiques
            if year >= 2010:
                increase = 1 + 0.015 * (year - 2010)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.10)
            grants.append(base_grants * increase * noise)
        
        return grants
    
    def _simulate_international_aid(self, dates):
        """Simule l'aide internationale (spécifique à l'Afrique)"""
        base_aid = self._convert_to_local_currency(self.config["budget_base"] * 0.15)  # Part importante
        
        aid = []
        for i, date in enumerate(dates):
            year = date.year
            # Variations selon les programmes internationaux
            if year in [2005, 2010, 2015, 2020]:
                multiplier = 1.8  # Années de programmes d'aide
            elif year in [2008, 2014, 2022]:
                multiplier = 0.7  # Réduction pendant les crises
            else:
                multiplier = 1.0
            
            growth = 1 + 0.025 * i
            noise = np.random.normal(1, 0.25)  # Très forte volatilité
            aid.append(base_aid * growth * multiplier * noise)
        
        return aid
    
    def _simulate_other_revenue(self, dates):
        """Simule les autres recettes en devise locale"""
        base_other = self._convert_to_local_currency(self.config["budget_base"] * 0.15)
        
        other_revenue = []
        for i, date in enumerate(dates):
            growth = 1 + 0.038 * i
            noise = np.random.normal(1, 0.18)
            other_revenue.append(base_other * growth * noise)
        
        return other_revenue
    
    def _simulate_total_expenses(self, dates):
        """Simule les dépenses totales en devise locale"""
        base_expenses = self._convert_to_local_currency(self.config["budget_base"] * 0.95)  # Dépenses proches des recettes
        
        expenses = []
        for i, date in enumerate(dates):
            growth = 1 + 0.052 * i  # Croissance forte
            noise = np.random.normal(1, 0.09)
            expenses.append(base_expenses * growth * noise)
        
        return expenses
    
    def _simulate_operating_expenses(self, dates):
        """Simule les dépenses de fonctionnement en devise locale"""
        base_operating = self._convert_to_local_currency(self.config["budget_base"] * 0.70)  # Part très importante
        
        operating = []
        for i, date in enumerate(dates):
            growth = 1 + 0.048 * i
            noise = np.random.normal(1, 0.08)
            operating.append(base_operating * growth * noise)
        
        return operating
    
    def _simulate_investment_expenses(self, dates):
        """Simule les dépenses d'investissement en devise locale"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.25)  # Part plus faible
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            # Plans d'investissement liés aux programmes de développement
            if year in [2005, 2010, 2015, 2020]:
                multiplier = 2.0  # Années d'investissement massif
            elif year in [2008, 2014, 2021]:
                multiplier = 0.6  # Réduction pendant les crises
            else:
                multiplier = 1.0
            
            growth = 1 + 0.040 * i
            noise = np.random.normal(1, 0.22)  # Très forte volatilité
            investment.append(base_investment * growth * multiplier * noise)
        
        return investment
    
    def _simulate_debt_charges(self, dates):
        """Simule les charges de la dette en devise locale"""
        base_debt_charge = self._convert_to_local_currency(self.config["budget_base"] * 0.08)  # Charges importantes
        
        debt_charges = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2005:
                increase = 1 + 0.012 * (year - 2005)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.15)
            debt_charges.append(base_debt_charge * increase * noise)
        
        return debt_charges
    
    def _simulate_staff_costs(self, dates):
        """Simule les dépenses de personnel en devise locale"""
        base_staff = self._convert_to_local_currency(self.config["budget_base"] * 0.50)  # Part très importante
        
        staff_costs = []
        for i, date in enumerate(dates):
            growth = 1 + 0.045 * i
            noise = np.random.normal(1, 0.07)
            staff_costs.append(base_staff * growth * noise)
        
        return staff_costs
    
    def _simulate_gross_savings(self, dates):
        """Simule l'épargne brute en devise locale"""
        savings = []
        for i, date in enumerate(dates):
            base_saving = self._convert_to_local_currency(self.config["budget_base"] * 0.02)  # Épargne faible
            
            year = date.year
            if year >= 2010:
                improvement = 1 + 0.006 * (year - 2010)  # Amélioration lente
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.20)  # Très forte volatilité
            savings.append(base_saving * improvement * noise)
        
        return savings
    
    def _simulate_total_debt(self, dates):
        """Simule la dette totale en devise locale"""
        base_debt = self._convert_to_local_currency(self.config["budget_base"] * 0.90)  # Dette importante
        
        debt = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2005, 2010, 2015, 2020]:
                change = 1.35  # Augmentation forte pendant les investissements
            elif year in [2008, 2014, 2021]:
                change = 0.85  # Réduction pendant les crises
            else:
                change = 1.0
            
            noise = np.random.normal(1, 0.12)
            debt.append(base_debt * change * noise)
        
        return debt
    
    def _simulate_debt_ratio(self, dates):
        """Simule le taux d'endettement"""
        ratios = []
        for i, date in enumerate(dates):
            base_ratio = 0.82  # Endettement initial élevé
            
            year = date.year
            if year >= 2010:
                improvement = 1 - 0.008 * (year - 2010)  # Amélioration lente
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.09)
            ratios.append(base_ratio * improvement * noise)
        
        return ratios
    
    def _simulate_tax_rate(self, dates):
        """Simule le taux de fiscalité (moyen)"""
        rates = []
        for i, date in enumerate(dates):
            base_rate = 0.65  # Fiscalité initiale faible
            
            year = date.year
            if year >= 2010:
                increase = 1 + 0.004 * (year - 2010)  # Augmentation très lente
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.05)
            rates.append(base_rate * increase * noise)
        
        return rates
    
    def _simulate_agriculture_investment(self, dates):
        """Simule l'investissement agricole (très important en Afrique)"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.12)  # Part importante
        
        # Ajustement selon les spécialités
        multiplier = 1.8 if "agriculture" in self.config["specialites"] else 0.9
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2005, 2010, 2015, 2020]:
                year_multiplier = 2.5  # Plans agricoles importants
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.040 * i
            noise = np.random.normal(1, 0.20)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_infrastructure_investment(self, dates):
        """Simule l'investissement en infrastructures (priorité en Afrique)"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.15)  # Part très importante
        
        multiplier = 1.6 if "infrastructures" in self.config["specialites"] else 1.2
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2006, 2012, 2018, 2023]:
                year_multiplier = 2.2
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.045 * i
            noise = np.random.normal(1, 0.18)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_health_investment(self, dates):
        """Simule l'investissement en santé"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.08)
        
        multiplier = 1.7 if "sante" in self.config["specialites"] else 1.0
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2008, 2014, 2020]:
                year_multiplier = 2.0
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.038 * i
            noise = np.random.normal(1, 0.22)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_education_investment(self, dates):
        """Simule l'investissement éducatif"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.10)  # Part importante
        
        multiplier = 1.6 if "education" in self.config["specialites"] else 1.1
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019]:
                year_multiplier = 1.9
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.042 * i
            noise = np.random.normal(1, 0.19)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_water_investment(self, dates):
        """Simule l'investissement en eau (priorité en Afrique)"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.06)
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2009, 2015, 2021]:
                year_multiplier = 2.3  # Programmes eau très importants
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.035 * i
            noise = np.random.normal(1, 0.21)
            investment.append(base_investment * growth * year_multiplier * noise)
        
        return investment
    
    def _simulate_energy_investment(self, dates):
        """Simule l'investissement en énergie"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.07)
        
        multiplier = 1.5 if "energie" in self.config["specialites"] else 1.0
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2010, 2016, 2022]:
                year_multiplier = 2.1
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.040 * i
            noise = np.random.normal(1, 0.20)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_mining_investment(self, dates):
        """Simule l'investissement minier (spécifique à l'Afrique)"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.05)
        
        multiplier = 2.5 if "mines" in self.config["specialites"] else 0.3
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2008, 2014, 2020]:
                year_multiplier = 3.0  # Investissements miniers massifs
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.050 * i
            noise = np.random.normal(1, 0.35)  # Extrême volatilité
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_tourism_investment(self, dates):
        """Simule l'investissement touristique"""
        base_investment = self._convert_to_local_currency(self.config["budget_base"] * 0.04)
        
        multiplier = 2.0 if "tourisme" in self.config["specialites"] else 0.7
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019, 2024]:
                year_multiplier = 2.0
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.036 * i
            noise = np.random.normal(1, 0.24)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _add_african_trends(self, df):
        """Ajoute des tendances réalistes adaptées au contexte africain"""
        for i, row in df.iterrows():
            year = row['Annee']
            
            # Période de croissance économique (2002-2008)
            if 2002 <= year <= 2008:
                df.loc[i, 'Investissement_Infrastructures'] *= 1.4
                df.loc[i, 'Aide_Internationale'] *= 1.3
            
            # Impact de la crise financière mondiale (2008-2009)
            if 2008 <= year <= 2009:
                df.loc[i, 'Recettes_Totales'] *= 0.88
                df.loc[i, 'Investissement'] *= 0.65
                df.loc[i, 'Aide_Internationale'] *= 1.25  # Augmentation de l'aide
            
            # Croissance forte post-crise (2010-2014)
            elif 2010 <= year <= 2014:
                df.loc[i, 'Investissement_Agriculture'] *= 1.3
                df.loc[i, 'Investissement_Infrastructures'] *= 1.5
            
            # Baisse des cours des matières premières (2014-2016)
            if 2014 <= year <= 2016:
                df.loc[i, 'Investissement_Mines'] *= 0.6
                df.loc[i, 'Recettes_Totales'] *= 0.92
            
            # Programme de développement continental (2017-2019)
            if 2017 <= year <= 2019:
                df.loc[i, 'Aide_Internationale'] *= 1.4
                df.loc[i, 'Investissement_Eau'] *= 1.8
                df.loc[i, 'Investissement_Energie'] *= 1.6
            
            # Impact de la crise COVID-19 (2020-2021)
            if 2020 <= year <= 2021:
                if year == 2020:
                    df.loc[i, 'Recettes_Totales'] *= 0.78
                    df.loc[i, 'Investissement_Tourisme'] *= 0.4
                    df.loc[i, 'Aide_Internationale'] *= 1.35
                else:
                    df.loc[i, 'Subventions_Etat'] *= 1.20
            
            # Plan de relance post-COVID et Agenda 2063 (2022-2025)
            if year >= 2022:
                df.loc[i, 'Investissement_Infrastructures'] *= 1.25
                df.loc[i, 'Investissement_Agriculture'] *= 1.30
                df.loc[i, 'Investissement_Sante'] *= 1.40
    
    def create_financial_analysis(self, df):
        """Crée une analyse complète des finances communales africaines"""
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Évolution des recettes et dépenses
        ax1 = plt.subplot(4, 2, 1)
        self._plot_revenue_expenses(df, ax1)
        
        # 2. Structure des recettes
        ax2 = plt.subplot(4, 2, 2)
        self._plot_revenue_structure(df, ax2)
        
        # 3. Structure des dépenses
        ax3 = plt.subplot(4, 2, 3)
        self._plot_expenses_structure(df, ax3)
        
        # 4. Investissements communaux
        ax4 = plt.subplot(4, 2, 4)
        self._plot_investments(df, ax4)
        
        # 5. Dette et endettement
        ax5 = plt.subplot(4, 2, 5)
        self._plot_debt(df, ax5)
        
        # 6. Indicateurs de performance
        ax6 = plt.subplot(4, 2, 6)
        self._plot_performance_indicators(df, ax6)
        
        # 7. Démographie
        ax7 = plt.subplot(4, 2, 7)
        self._plot_demography(df, ax7)
        
        # 8. Investissements sectoriels
        ax8 = plt.subplot(4, 2, 8)
        self._plot_sectorial_investments(df, ax8)
        
        plt.suptitle(f'Analyse des Comptes Communaux de {self.commune}, {self.pays} ({self.start_year}-{self.end_year})\n(En millions de {self.symbole})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.commune}_{self.pays}_financial_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Générer les insights
        self._generate_financial_insights(df)
    
    def _plot_revenue_expenses(self, df, ax):
        """Plot de l'évolution des recettes et dépenses"""
        ax.plot(df['Annee'], df['Recettes_Totales'], label='Recettes Totales', 
               linewidth=2, color='#008000', alpha=0.8)
        ax.plot(df['Annee'], df['Depenses_Totales'], label='Dépenses Totales', 
               linewidth=2, color='#DC143C', alpha=0.8)
        
        ax.set_title(f'Évolution des Recettes et Dépenses (millions de {self.symbole})', 
                    fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Montants (millions {self.symbole})')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_revenue_structure(self, df, ax):
        """Plot de la structure des recettes"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Impots_Locaux', 'Subventions_Etat', 'Aide_Internationale', 'Autres_Recettes']
        colors = ['#008000', '#FFD700', '#DC143C', '#0000FF']
        labels = ['Impôts Locaux', 'Subventions État', 'Aide Internationale', 'Autres Recettes']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title(f'Structure des Recettes (millions de {self.symbole})', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Montants (millions {self.symbole})')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_expenses_structure(self, df, ax):
        """Plot de la structure des dépenses"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Fonctionnement', 'Investissement', 'Charge_Dette', 'Personnel']
        colors = ['#008000', '#FFD700', '#DC143C', '#0000FF']
        labels = ['Fonctionnement', 'Investissement', 'Charge Dette', 'Personnel']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title(f'Structure des Dépenses (millions de {self.symbole})', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Montants (millions {self.symbole})')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_investments(self, df, ax):
        """Plot des investissements communaux"""
        ax.plot(df['Annee'], df['Investissement_Agriculture'], label='Agriculture', 
               linewidth=2, color='#008000', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Infrastructures'], label='Infrastructures', 
               linewidth=2, color='#FFD700', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Sante'], label='Santé', 
               linewidth=2, color='#DC143C', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Education'], label='Éducation', 
               linewidth=2, color='#0000FF', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Eau'], label='Eau', 
               linewidth=2, color='#00CED1', alpha=0.8)
        if 'Investissement_Mines' in df.columns:
            ax.plot(df['Annee'], df['Investissement_Mines'], label='Mines', 
                   linewidth=2, color='#8B4513', alpha=0.8)
        
        ax.set_title(f'Répartition des Investissements (millions de {self.symbole})', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Montants (millions {self.symbole})')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_debt(self, df, ax):
        """Plot de la dette et du taux d'endettement"""
        # Dette totale
        ax.bar(df['Annee'], df['Dette_Totale'], label=f'Dette Totale (millions {self.symbole})', 
              color='#008000', alpha=0.7)
        
        ax.set_title('Dette Communale et Taux d\'Endettement', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Dette (millions {self.symbole})', color='#008000')
        ax.tick_params(axis='y', labelcolor='#008000')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Taux d'endettement en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Taux_Endettement'], label='Taux d\'Endettement', 
                linewidth=3, color='#DC143C')
        ax2.set_ylabel('Taux d\'Endettement', color='#DC143C')
        ax2.tick_params(axis='y', labelcolor='#DC143C')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_performance_indicators(self, df, ax):
        """Plot des indicateurs de performance"""
        # Épargne brute
        ax.bar(df['Annee'], df['Epargne_Brute'], label=f'Épargne Brute (millions {self.symbole})', 
              color='#32CD32', alpha=0.7)
        
        ax.set_title('Indicateurs de Performance', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Épargne Brute (millions {self.symbole})', color='#32CD32')
        ax.tick_params(axis='y', labelcolor='#32CD32')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Taux de fiscalité en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Taux_Fiscalite'], label='Taux de Fiscalité', 
                linewidth=3, color='#FF4500')
        ax2.set_ylabel('Taux de Fiscalité', color='#FF4500')
        ax2.tick_params(axis='y', labelcolor='#FF4500')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_demography(self, df, ax):
        """Plot de l'évolution démographique"""
        ax.plot(df['Annee'], df['Population'], label='Population', 
               linewidth=2, color='#008000', alpha=0.8)
        
        ax.set_title('Évolution Démographique', fontsize=12, fontweight='bold')
        ax.set_ylabel('Population', color='#008000')
        ax.tick_params(axis='y', labelcolor='#008000')
        ax.grid(True, alpha=0.3)
        
        # Nombre de ménages en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Menages'], label='Ménages', 
                linewidth=2, color='#DC143C', alpha=0.8)
        ax2.set_ylabel('Ménages', color='#DC143C')
        ax2.tick_params(axis='y', labelcolor='#DC143C')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_sectorial_investments(self, df, ax):
        """Plot des investissements sectoriels"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Investissement_Agriculture', 'Investissement_Infrastructures', 
                     'Investissement_Sante', 'Investissement_Education', 
                     'Investissement_Eau', 'Investissement_Energie']
        if 'Investissement_Mines' in df.columns:
            categories.append('Investissement_Mines')
        
        colors = ['#008000', '#FFD700', '#DC143C', '#0000FF', '#00CED1', '#4B0082', '#8B4513']
        labels = ['Agriculture', 'Infrastructures', 'Santé', 'Éducation', 'Eau', 'Énergie']
        if 'Investissement_Mines' in df.columns:
            labels.append('Mines')
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title(f'Répartition Sectorielle des Investissements (millions de {self.symbole})', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Montants (millions {self.symbole})')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _generate_financial_insights(self, df):
        """Génère des insights analytiques adaptés au contexte africain"""
        print(f"🏛️ INSIGHTS ANALYTIQUES - Commune de {self.commune}, {self.pays}")
        print("=" * 60)
        
        # 1. Statistiques de base
        print(f"\n1. 📈 STATISTIQUES GÉNÉRALES ({self.symbole}):")
        avg_revenue = df['Recettes_Totales'].mean()
        avg_expenses = df['Depenses_Totales'].mean()
        avg_savings = df['Epargne_Brute'].mean()
        avg_debt = df['Dette_Totale'].mean()
        
        print(f"Recettes moyennes annuelles: {avg_revenue:,.0f} millions {self.symbole}")
        print(f"Dépenses moyennes annuelles: {avg_expenses:,.0f} millions {self.symbole}")
        print(f"Épargne brute moyenne: {avg_savings:,.0f} millions {self.symbole}")
        print(f"Dette moyenne: {avg_debt:,.0f} millions {self.symbole}")
        
        # 2. Croissance (très forte en Afrique)
        print("\n2. 📊 TAUX DE CROISSANCE:")
        revenue_growth = ((df['Recettes_Totales'].iloc[-1] / 
                          df['Recettes_Totales'].iloc[0]) - 1) * 100
        population_growth = ((df['Population'].iloc[-1] / 
                             df['Population'].iloc[0]) - 1) * 100
        
        print(f"Croissance des recettes ({self.start_year}-{self.end_year}): {revenue_growth:.1f}%")
        print(f"Croissance de la population ({self.start_year}-{self.end_year}): {population_growth:.1f}%")
        
        # 3. Structure financière (spécificités africaines)
        print("\n3. 📋 STRUCTURE FINANCIÈRE:")
        tax_share = (df['Impots_Locaux'].mean() / df['Recettes_Totales'].mean()) * 100
        state_share = (df['Subventions_Etat'].mean() / df['Recettes_Totales'].mean()) * 100
        aid_share = (df['Aide_Internationale'].mean() / df['Recettes_Totales'].mean()) * 100
        investment_share = (df['Investissement'].mean() / df['Depenses_Totales'].mean()) * 100
        
        print(f"Part des impôts locaux dans les recettes: {tax_share:.1f}%")
        print(f"Part des subventions de l'État dans les recettes: {state_share:.1f}%")
        print(f"Part de l'aide internationale dans les recettes: {aid_share:.1f}%")
        print(f"Part de l'investissement dans les dépenses: {investment_share:.1f}%")
        
        # 4. Dette et fiscalité
        print("\n4. 💰 ENDETTEMENT ET FISCALITÉ:")
        avg_debt_ratio = df['Taux_Endettement'].mean() * 100
        avg_tax_rate = df['Taux_Fiscalite'].mean()
        last_debt_ratio = df['Taux_Endettement'].iloc[-1] * 100
        
        print(f"Taux d'endettement moyen: {avg_debt_ratio:.1f}%")
        print(f"Taux d'endettement final: {last_debt_ratio:.1f}%")
        print(f"Taux de fiscalité moyen: {avg_tax_rate:.2f}")
        
        # 5. Spécificités de la commune africaine
        print(f"\n5. 🌟 SPÉCIFICITÉS DE {self.commune.upper()} ({self.pays.upper()}):")
        print(f"Type de commune: {self.config['type']}")
        print(f"Spécialités: {', '.join(self.config['specialites'])}")
        print(f"Devise: {self.devise} ({self.symbole})")
        
        # 6. Événements marquants spécifiques à l'Afrique
        print("\n6. 📅 ÉVÉNEMENTS MARQUANTS AFRIQUE:")
        print("• 2002-2008: Période de croissance économique soutenue")
        print("• 2008-2009: Impact de la crise financière mondiale")
        print("• 2010-2014: Croissance post-crise et investissements")
        print("• 2014-2016: Baisse des cours des matières premières")
        print("• 2017-2019: Programmes de développement continental")
        print("• 2020-2021: Impact de la crise COVID-19")
        print("• 2022-2025: Plan de relance et Agenda 2063")
        
        # 7. Recommandations adaptées au contexte africain
        print("\n7. 💡 RECOMMANDATIONS STRATÉGIQUES:")
        if "agriculture" in self.config["specialites"]:
            print("• Moderniser l'agriculture et développer l'agro-industrie")
            print("• Valoriser les filières agricoles locales")
        if "mines" in self.config["specialites"]:
            print("• Développer la transformation locale des minerais")
            print("• Renforcer la responsabilité sociale des entreprises minières")
        if "tourisme" in self.config["specialites"]:
            print("• Promouvoir l'écotourisme et le tourisme culturel")
            print("• Développer les infrastructures d'accueil")
        print("• Investir dans les infrastructures de base (eau, électricité, routes)")
        print("• Renforcer les systèmes de santé et d'éducation")
        print("• Développer l'économie numérique et les technologies")
        print("• Promouvoir l'entreprenariat local et les PME")
        print("• Renforcer la gouvernance locale et la transparence")

def main():
    """Fonction principale pour l'Afrique"""
    # Liste des pays et communes africaines
    communes_par_pays = {
        "Sénégal": ["Dakar", "Saint-Louis", "Tamba", "Thiès", "Kaolack"],
        "Côte d'Ivoire": ["Abidjan", "Bouaké", "Korhogo", "Yamoussoukro", "San-Pédro"],
        "Cameroun": ["Yaoundé", "Douala", "Garoua", "Bafoussam", "Maroua"],
        "Nigeria": ["Lagos", "Abuja", "Kano", "Ibadan", "Port Harcourt"],
        "Ghana": ["Accra", "Kumasi", "Tamale", "Sekondi-Takoradi", "Cape Coast"],
        "Kenya": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"],
        "RDC": ["Kinshasa", "Lubumbashi", "Mbuji-Mayi", "Kananga", "Kisangani"],
        "Afrique du Sud": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth"],
        "Maroc": ["Casablanca", "Marrakech", "Fès", "Tanger", "Rabat"],
        "Algérie": ["Alger", "Oran", "Constantine", "Annaba", "Batna"],
        "Tunisie": ["Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte"]
    }
    
    print("🏛️ ANALYSE DES COMPTES COMMUNAUX EN AFRIQUE (2002-2025)")
    print("=" * 60)
    
    # Demander à l'utilisateur de choisir un pays
    print("Liste des pays disponibles:")
    pays_liste = list(communes_par_pays.keys())
    for i, pays in enumerate(pays_liste, 1):
        print(f"{i}. {pays}")
    
    try:
        choix_pays = int(input("\nChoisissez le numéro du pays: "))
        if choix_pays < 1 or choix_pays > len(pays_liste):
            raise ValueError
        pays_selectionne = pays_liste[choix_pays-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection du Sénégal par défaut.")
        pays_selectionne = "Sénégal"
    
    # Demander à l'utilisateur de choisir une commune
    print(f"\nListe des communes disponibles pour {pays_selectionne}:")
    communes = communes_par_pays[pays_selectionne]
    for i, commune in enumerate(communes, 1):
        print(f"{i}. {commune}")
    
    try:
        choix_commune = int(input("\nChoisissez le numéro de la commune à analyser: "))
        if choix_commune < 1 or choix_commune > len(communes):
            raise ValueError
        commune_selectionnee = communes[choix_commune-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection de la capitale par défaut.")
        commune_selectionnee = communes[0]
    
    # Initialiser l'analyseur
    analyzer = AfriqueCommuneFinanceAnalyzer(commune_selectionnee, pays_selectionne)
    
    # Générer les données
    financial_data = analyzer.generate_financial_data()
    
    # Sauvegarder les données
    output_file = f'{commune_selectionnee}_{pays_selectionne}_financial_data_2002_2025.csv'
    financial_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print(f"\n👀 Aperçu des données (en millions de {analyzer.symbole}):")
    print(financial_data[['Annee', 'Population', 'Recettes_Totales', 'Depenses_Totales', 'Dette_Totale']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse financière...")
    analyzer.create_financial_analysis(financial_data)
    
    print(f"\n✅ Analyse des comptes communaux de {commune_selectionnee}, {pays_selectionne} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print(f"💰 Devise: {analyzer.devise} ({analyzer.symbole})")
    print("📦 Données: Démographie, finances, investissements, dette")

if __name__ == "__main__":
    main()