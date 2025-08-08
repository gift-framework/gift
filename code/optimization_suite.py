#!/usr/bin/env python3
"""
optimization_suite.py
GIFT v3.0 - Optimization Methods Suite

Comprehensive optimization suite for the GIFT framework including:
- Multiple optimization algorithms (L-BFGS-B, Differential Evolution, SLSQP)
- Robustness analysis and Monte Carlo validation
- Sensitivity analysis and cross-validation
- Multi-restart strategies

GitHub: https://github.com/gift-framework/gift
License: MIT
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution, basinhopping, dual_annealing
from scipy.stats import chi2, normaltest
import time
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
import hashlib
import json

# Import GIFT protocol
try:
    from gift_v3_protocol import (
        GIFTProtocol, M6Coordinates, InitialConditions,
        ZETA3_CBRT, format_coordinates
    )
except ImportError:
    print("Error: gift_v3_protocol.py required")
    print("Please ensure gift_v3_protocol.py is in the same directory")
    exit(1)

# ==============================================================================
# OPTIMIZATION CONFIGURATION
# ==============================================================================

@dataclass
class OptimizationConfig:
    """Configuration for optimization runs"""
    max_iterations: int = 500
    function_tolerance: float = 1e-10
    gradient_tolerance: float = 1e-8
    parameter_tolerance: float = 1e-9
    n_restarts: int = 4
    n_monte_carlo: int = 100
    noise_level: float = 0.1
    seed: int = 42

# ==============================================================================
# OPTIMIZATION ALGORITHMS
# ==============================================================================

class OptimizationAlgorithms:
    """
    Collection of optimization algorithms for GIFT framework
    Section 3.1: Computational protocol
    """
    
    def __init__(self, protocol: GIFTProtocol, config: OptimizationConfig):
        self.protocol = protocol
        self.config = config
        np.random.seed(config.seed)
    
    def lbfgs_optimize(self, domain: str, target: float, 
                       x0: Optional[np.ndarray] = None) -> Dict:
        """
        L-BFGS-B optimization (primary method)
        Limited-memory Broyden-Fletcher-Goldfarb-Shanno with bounds
        """
        if x0 is None:
            x0 = InitialConditions.get_domain_conditions(domain).to_array()
        
        start_time = time.time()
        
        result = minimize(
            lambda x: self.protocol.objective_function(x, domain, target),
            x0,
            method='L-BFGS-B',
            bounds=self.protocol.get_bounds(),
            options={
                'maxiter': self.config.max_iterations,
                'ftol': self.config.function_tolerance,
                'gtol': self.config.gradient_tolerance
            }
        )
        
        elapsed = time.time() - start_time
        coords = M6Coordinates.from_array(result.x)
        validation = self.protocol.validate_solution(coords, domain)
        
        return {
            'method': 'L-BFGS-B',
            'coords': coords,
            'success': result.success and validation['success'],
            'iterations': result.nit,
            'function_evals': result.nfev,
            'objective': result.fun,
            'time': elapsed,
            'validation': validation,
            'message': result.message
        }
    
    def differential_evolution_optimize(self, domain: str, target: float) -> Dict:
        """
        Differential Evolution (global optimization)
        Stochastic population-based algorithm
        """
        start_time = time.time()
        
        result = differential_evolution(
            lambda x: self.protocol.objective_function(x, domain, target),
            self.protocol.get_bounds(),
            seed=self.config.seed,
            maxiter=self.config.max_iterations // 5,  # Fewer iterations for DE
            tol=self.config.function_tolerance,
            popsize=15,
            mutation=(0.5, 1.5),
            recombination=0.7,
            workers=1,
            updating='deferred'
        )
        
        elapsed = time.time() - start_time
        coords = M6Coordinates.from_array(result.x)
        validation = self.protocol.validate_solution(coords, domain)
        
        return {
            'method': 'Differential Evolution',
            'coords': coords,
            'success': result.success and validation['success'],
            'iterations': result.nit,
            'function_evals': result.nfev,
            'objective': result.fun,
            'time': elapsed,
            'validation': validation,
            'message': result.message
        }
    
    def slsqp_optimize(self, domain: str, target: float,
                      x0: Optional[np.ndarray] = None) -> Dict:
        """
        Sequential Least Squares Programming
        Sequential quadratic programming for constrained optimization
        """
        if x0 is None:
            x0 = InitialConditions.get_domain_conditions(domain).to_array()
        
        # Constraint: E/M should be close to ζ(3)^(1/3)
        def em_constraint(x):
            E, M = x[1], x[2]
            if M > 0.1:
                return abs(E/M - ZETA3_CBRT) - 0.1  # Allow 10% deviation
            return 0
        
        start_time = time.time()
        
        result = minimize(
            lambda x: self.protocol.objective_function(x, domain, target),
            x0,
            method='SLSQP',
            bounds=self.protocol.get_bounds(),
            constraints={'type': 'ineq', 'fun': lambda x: -em_constraint(x)},
            options={
                'maxiter': self.config.max_iterations,
                'ftol': self.config.function_tolerance
            }
        )
        
        elapsed = time.time() - start_time
        coords = M6Coordinates.from_array(result.x)
        validation = self.protocol.validate_solution(coords, domain)
        
        return {
            'method': 'SLSQP',
            'coords': coords,
            'success': result.success and validation['success'],
            'iterations': result.nit,
            'function_evals': result.nfev,
            'objective': result.fun,
            'time': elapsed,
            'validation': validation,
            'message': result.message
        }
    
    def basin_hopping_optimize(self, domain: str, target: float,
                              x0: Optional[np.ndarray] = None) -> Dict:
        """
        Basin Hopping (global optimization)
        Monte Carlo with local minimization
        """
        if x0 is None:
            x0 = InitialConditions.get_domain_conditions(domain).to_array()
        
        start_time = time.time()
        
        result = basinhopping(
            lambda x: self.protocol.objective_function(x, domain, target),
            x0,
            niter=100,
            T=1.0,
            stepsize=0.5,
            minimizer_kwargs={
                'method': 'L-BFGS-B',
                'bounds': self.protocol.get_bounds()
            },
            seed=self.config.seed
        )
        
        elapsed = time.time() - start_time
        coords = M6Coordinates.from_array(result.x)
        validation = self.protocol.validate_solution(coords, domain)
        
        return {
            'method': 'Basin Hopping',
            'coords': coords,
            'success': result.lowest_optimization_result.success and validation['success'],
            'iterations': result.nit,
            'function_evals': result.nfev,
            'objective': result.fun,
            'time': elapsed,
            'validation': validation,
            'message': result.message
        }
    
    def dual_annealing_optimize(self, domain: str, target: float) -> Dict:
        """
        Dual Annealing (global optimization)
        Simulated annealing with adaptive temperature
        """
        start_time = time.time()
        
        result = dual_annealing(
            lambda x: self.protocol.objective_function(x, domain, target),
            self.protocol.get_bounds(),
            seed=self.config.seed,
            maxiter=self.config.max_iterations,
            visit=2.62,
            accept=-5.0,
            maxfun=10000
        )
        
        elapsed = time.time() - start_time
        coords = M6Coordinates.from_array(result.x)
        validation = self.protocol.validate_solution(coords, domain)
        
        return {
            'method': 'Dual Annealing',
            'coords': coords,
            'success': result.success and validation['success'],
            'iterations': result.nit,
            'function_evals': result.nfev,
            'objective': result.fun,
            'time': elapsed,
            'validation': validation,
            'message': result.message
        }

# ==============================================================================
# MULTI-RESTART OPTIMIZATION
# ==============================================================================

class MultiRestartOptimizer:
    """
    Multi-restart optimization strategy
    Escapes local minima through multiple initializations
    """
    
    def __init__(self, algorithms: OptimizationAlgorithms):
        self.algorithms = algorithms
        self.config = algorithms.config
        self.protocol = algorithms.protocol
    
    def optimize_with_restarts(self, domain: str, target: float,
                              methods: List[str] = ['L-BFGS-B']) -> Dict:
        """
        Optimize with multiple restarts and methods
        """
        all_results = []
        best_result = None
        best_error = float('inf')
        
        for restart in range(self.config.n_restarts):
            # Perturbed initial conditions
            base_coords = InitialConditions.get_domain_conditions(domain)
            noise = np.random.normal(0, self.config.noise_level, 6)
            x0 = np.clip(base_coords.to_array() + noise, 0.01, 10.0)
            
            for method in methods:
                # Select optimization method
                if method == 'L-BFGS-B':
                    result = self.algorithms.lbfgs_optimize(domain, target, x0)
                elif method == 'Differential Evolution':
                    result = self.algorithms.differential_evolution_optimize(domain, target)
                elif method == 'SLSQP':
                    result = self.algorithms.slsqp_optimize(domain, target, x0)
                elif method == 'Basin Hopping':
                    result = self.algorithms.basin_hopping_optimize(domain, target, x0)
                elif method == 'Dual Annealing':
                    result = self.algorithms.dual_annealing_optimize(domain, target)
                else:
                    continue
                
                result['restart'] = restart
                all_results.append(result)
                
                # Update best result
                error = result['validation']['error']
                if error < best_error and result['validation']['nontrivial']:
                    best_error = error
                    best_result = result
        
        return {
            'best_result': best_result,
            'all_results': all_results,
            'n_successful': sum(1 for r in all_results if r['success']),
            'n_total': len(all_results),
            'success_rate': sum(1 for r in all_results if r['success']) / len(all_results)
        }

# ==============================================================================
# ROBUSTNESS ANALYSIS
# ==============================================================================

class RobustnessAnalysis:
    """
    Statistical robustness testing
    Section 3.1: Validation methodology
    """
    
    def __init__(self, optimizer: MultiRestartOptimizer):
        self.optimizer = optimizer
        self.config = optimizer.config
        self.protocol = optimizer.protocol
    
    def monte_carlo_validation(self, domain: str, target: float) -> Dict:
        """
        Monte Carlo validation with perturbed initial conditions
        Tests stability under random perturbations
        """
        results = []
        successful_coords = []
        observables = []
        
        for trial in range(self.config.n_monte_carlo):
            # Random perturbation
            base_coords = InitialConditions.get_domain_conditions(domain)
            noise = np.random.normal(0, self.config.noise_level, 6)
            x0 = np.clip(base_coords.to_array() + noise, 0.01, 10.0)
            
            # Optimize
            result = self.optimizer.algorithms.lbfgs_optimize(domain, target, x0)
            results.append(result)
            
            if result['success']:
                successful_coords.append(result['coords'].to_array())
                observables.append(result['validation']['observable'])
        
        if successful_coords:
            successful_coords = np.array(successful_coords)
            
            # Statistics
            mean_coords = np.mean(successful_coords, axis=0)
            std_coords = np.std(successful_coords, axis=0)
            cov_matrix = np.cov(successful_coords.T)
            
            # Observable statistics
            obs_mean = np.mean(observables)
            obs_std = np.std(observables)
            
            # Normality test
            if len(observables) > 3:
                stat, p_value = normaltest(observables)
            else:
                p_value = 0.0
            
            success_rate = len(successful_coords) / self.config.n_monte_carlo
            
            return {
                'success_rate': success_rate,
                'n_trials': self.config.n_monte_carlo,
                'mean_coords': mean_coords,
                'std_coords': std_coords,
                'covariance': cov_matrix,
                'observable_mean': obs_mean,
                'observable_std': obs_std,
                'normality_p': p_value,
                'robust': success_rate > 0.8 and obs_std / (obs_mean + 1e-10) < 0.1
            }
        else:
            return {
                'success_rate': 0.0,
                'n_trials': self.config.n_monte_carlo,
                'robust': False
            }
    
    def sensitivity_analysis(self, coords: M6Coordinates, domain: str) -> Dict:
        """
        Sensitivity analysis: ∂Observable/∂Coordinate
        """
        base_obs = self.protocol.extractor.extract(coords, domain)
        sensitivities = {}
        
        delta = 0.01  # Perturbation size
        coord_names = ['S', 'E', 'M', 'C', 'N', 'F']
        x = coords.to_array()
        
        for i, name in enumerate(coord_names):
            # Forward difference
            x_plus = x.copy()
            x_plus[i] += delta
            obs_plus = self.protocol.extractor.extract(
                M6Coordinates.from_array(x_plus), domain
            )
            
            # Backward difference
            x_minus = x.copy()
            x_minus[i] -= delta
            obs_minus = self.protocol.extractor.extract(
                M6Coordinates.from_array(x_minus), domain
            )
            
            # Central difference derivative
            derivative = (obs_plus - obs_minus) / (2 * delta)
            
            # Relative sensitivity
            relative = derivative * x[i] / (base_obs + 1e-10)
            
            sensitivities[name] = {
                'absolute': derivative,
                'relative': relative,
                'normalized': abs(relative)
            }
        
        # Identify dominant parameters
        max_sensitivity = max(s['normalized'] for s in sensitivities.values())
        dominant = [name for name, s in sensitivities.items()
                   if s['normalized'] > 0.5 * max_sensitivity]
        
        return {
            'sensitivities': sensitivities,
            'dominant_parameters': dominant,
            'base_observable': base_obs
        }
    
    def cross_validation(self, domains: List[str], k_folds: int = 5) -> Dict:
        """
        K-fold cross-validation across domains
        """
        n_domains = len(domains)
        fold_size = n_domains // k_folds
        cv_results = []
        
        for fold in range(k_folds):
            # Split domains
            test_start = fold * fold_size
            test_end = test_start + fold_size if fold < k_folds - 1 else n_domains
            
            test_domains = domains[test_start:test_end]
            train_domains = domains[:test_start] + domains[test_end:]
            
            # Train: optimize on training domains
            train_coords = []
            for domain in train_domains:
                target = self.protocol.domains[domain]['target']
                result = self.optimizer.algorithms.lbfgs_optimize(domain, target)
                if result['success']:
                    train_coords.append(result['coords'].to_array())
            
            if train_coords:
                # Average training coordinates
                mean_coords = M6Coordinates.from_array(np.mean(train_coords, axis=0))
                
                # Test: evaluate on test domains
                test_errors = []
                for domain in test_domains:
                    predicted = self.protocol.extractor.extract(mean_coords, domain)
                    actual = self.protocol.domains[domain]['target']
                    error = abs(predicted - actual) / (actual + 1e-10)
                    test_errors.append(error)
                
                cv_results.append({
                    'fold': fold,
                    'mean_error': np.mean(test_errors),
                    'std_error': np.std(test_errors)
                })
        
        if cv_results:
            mean_errors = [r['mean_error'] for r in cv_results]
            return {
                'cv_results': cv_results,
                'mean_cv_error': np.mean(mean_errors),
                'std_cv_error': np.std(mean_errors),
                'k_folds': k_folds
            }
        else:
            return {'mean_cv_error': 1.0, 'k_folds': k_folds}

# ==============================================================================
# OPTIMIZATION SUITE
# ==============================================================================

class OptimizationSuite:
    """
    Complete optimization suite orchestration
    """
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        self.config = config or OptimizationConfig()
        self.protocol = GIFTProtocol()
        self.algorithms = OptimizationAlgorithms(self.protocol, self.config)
        self.multi_restart = MultiRestartOptimizer(self.algorithms)
        self.robustness = RobustnessAnalysis(self.multi_restart)
    
    def run_comprehensive_optimization(self, domain: str, 
                                      methods: List[str] = ['L-BFGS-B']) -> Dict:
        """
        Run comprehensive optimization for a single domain
        """
        target = self.protocol.domains[domain]['target']
        
        # Multi-restart optimization
        opt_results = self.multi_restart.optimize_with_restarts(domain, target, methods)
        
        # Robustness analysis
        if self.config.n_monte_carlo > 0:
            monte_carlo = self.robustness.monte_carlo_validation(domain, target)
        else:
            monte_carlo = None
        
        # Sensitivity analysis
        if opt_results['best_result']:
            sensitivity = self.robustness.sensitivity_analysis(
                opt_results['best_result']['coords'], domain
            )
        else:
            sensitivity = None
        
        return {
            'domain': domain,
            'target': target,
            'optimization': opt_results,
            'monte_carlo': monte_carlo,
            'sensitivity': sensitivity
        }
    
    def run_all_domains(self, methods: List[str] = ['L-BFGS-B']) -> Dict:
        """
        Run optimization for all domains
        """
        results = {}
        
        print("="*60)
        print("GIFT v3.0 - Optimization Suite")
        print(f"Methods: {', '.join(methods)}")
        print(f"Restarts: {self.config.n_restarts}")
        print(f"Monte Carlo trials: {self.config.n_monte_carlo}")
        print("="*60)
        
        for domain in self.protocol.domains.keys():
            print(f"\nOptimizing {domain}...")
            results[domain] = self.run_comprehensive_optimization(domain, methods)
            
            # Display summary
            best = results[domain]['optimization']['best_result']
            if best:
                print(f"  Best method: {best['method']}")
                print(f"  Observable: {best['validation']['observable']:.4f}")
                print(f"  Error: {best['validation']['error_percent']:.2f}%")
                print(f"  Coordinates: {format_coordinates(best['coords'])}")
                
                if results[domain]['monte_carlo']:
                    mc = results[domain]['monte_carlo']
                    print(f"  Robustness: {mc['success_rate']*100:.1f}% success rate")
        
        # Cross-validation
        print("\nRunning cross-validation...")
        cv_results = self.robustness.cross_validation(list(self.protocol.domains.keys()))
        
        # Summary statistics
        successful = sum(1 for r in results.values() 
                        if r['optimization']['best_result'] and 
                        r['optimization']['best_result']['success'])
        
        print("\n" + "="*60)
        print("OPTIMIZATION SUMMARY")
        print("="*60)
        print(f"Successful domains: {successful}/{len(results)}")
        print(f"Cross-validation error: {cv_results['mean_cv_error']:.3f}")
        
        # Reproducibility hash
        config_str = json.dumps({
            'methods': methods,
            'config': self.config.__dict__,
            'domains': list(self.protocol.domains.keys())
        }, sort_keys=True)
        
        hash_value = hashlib.sha256(config_str.encode()).hexdigest()[:16]
        print(f"Reproducibility hash: {hash_value}")
        
        return {
            'domain_results': results,
            'cross_validation': cv_results,
            'summary': {
                'successful': successful,
                'total': len(results),
                'success_rate': successful / len(results),
                'hash': hash_value
            }
        }
    
    def benchmark_methods(self, domain: str) -> Dict:
        """
        Benchmark different optimization methods
        """
        target = self.protocol.domains[domain]['target']
        methods = ['L-BFGS-B', 'Differential Evolution', 'SLSQP', 
                  'Basin Hopping', 'Dual Annealing']
        
        results = {}
        
        print(f"\nBenchmarking methods for {domain}")
        print("-"*40)
        
        for method in methods:
            print(f"Testing {method}...")
            start = time.time()
            
            if method == 'L-BFGS-B':
                result = self.algorithms.lbfgs_optimize(domain, target)
            elif method == 'Differential Evolution':
                result = self.algorithms.differential_evolution_optimize(domain, target)
            elif method == 'SLSQP':
                result = self.algorithms.slsqp_optimize(domain, target)
            elif method == 'Basin Hopping':
                result = self.algorithms.basin_hopping_optimize(domain, target)
            elif method == 'Dual Annealing':
                result = self.algorithms.dual_annealing_optimize(domain, target)
            
            results[method] = result
            
            print(f"  Time: {result['time']:.3f}s")
            print(f"  Error: {result['validation']['error_percent']:.2f}%")
            print(f"  Success: {result['success']}")
        
        # Find best method
        best_method = min(results.items(), 
                         key=lambda x: x[1]['validation']['error'])
        
        return {
            'results': results,
            'best_method': best_method[0],
            'best_error': best_method[1]['validation']['error_percent']
        }

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """
    Main execution for optimization suite
    """
    # Configuration
    config = OptimizationConfig(
        max_iterations=500,
        n_restarts=2,  # Reduced for faster demo
        n_monte_carlo=20,  # Reduced for faster demo
        seed=42
    )
    
    # Initialize suite
    suite = OptimizationSuite(config)
    
    # Option 1: Run comprehensive optimization for all domains
    print("\n1. Running comprehensive optimization...")
    all_results = suite.run_all_domains(methods=['L-BFGS-B', 'Differential Evolution'])
    
    # Option 2: Benchmark methods for a specific domain
    print("\n2. Benchmarking methods for quantum_mechanics...")
    benchmark = suite.benchmark_methods('quantum_mechanics')
    print(f"Best method: {benchmark['best_method']} (error: {benchmark['best_error']:.2f}%)")
    
    # Option 3: Detailed analysis for a single domain
    print("\n3. Detailed analysis for cosmology_hubble...")
    detailed = suite.run_comprehensive_optimization('cosmology_hubble', 
                                                   methods=['L-BFGS-B'])
    
    if detailed['sensitivity']:
        print("\nSensitivity analysis:")
        for param, sens in detailed['sensitivity']['sensitivities'].items():
            print(f"  ∂O/∂{param} = {sens['absolute']:.3e} (relative: {sens['relative']:.3f})")
        print(f"  Dominant: {detailed['sensitivity']['dominant_parameters']}")
    
    return all_results

if __name__ == "__main__":
    results = main()