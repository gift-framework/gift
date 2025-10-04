// GIFT ↔ Standard Model Translator Engine
// Based on the technical supplement derivations

class GIFTTranslator {
    constructor() {
        this.translationRules = {
            // Standard Model to GIFT conversions
            smToGift: {
                // Electromagnetic coupling conversions
                coupling: {
                    '1/4': 'ζ(3) × 114',  // α⁻¹ = ζ(3) × 114
                    '-(1/4)': '-(ζ(3) × 114)',
                    '1/(4π)': '1/(4π × ζ(3) × 114)',
                    'e²/(4π)': 'ζ(3) × 114/(4π)'
                },
                
                // Weak mixing angle
                weakMixing: {
                    'sin²θ_W': 'ζ(2) - √2',
                    'cos²θ_W': '1 - (ζ(2) - √2)',
                    'tan²θ_W': '(ζ(2) - √2)/(1 - (ζ(2) - √2))'
                },
                
                // Strong coupling
                strongCoupling: {
                    'α_s': '√2/12',
                    'g_s': '√(4π × √2/12)'
                },
                
                // Geometric parameters
                geometricParams: {
                    'ξ': '5π/16',
                    'τ': '8γ^(5π/12)',
                    'β₀': 'π/8',
                    'δ': '2π/25'
                },
                
                // Correction factors
                corrections: {
                    'F_α': '98.999',
                    'F_β': '99.734',
                    'k': '26.464068'
                }
            },
            
            // GIFT to Standard Model conversions
            giftToSm: {
                // Reverse mappings
                'ζ(3) × 114': '1/4',
                'ζ(2) - √2': 'sin²θ_W',
                '√2/12': 'α_s',
                '5π/16': 'ξ',
                '8γ^(5π/12)': 'τ',
                'π/8': 'β₀',
                '2π/25': 'δ',
                '98.999': 'F_α',
                '99.734': 'F_β',
                '26.464068': 'k'
            }
        };
        
        this.examples = {
            maxwell: {
                sm: '-(1/4) F_μν F^μν - A_μ J^μ',
                gift: '-(ζ(3) × 114) F_μν F^μν - A_μ J^μ'
            },
            qcd: {
                sm: '-(1/4) F^a_μν F^{aμν} + ψ̄(iγ^μ D_μ - m)ψ',
                gift: '-(√2/12) F^a_μν F^{aμν} + ψ̄(iγ^μ D_μ - m)ψ'
            },
            electroweak: {
                sm: '-(1/4) W^i_μν W^{iμν} - (1/4) B_μν B^μν + |D_μ Φ|² - V(Φ)',
                gift: '-(ζ(3) × 114) W^i_μν W^{iμν} - (ζ(3) × 114) B_μν B^μν + |D_μ Φ|² - V(Φ)'
            },
            higgs: {
                sm: '|D_μ H|² - μ²|H|² - λ|H|⁴',
                gift: '|D_μ H|² - μ²|H|² - (√17/32)|H|⁴'
            },
            yukawa: {
                sm: '-Y_u ū_L H u_R - Y_d d̄_L H* d_R - Y_e ē_L H* e_R + h.c.',
                gift: '-(8γ^(5π/12)) ū_L H u_R - (8γ^(5π/12)) d̄_L H* d_R - (8γ^(5π/12)) ē_L H* e_R + h.c.'
            },
            kinetic: {
                sm: 'iψ̄_L γ^μ D_μ ψ_L + iψ̄_R γ^μ D_μ ψ_R',
                gift: 'iψ̄_L γ^μ D_μ ψ_L + iψ̄_R γ^μ D_μ ψ_R'
            },
            dirac: {
                sm: 'ψ̄(iγ^μ ∂_μ - m)ψ',
                gift: 'ψ̄(iγ^μ ∂_μ - m)ψ'
            },
            yang_mills: {
                sm: '-(1/4) F^A_μν F^{Aμν} + ψ̄(iγ^μ D_μ - m)ψ',
                gift: '-(ζ(3) × 114) F^A_μν F^{Aμν} + ψ̄(iγ^μ D_μ - m)ψ'
            },
            scalar: {
                sm: '(1/2) ∂_μ φ ∂^μ φ - (1/2) m² φ² - (λ/4!) φ⁴',
                gift: '(1/2) ∂_μ φ ∂^μ φ - (1/2) m² φ² - (ζ(3) × 114/4!) φ⁴'
            },
            proca: {
                sm: '-(1/4) F_μν F^μν + (1/2) m² A_μ A^μ',
                gift: '-(ζ(3) × 114) F_μν F^μν + (1/2) m² A_μ A^μ'
            }
        };
    }
    
