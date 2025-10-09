// GIFT Predictions Calculator Engine
// Based on rigorous derivations from gift_support_notebook.ipynb

class GIFTCalculator {
    constructor() {
        // Geometric parameters from E8×E8 → AdS4×K7 → SM
        this.xi = 5 * Math.PI / 16;        // 0.981748 (bulk-boundary correspondence)
        this.tau = 8 * Math.pow(0.5772156649, 5 * Math.PI / 12);  // 3.896568 (information processing)
        this.beta0 = Math.PI / 8;          // 0.392699 (dimensional anomaly)
        this.delta = 2 * Math.PI / 25;     // 0.251327 (Koide correction)
        
        // Mathematical constants
        this.zeta2 = Math.PI**2 / 6;       // 1.644934 (Basel constant)
        this.zeta3 = 1.2020569031595942;   // Apéry constant
        this.gamma = 0.5772156649;         // Euler-Mascheroni constant
        this.phi = (1 + Math.sqrt(5)) / 2; // Golden ratio
        this.e = Math.E;                   // Natural logarithm base
        
        // k-factor from exceptional Jordan algebra J3(O)
        this.k = 27 - this.gamma + 1/24;   // 26.464068
        
        // Cohomological correction factors
        this.factor_99 = 99;   // H*(K7) = C^1 ⊕ C^21 ⊕ C^77 = C^99
        this.factor_114 = 114; // 99 + 15 (E8 correction)
        this.factor_38 = 38;   // 99 - 61 (complement)
        
        // Dual correction families
        this.F_alpha = 98.999; // Single-sector abundance optimization
        this.F_beta = 99.734;  // Multi-sector mixing coordination
        
        // Experimental data - 22 fundamental observables
        this.experimental_data = {
            // Electromagnetic sector
            alpha_inv_0: 137.035999139,
            alpha_inv_MZ: 128.962,
            
            // Electroweak sector
            sin2_theta_W: 0.23122,
            M_W: 80.379,
            G_F: 1.1664e-5,
            
            // Strong sector
            alpha_s_MZ: 0.1179,
            Lambda_QCD: 218.0,
            f_pi: 130.4,
            
            // Scalar sector
            lambda_H: 0.129,
            m_H: 125.25,
            
            // Fermion sector
            Q_koide: 0.373038,
            
            // Neutrino sector
            theta13: 8.57,
            theta23: 49.2,
            theta12: 33.44,
            delta_CP: 230.0,
            
            // Cosmological sector
            H0: 73.04,
            Omega_DE: 0.6889,
            n_s: 0.9649,
        };
        
        this.initializeObservables();
    }
    
    initializeObservables() {
        this.observables = {
            alpha_inv_0: {
                name: "Fine Structure Constant α⁻¹",
                unit: "",
                gift_formula: "ζ(3) × 114",
                gift_value: () => this.zeta3 * this.factor_114,
                derivation: "Electromagnetic coupling from K7 cohomology structure"
            },
            alpha_inv_MZ: {
                name: "α⁻¹(MZ)",
                unit: "",
                gift_formula: "128 - 1/24",
                gift_value: () => 128 - 1/24,
                derivation: "Running coupling at MZ scale with geometric correction"
            },
            sin2_theta_W: {
                name: "Weak Mixing Angle sin²θ_W",
                unit: "",
                gift_formula: "ζ(2) - √2",
                gift_value: () => this.zeta2 - Math.sqrt(2),
                derivation: "Weak mixing angle from geometric parameters"
            },
            alpha_s_MZ: {
                name: "Strong Coupling α_s(MZ)",
                unit: "",
                gift_formula: "√2/12",
                gift_value: () => Math.sqrt(2) / 12,
                derivation: "Strong coupling constant from geometric structure"
            },
            lambda_H: {
                name: "Higgs Quartic Coupling λ_H",
                unit: "",
                gift_formula: "√17/32",
                gift_value: () => Math.sqrt(17) / 32,
                derivation: "Higgs quartic coupling from geometric parameters"
            },
            m_H: {
                name: "Higgs Mass m_H",
                unit: "GeV",
                gift_formula: "246.22 × √(2λ_H)",
                gift_value: () => 246.22 * Math.sqrt(2 * this.observables.lambda_H.gift_value()),
                derivation: "Higgs mass from geometric quartic coupling"
            },
            f_pi: {
                name: "Pion Decay Constant f_π",
                unit: "MeV",
                gift_formula: "48×e",
                gift_value: () => 48 * this.e,
                derivation: "Pion decay constant with geometric significance: f_π = 48×e"
            },
            Q_koide: {
                name: "Koide Relation Q",
                unit: "",
                gift_formula: "√5/6",
                gift_value: () => Math.sqrt(5) / 6,
                derivation: "Koide relation from geometric parameters"
            },
            theta13: {
                name: "Neutrino Mixing θ₁₃",
                unit: "°",
                gift_formula: "π/21 × 180/π",
                gift_value: () => Math.PI / 21 * 180 / Math.PI,
                derivation: "Neutrino mixing angle θ₁₃ from geometric structure"
            },
            theta23: {
                name: "Neutrino Mixing θ₂₃",
                unit: "°",
                gift_formula: "18×e",
                gift_value: () => 18 * this.e,
                derivation: "Neutrino mixing angle θ₂₃ from transcendental combination"
            },
            theta12: {
                name: "Neutrino Mixing θ₁₂",
                unit: "°",
                gift_formula: "15×√5",
                gift_value: () => 15 * Math.sqrt(5),
                derivation: "Neutrino mixing angle θ₁₂ from geometric parameters"
            },
            delta_CP: {
                name: "CP Violation δ_CP",
                unit: "°",
                gift_formula: "2π × (99/(114+38)) × 180/π",
                gift_value: () => 2 * Math.PI * (this.factor_99 / (this.factor_114 + this.factor_38)) * 180 / Math.PI,
                derivation: "CP violation phase from cohomological correction factors"
            },
            H0: {
                name: "Hubble Constant H₀",
                unit: "km/s/Mpc",
                gift_formula: "67.36 × (ζ(3)/ξ)^β₀",
                gift_value: () => 67.36 * Math.pow(this.zeta3 / this.xi, this.beta0),
                derivation: "Hubble constant resolution from geometric parameters"
            },
            Omega_DE: {
                name: "Dark Energy Ω_DE",
                unit: "",
                gift_formula: "ζ(3) × γ",
                gift_value: () => this.zeta3 * this.gamma,
                derivation: "Dark energy density from geometric constants"
            },
            n_s: {
                name: "Spectral Index n_s",
                unit: "",
                gift_formula: "ξ²",
                gift_value: () => this.xi * this.xi,
                derivation: "Spectral index from geometric parameter ξ"
            }
        };
    }
    
