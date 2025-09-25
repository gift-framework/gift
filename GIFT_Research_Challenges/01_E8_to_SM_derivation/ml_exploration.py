"""
ML Exploration pour la Dérivation E₈×E₈ → SU(3)×SU(2)×U(1)
Utilise des techniques de ML pour découvrir de nouvelles relations et optimiser les dérivations
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import sympy as sp
from sympy import symbols, Matrix, simplify, expand
import warnings
warnings.filterwarnings('ignore')

# Import des outils GIFT
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared_tools'))
from gift_parameters import GIFTParameters, E8GroupTheory, ChiralSymmetryAnalysis

class E8DecompositionML:
    """Exploration ML des décompositions E₈×E₈"""
    
    def __init__(self):
        self.gift = GIFTParameters()
        self.e8 = E8GroupTheory()
        self.chiral = ChiralSymmetryAnalysis()
        
        # Données de décomposition
        self.decomposition_data = self._generate_decomposition_data()
        
    def _generate_decomposition_data(self):
        """Génère des données de décomposition pour l'entraînement ML"""
        data = []
        
        # Chemins de décomposition possibles
        paths = self.e8.e8_decomposition_paths()
        
        for path_name, path in paths.items():
            for i, group in enumerate(path):
                # Caractéristiques du groupe
                dim = self.e8.dimensions.get(group, 0)
                rank = self.e8.ranks.get(group, 0)
                info_content = self.e8.calculate_information_content(group)
                
                # Position dans le chemin
                position = i / (len(path) - 1) if len(path) > 1 else 0
                
                # Caractéristiques du chemin
                path_length = len(path)
                is_final = (i == len(path) - 1)
                is_initial = (i == 0)
                
                # Relations avec les paramètres GIFT
                xi_relation = dim * self.gift.xi
                tau_relation = rank * self.gift.tau
                beta0_relation = info_content * self.gift.beta0
                delta_relation = position * self.gift.delta
                
                data.append({
                    'group': group,
                    'dimension': dim,
                    'rank': rank,
                    'info_content': info_content,
                    'position': position,
                    'path_length': path_length,
                    'is_final': is_final,
                    'is_initial': is_initial,
                    'xi_relation': xi_relation,
                    'tau_relation': tau_relation,
                    'beta0_relation': beta0_relation,
                    'delta_relation': delta_relation,
                    'path_name': path_name
                })
        
        return pd.DataFrame(data)
    
    def train_decomposition_predictor(self):
        """Entraîne un modèle ML pour prédire les décompositions optimales"""
        # Préparation des données
        X = self.decomposition_data[['dimension', 'rank', 'info_content', 'position', 
                                   'xi_relation', 'tau_relation', 'beta0_relation', 'delta_relation']]
        y = self.decomposition_data['is_final'].astype(int)
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Modèles à tester
        models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Neural Network': MLPRegressor(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
        }
        
        results = {}
        for name, model in models.items():
            # Entraînement
            model.fit(X_train, y_train)
            
            # Prédictions
            y_pred = model.predict(X_test)
            
            # Métriques
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            results[name] = {
                'model': model,
                'mse': mse,
                'r2': r2,
                'predictions': y_pred
            }
            
            print(f"{name}:")
            print(f"  MSE: {mse:.6f}")
            print(f"  R²: {r2:.6f}")
        
        return results
    
    def analyze_optimal_paths(self):
        """Analyse les chemins de décomposition optimaux"""
        # Calcul des scores pour chaque chemin
        path_scores = {}
        
        for path_name in self.decomposition_data['path_name'].unique():
            path_data = self.decomposition_data[self.decomposition_data['path_name'] == path_name]
            
            # Score basé sur l'efficacité de réduction
            total_info_loss = 0
            for i in range(len(path_data) - 1):
                current_info = path_data.iloc[i]['info_content']
                next_info = path_data.iloc[i+1]['info_content']
                if current_info > 0:
                    loss = (current_info - next_info) / current_info
                    total_info_loss += loss
            
            # Score basé sur la cohérence avec les paramètres GIFT
            gift_coherence = 0
            for _, row in path_data.iterrows():
                coherence = (row['xi_relation'] + row['tau_relation'] + 
                           row['beta0_relation'] + row['delta_relation']) / 4
                gift_coherence += coherence
            
            # Score combiné
            path_scores[path_name] = {
                'info_loss': total_info_loss,
                'gift_coherence': gift_coherence,
                'combined_score': gift_coherence - total_info_loss
            }
        
        return path_scores
    
    def discover_new_relations(self):
        """Découvre de nouvelles relations mathématiques"""
        # Analyse des patterns dans les décompositions
        patterns = {}
        
        # Pattern 1: Relations dimension-rang
        dimensions = self.decomposition_data['dimension'].values
        ranks = self.decomposition_data['rank'].values
        
        # Régression polynomiale
        coeffs = np.polyfit(ranks, dimensions, 2)
        patterns['dimension_rank_poly'] = coeffs
        
        # Pattern 2: Relations avec les paramètres GIFT
        xi_relations = self.decomposition_data['xi_relation'].values
        tau_relations = self.decomposition_data['tau_relation'].values
        
        # Corrélation
        correlation = np.corrcoef(xi_relations, tau_relations)[0, 1]
        patterns['xi_tau_correlation'] = correlation
        
        # Pattern 3: Efficacité de réduction
        positions = self.decomposition_data['position'].values
        info_contents = self.decomposition_data['info_content'].values
        
        # Régression exponentielle
        log_info = np.log(info_contents + 1)  # +1 pour éviter log(0)
        coeffs_exp = np.polyfit(positions, log_info, 1)
        patterns['info_decay_exponential'] = coeffs_exp
        
        return patterns
    
    def optimize_gift_parameters(self):
        """Optimise les paramètres GIFT pour la décomposition"""
        def objective(params):
            xi, tau, beta0, delta = params
            
            # Calcul des prédictions avec les nouveaux paramètres
            predictions = self._calculate_predictions_with_params(xi, tau, beta0, delta)
            
            # Calcul de l'erreur par rapport aux données expérimentales
            error = 0
            for obs, pred in predictions.items():
                if obs in self.gift.experimental_data:
                    exp_val = self.gift.experimental_data[obs]
                    error += abs(pred - exp_val) / exp_val
            
            return error
        
        # Paramètres initiaux
        initial_params = [self.gift.xi, self.gift.tau, self.gift.beta0, self.gift.delta]
        
        # Optimisation
        from scipy.optimize import minimize
        result = minimize(objective, initial_params, method='Nelder-Mead')
        
        return {
            'optimized_params': result.x,
            'initial_params': initial_params,
            'improvement': result.fun,
            'success': result.success
        }
    
    def _calculate_predictions_with_params(self, xi, tau, beta0, delta):
        """Calcule les prédictions avec des paramètres donnés"""
        predictions = {}
        
        # Électromagnétique
        predictions['alpha_inv_0'] = 1.2020569031595942 * 114  # zeta3 * 114
        predictions['alpha_inv_MZ'] = 128 - 1/24
        
        # Électrofaible
        predictions['sin2_theta_W'] = np.pi**2/6 - np.sqrt(2)  # zeta2 - sqrt(2)
        
        # Fort
        predictions['alpha_s_MZ'] = np.sqrt(2) / 12
        
        # Cosmologique
        predictions['H0'] = 67.36 * ((1.2020569031595942/xi)**beta0)
        
        return predictions
    
    def visualize_decomposition_analysis(self):
        """Visualise l'analyse des décompositions"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Dimensions vs Rangs
        axes[0, 0].scatter(self.decomposition_data['rank'], self.decomposition_data['dimension'], 
                          c=self.decomposition_data['position'], cmap='viridis')
        axes[0, 0].set_xlabel('Rang')
        axes[0, 0].set_ylabel('Dimension')
        axes[0, 0].set_title('Dimension vs Rang des Groupes')
        
        # 2. Contenu Informationnel
        axes[0, 1].plot(self.decomposition_data['position'], self.decomposition_data['info_content'], 'o-')
        axes[0, 1].set_xlabel('Position dans le Chemin')
        axes[0, 1].set_ylabel('Contenu Informationnel')
        axes[0, 1].set_title('Évolution du Contenu Informationnel')
        
        # 3. Relations avec les Paramètres GIFT
        axes[1, 0].scatter(self.decomposition_data['xi_relation'], 
                          self.decomposition_data['tau_relation'],
                          c=self.decomposition_data['is_final'], cmap='coolwarm')
        axes[1, 0].set_xlabel('Relation avec ξ')
        axes[1, 0].set_ylabel('Relation avec τ')
        axes[1, 0].set_title('Relations avec les Paramètres GIFT')
        
        # 4. Scores des Chemins
        path_scores = self.analyze_optimal_paths()
        path_names = list(path_scores.keys())
        combined_scores = [path_scores[name]['combined_score'] for name in path_names]
        
        axes[1, 1].bar(path_names, combined_scores)
        axes[1, 1].set_xlabel('Chemin de Décomposition')
        axes[1, 1].set_ylabel('Score Combiné')
        axes[1, 1].set_title('Scores des Chemins de Décomposition')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def generate_synthesis_report(self):
        """Génère un rapport de synthèse de l'analyse ML"""
        # Entraînement des modèles
        ml_results = self.train_decomposition_predictor()
        
        # Analyse des chemins optimaux
        path_scores = self.analyze_optimal_paths()
        
        # Découverte de nouvelles relations
        patterns = self.discover_new_relations()
        
        # Optimisation des paramètres
        optimization = self.optimize_gift_parameters()
        
        report = f"""
# Rapport de Synthèse - Exploration ML E₈×E₈ → SU(3)×SU(2)×U(1)

## Résultats des Modèles ML

"""
        for name, result in ml_results.items():
            report += f"""
### {name}
- MSE: {result['mse']:.6f}
- R²: {result['r2']:.6f}
"""
        
        report += f"""

## Analyse des Chemins de Décomposition

"""
        for path_name, scores in path_scores.items():
            report += f"""
### {path_name}
- Perte d'information: {scores['info_loss']:.6f}
- Cohérence GIFT: {scores['gift_coherence']:.6f}
- Score combiné: {scores['combined_score']:.6f}
"""
        
        report += f"""

## Nouvelles Relations Découvertes

- Corrélation ξ-τ: {patterns['xi_tau_correlation']:.6f}
- Décroissance exponentielle: {patterns['info_decay_exponential']}
- Relation dimension-rang: {patterns['dimension_rank_poly']}

## Optimisation des Paramètres GIFT

- Paramètres initiaux: {optimization['initial_params']}
- Paramètres optimisés: {optimization['optimized_params']}
- Amélioration: {optimization['improvement']:.6f}
- Succès: {optimization['success']}

## Conclusions

L'analyse ML révèle des patterns intéressants dans les décompositions E₈×E₈ et suggère des optimisations possibles des paramètres GIFT.
"""
        
        return report