    // Main translation function
    translate(formula, mode) {
        try {
            if (mode === 'sm-to-gift') {
                return this.smToGift(formula);
            } else {
                return this.giftToSm(formula);
            }
        } catch (error) {
            throw new Error(`Translation error: ${error.message}`);
        }
    }
    
    // Standard Model to GIFT conversion
    smToGift(formula) {
        let result = formula;
        
        // Apply exact coupling conversions first
        for (const [sm, gift] of Object.entries(this.translationRules.smToGift.coupling)) {
            result = result.replace(new RegExp(sm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), gift);
        }
        
        // Apply weak mixing angle conversions
        for (const [sm, gift] of Object.entries(this.translationRules.smToGift.weakMixing)) {
            result = result.replace(new RegExp(sm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), gift);
        }
        
        // Apply strong coupling conversions
        for (const [sm, gift] of Object.entries(this.translationRules.smToGift.strongCoupling)) {
            result = result.replace(new RegExp(sm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), gift);
        }
        
        // Smart fraction conversion: convert any fraction to GIFT form
        result = this.convertFractionsToGIFT(result);
        
        // Convert numerical coefficients to GIFT parameters
        result = this.convertCoefficientsToGIFT(result);
        
        // Add geometric correction terms for complex Lagrangians
        if (result.includes('F_μν') || result.includes('F^a_μν')) {
            result = this.addGeometricCorrections(result, 'sm-to-gift');
        }
        
        return result;
    }
    
    // Convert fractions to GIFT geometric form
    convertFractionsToGIFT(formula) {
        let result = formula;
        
        // Match fractions like -(2/4), (3/8), etc.
        const fractionPattern = /(-?\s*)?\(?(\d+)\/(\d+)\)?/g;
        
        result = result.replace(fractionPattern, (match, sign, numerator, denominator) => {
            const num = parseInt(numerator);
            const den = parseInt(denominator);
            const value = num / den;
            
            // Convert to GIFT geometric equivalent
            if (denominator === '4') {
                // Any /4 fraction becomes ζ(3) × 114 scaled by the coefficient
                const coefficient = num;
                return `${sign || ''}(ζ(3) × 114 × ${coefficient}/4)`;
            } else if (denominator === '12') {
                // Any /12 fraction becomes √2/12 scaled
                const coefficient = num;
                return `${sign || ''}(√2/12 × ${coefficient})`;
            } else if (denominator === '8') {
                // Any /8 fraction becomes π/8 scaled
                const coefficient = num;
                return `${sign || ''}(π/8 × ${coefficient})`;
            } else {
                // For other fractions, show the geometric interpretation
                return `${sign || ''}(ζ(3) × 114 × ${value})`;
            }
        });
        
        return result;
    }
    
    // Convert numerical coefficients to GIFT parameters
    convertCoefficientsToGIFT(formula) {
        let result = formula;
        
        // Match standalone numbers that could be coupling constants
        const numberPattern = /\b(\d+\.?\d*)\b/g;
        
        result = result.replace(numberPattern, (match, number) => {
            const num = parseFloat(number);
            
            // Skip very large numbers (likely masses, energies)
            if (num > 1000) return match;
            
            // Convert specific coupling-like numbers
            if (Math.abs(num - 0.1179) < 0.01) {
                return '√2/12'; // α_s equivalent
            } else if (Math.abs(num - 0.2307) < 0.01) {
                return 'ζ(2) - √2'; // sin²θ_W equivalent
            } else if (Math.abs(num - 0.25) < 0.01) {
                return 'ζ(3) × 114/4'; // 1/4 equivalent
            } else if (Math.abs(num - 0.5) < 0.01) {
                return 'ζ(3) × 114/2'; // 1/2 equivalent
            } else if (Math.abs(num - 1.0) < 0.01) {
                return 'ζ(3) × 114/4'; // 1 equivalent (scaled)
            }
            
            return match; // Keep original if no conversion found
        });
        
        return result;
    }
    
    // GIFT to Standard Model conversion
    giftToSm(formula) {
        let result = formula;
        
        // Apply reverse conversions
        for (const [gift, sm] of Object.entries(this.translationRules.giftToSm)) {
            result = result.replace(new RegExp(gift.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), sm);
        }
        
        // Remove geometric correction terms
        if (result.includes('F_α') || result.includes('F_β')) {
            result = this.removeGeometricCorrections(result);
        }
        
        return result;
    }
    