    calculatePrediction(observable_key, experimental_value = null) {
        if (!this.observables[observable_key]) {
            throw new Error(`Unknown observable: ${observable_key}`);
        }
        
        const observable = this.observables[observable_key];
        const gift_prediction = observable.gift_value();
        const experimental = experimental_value !== null ? experimental_value : this.experimental_data[observable_key];
        
        let deviation = null;
        if (experimental !== undefined && experimental !== 0) {
            deviation = Math.abs(gift_prediction - experimental) / experimental * 100;
        }
        
        return {
            name: observable.name,
            unit: observable.unit,
            gift_prediction: gift_prediction,
            experimental_value: experimental,
            deviation_percent: deviation,
            formula: observable.gift_formula,
            derivation: observable.derivation
        };
    }
    
    formatValue(value, unit) {
        if (value === null || value === undefined) return "N/A";
        
        if (unit === "°") {
            return value.toFixed(2) + "°";
        } else if (unit === "GeV") {
            return value.toFixed(3) + " GeV";
        } else if (unit === "MeV") {
            return value.toFixed(1) + " MeV";
        } else if (unit === "km/s/Mpc") {
            return value.toFixed(2) + " km/s/Mpc";
        } else {
            return value.toFixed(6);
        }
    }
    
    getDeviationClass(deviation) {
        if (deviation === null) return "excellent";
        if (deviation < 0.1) return "excellent";
        if (deviation < 1.0) return "good";
        return "poor";
    }
    
    getDeviationText(deviation) {
        if (deviation === null) return "N/A";
        return deviation.toFixed(4) + "%";
    }
}

// Global calculator instance
const calculator = new GIFTCalculator();

// UI Functions
function calculatePrediction() {
    const observableSelect = document.getElementById('observable-select');
    const experimentalInput = document.getElementById('experimental-value');
    const resultsDiv = document.getElementById('results');
    const formulaDisplay = document.getElementById('formula-display');
    const formulaContent = document.getElementById('formula-content');
    const statusMessage = document.getElementById('status-message');
    
    const selectedObservable = observableSelect.value;
    
    if (!selectedObservable) {
        showStatus('Please select an observable', 'error');
        return;
    }
    
    try {
        let experimentalValue = null;
        if (experimentalInput.value.trim() !== '') {
            experimentalValue = parseFloat(experimentalInput.value);
            if (isNaN(experimentalValue)) {
                showStatus('Invalid experimental value', 'error');
                return;
            }
        }
        
        const result = calculator.calculatePrediction(selectedObservable, experimentalValue);
        
        // Update results display
        resultsDiv.innerHTML = `
            <div class="result-item">
                <span class="result-label">GIFT Prediction:</span>
                <span class="result-value">${calculator.formatValue(result.gift_prediction, result.unit)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Experimental Value:</span>
                <span class="result-value">${calculator.formatValue(result.experimental_value, result.unit)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Deviation:</span>
                <span class="result-value">
                    <span class="deviation ${calculator.getDeviationClass(result.deviation_percent)}">
                        ${calculator.getDeviationText(result.deviation_percent)}
                    </span>
                </span>
            </div>
        `;
        
        // Update formula display
        formulaContent.textContent = `${result.formula}\n\nDerivation: ${result.derivation}`;
        formulaDisplay.style.display = 'block';
        
        showStatus('Calculation completed successfully', 'success');
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function showStatus(message, type) {
    const statusDiv = document.getElementById('status-message');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
    statusDiv.style.display = 'block';
    
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 3000);
}

// Auto-populate experimental value when observable is selected
document.getElementById('observable-select').addEventListener('change', function() {
    const selectedObservable = this.value;
    const experimentalInput = document.getElementById('experimental-value');
    
    if (selectedObservable && calculator.experimental_data[selectedObservable] !== undefined) {
        experimentalInput.value = calculator.experimental_data[selectedObservable];
        experimentalInput.placeholder = `Default: ${calculator.experimental_data[selectedObservable]}`;
    } else {
        experimentalInput.value = '';
        experimentalInput.placeholder = 'Enter experimental value for comparison';
    }
});

// Calculate on Enter key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        calculatePrediction();
    }
});

// Initialize with first observable info
document.addEventListener('DOMContentLoaded', function() {
    // Add some initial help text
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="result-item">
            <span class="result-label">Instructions:</span>
            <span class="result-value">Select an observable and click Calculate</span>
        </div>
    `;
});