def main():
    """Fonction principale pour l'exploration ML"""
    print("=== Exploration ML: E₈×E₈ → SU(3)×SU(2)×U(1) ===")
    
    # Initialisation
    ml_explorer = E8DecompositionML()
    
    # Analyse des données
    print("\n1. Analyse des données de décomposition...")
    print(f"Nombre de groupes analysés: {len(ml_explorer.decomposition_data)}")
    print(f"Chemins de décomposition: {len(ml_explorer.decomposition_data['path_name'].unique())}")
    
    # Entraînement des modèles
    print("\n2. Entraînement des modèles ML...")
    ml_results = ml_explorer.train_decomposition_predictor()
    
    # Analyse des chemins optimaux
    print("\n3. Analyse des chemins optimaux...")
    path_scores = ml_explorer.analyze_optimal_paths()
    best_path = max(path_scores.keys(), key=lambda x: path_scores[x]['combined_score'])
    print(f"Meilleur chemin: {best_path}")
    
    # Découverte de nouvelles relations
    print("\n4. Découverte de nouvelles relations...")
    patterns = ml_explorer.discover_new_relations()
    print(f"Corrélation ξ-τ: {patterns['xi_tau_correlation']:.6f}")
    
    # Optimisation des paramètres
    print("\n5. Optimisation des paramètres GIFT...")
    optimization = ml_explorer.optimize_gift_parameters()
    print(f"Amélioration possible: {optimization['improvement']:.6f}")
    
    # Visualisation
    print("\n6. Génération des visualisations...")
    ml_explorer.visualize_decomposition_analysis()
    
    # Rapport de synthèse
    print("\n7. Génération du rapport de synthèse...")
    report = ml_explorer.generate_synthesis_report()
    
    # Sauvegarde du rapport
    with open('ml_exploration_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n=== Exploration ML Terminée ===")
    print("Rapport sauvegardé dans: ml_exploration_report.md")

if __name__ == "__main__":
    main()