    // Add geometric corrections to Lagrangian
    addGeometricCorrections(formula, mode) {
        let result = formula;
        
        // Add correction terms based on Lagrangian type
        if (formula.includes('F_μν F^μν')) {
            // Electromagnetic corrections
            result += ' + ℒ_geometric_EM';
            result += '\n// Where: ℒ_geometric_EM = (F_α/Λ²) F_μν F^μν [EM coupling enhancement]';
        }
        
        if (formula.includes('ψ̄_L') && formula.includes('ψ_R')) {
            // Fermion corrections
            result += ' + ℒ_geometric_fermion';
            result += '\n// Where: ℒ_geometric_fermion = (1/F_α) (ψ̄ψ)² [Fermion density suppression]';
        }
        
        if (formula.includes('Φ') || formula.includes('H')) {
            // Scalar corrections
            result += ' + ℒ_geometric_scalar';
            result += '\n// Where: ℒ_geometric_scalar = (F_β/v²) |H|² (∂φ)² [Scalar mixing]';
        }
        
        return result;
    }
    
    // Remove geometric corrections
    removeGeometricCorrections(formula) {
        let result = formula;
        
        // Remove correction terms
        result = result.replace(/\s*\+\s*ℒ_geometric_[^\n]*/g, '');
        result = result.replace(/\/\/ Where: ℒ_geometric_[^\n]*\n?/g, '');
        
        return result.trim();
    }
    
    // Get example formula
    getExample(exampleName, mode) {
        if (this.examples[exampleName]) {
            return mode === 'sm-to-gift' ? 
                this.examples[exampleName].sm : 
                this.examples[exampleName].gift;
        }
        return '';
    }
}

// Global translator instance
const translator = new GIFTTranslator();

// UI Functions
function updateHeaders(mode) {
    const inputHeader = document.getElementById('inputHeader');
    const outputHeader = document.getElementById('outputHeader');
    
    if (mode === 'sm-to-gift') {
        inputHeader.textContent = 'Standard Model Lagrangian';
        outputHeader.textContent = 'GIFT Geometric Form';
    } else {
        inputHeader.textContent = 'GIFT Geometric Form';
        outputHeader.textContent = 'Standard Model Lagrangian';
    }
}

function translateFormula() {
    const inputFormula = document.getElementById('inputFormula').value.trim();
    const mode = document.getElementById('translationMode').value;
    const outputFormula = document.getElementById('outputFormula');
    const status = document.getElementById('status');
    
    if (!inputFormula) {
        showStatus('Please enter a formula to translate', 'error');
        return;
    }
    
    try {
        const result = translator.translate(inputFormula, mode);
        outputFormula.value = result;
        showStatus('Translation completed successfully!', 'success');
    } catch (error) {
        showStatus(`Translation failed: ${error.message}`, 'error');
        outputFormula.value = '';
    }
}

function swapTranslation() {
    const modeSelect = document.getElementById('translationMode');
    const inputFormula = document.getElementById('inputFormula');
    const outputFormula = document.getElementById('outputFormula');
    
    // Swap the mode
    modeSelect.value = modeSelect.value === 'sm-to-gift' ? 'gift-to-sm' : 'sm-to-gift';
    
    // Swap the formulas
    const temp = inputFormula.value;
    inputFormula.value = outputFormula.value;
    outputFormula.value = temp;
    
    // Update headers
    updateHeaders(modeSelect.value);
    
    showStatus('Translation mode swapped!', 'info');
}

function loadExample(exampleName) {
    const mode = document.getElementById('translationMode').value;
    const inputFormula = document.getElementById('inputFormula');
    
    const example = translator.getExample(exampleName, mode);
    if (example) {
        inputFormula.value = example;
        showStatus(`Loaded ${exampleName} example`, 'info');
    }
}

function showStatus(message, type) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status ${type}`;
    status.style.display = 'block';
    
    setTimeout(() => {
        status.style.display = 'none';
    }, 3000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const modeSelect = document.getElementById('translationMode');
    
    modeSelect.addEventListener('change', function() {
        updateHeaders(this.value);
    });
    
    // Initialize headers
    updateHeaders(modeSelect.value);
    
    // Add keyboard shortcut for translation (Ctrl+Enter)
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            translateFormula();
        }
    });
});

// Advanced translation features
function addGeometricParameter() {
    const inputFormula = document.getElementById('inputFormula');
    const params = ['ξ = 5π/16', 'τ = 8γ^(5π/12)', 'β₀ = π/8', 'δ = 2π/25'];
    const param = params[Math.floor(Math.random() * params.length)];
    
    if (inputFormula.value.trim()) {
        inputFormula.value += '\n' + param;
    } else {
        inputFormula.value = param;
    }
    
    showStatus(`Added geometric parameter: ${param}`, 'info');
}

function addCorrectionFactor() {
    const inputFormula = document.getElementById('inputFormula');
    const corrections = ['F_α ≈ 98.999', 'F_β ≈ 99.734', 'k ≈ 26.464068'];
    const correction = corrections[Math.floor(Math.random() * corrections.length)];
    
    if (inputFormula.value.trim()) {
        inputFormula.value += '\n' + correction;
    } else {
        inputFormula.value = correction;
    }
    
    showStatus(`Added correction factor: ${correction}`, 'info');
}
