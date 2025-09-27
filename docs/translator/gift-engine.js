/**
 * GIFT Translation Engine
 * ======================
 * 
 * Advanced translation engine based on GIFT framework derivations
 * from the core notebook and scientific papers.
 */

class GIFTEngine {
    constructor() {
        // GIFT geometric parameters from E₈×E₈ dimensional reduction
        this.constants = {
            xi: 5 * Math.PI / 16,                    // ξ = 0.981748... (projection efficiency)
            tau: 8 * Math.pow(0.5772156649, 5 * Math.PI / 12), // τ = 3.896568... (mass hierarchy)
            beta_0: Math.PI / 8,                     // β₀ = 0.392699... (dimensional anomaly)
            delta: 2 * Math.PI / 25,                 // δ = 0.251327... (Koide correction)
            zeta_2: Math.PI * Math.PI / 6,           // ζ₂ = 1.644934... (Basel constant)
            zeta_3: 1.2020569031595942,              // ζ₃ = 1.202057... (Apéry's constant)
            gamma: 0.5772156649,                     // γ = 0.577216... (Euler-Mascheroni)
            phi: (1 + Math.sqrt(5)) / 2,             // φ = 1.618034... (Golden ratio)
            k: 27 - 0.5772156649 + 1/24,             // k = 26.465... (family factor)
            F_alpha: 99 - 0.001,                     // F_α ≈ 98.999 (single-sector correction)
            F_beta: 99 + 0.735                       // F_β ≈ 99.734 (multi-sector correction)
        };
        
        // Physical constants
        this.physical = {
            c: 299792458,                            // Speed of light (m/s)
            hbar: 1.054571817e-34,                   // Reduced Planck constant (J⋅s)
            e: 1.602176634e-19,                      // Elementary charge (C)
            epsilon_0: 8.8541878128e-12,             // Vacuum permittivity (F/m)
            mu_0: 4 * Math.PI * 1e-7,                // Vacuum permeability (H/m)
            G: 6.67430e-11,                          // Gravitational constant (m³/kg/s²)
            m_e: 9.1093837015e-31,                   // Electron mass (kg)
            m_p: 1.67262192369e-27,                  // Proton mass (kg)
            alpha_0: 1/137.035999139,                // Fine structure constant (experimental)
            M_Z: 91.1876e9,                          // Z boson mass (eV)
            M_W: 80.379e9                            // W boson mass (eV)
        };
        
        // Unit conversions
        this.units = {
            eV_to_J: 1.602176634e-19,
            MeV_to_J: 1.602176634e-13,
            GeV_to_J: 1.602176634e-10,
            km_s_Mpc_to_s: 3.240779289e-20
        };
        
        // Initialize equation patterns
        this.initializeEquationPatterns();
    }
    
    initializeEquationPatterns() {
        this.equationPatterns = {
            // Electromagnetic sector
            'fine_structure': {
                patterns: [
                    /α\s*=\s*e\^?2\s*\/\s*\(4π\s*ε₀\s*ℏ\s*c\)/i,
                    /α\s*=\s*e\^?2\s*\/\s*\(4π\s*ε_?0\s*ℏ\s*c\)/i
                ],
                sm: () => 'α = e²/(4πε₀ℏc)',
                gift: () => {
                    const alpha_inv = this.constants.zeta_3 * 114;
                    const alpha = 1 / alpha_inv;
                    return `α⁻¹ = ${alpha_inv.toFixed(6)} (GIFT: α⁻¹ = ζ₃ × 114)`;
                },
                derivation: 'GIFT derives α⁻¹ from geometric reduction: α⁻¹ = ζ₃ × 114, where ζ₃ = 1.202... (Apéry\'s constant)'
            },
            
            // Electroweak sector
            'weinberg_angle': {
                patterns: [
                    /sin\^?2\s*θ_?W\s*=\s*g'?\^?2\s*\/\s*\(g\^?2\s*\+\s*g'?\^?2\)/i,
                    /sin\^?2\s*θ_?w\s*=\s*g'?\^?2\s*\/\s*\(g\^?2\s*\+\s*g'?\^?2\)/i
                ],
                sm: () => 'sin²θ_W = g\'²/(g² + g\'²)',
                gift: () => {
                    const sin2_theta_W = this.constants.zeta_2 - Math.sqrt(2);
                    return `sin²θ_W = ${sin2_theta_W.toFixed(6)} (GIFT: sin²θ_W = ζ₂ - √2)`;
                },
                derivation: 'GIFT derives Weinberg angle from geometric constraint: sin²θ_W = ζ₂ - √2, where ζ₂ = π²/6'
            },
            
            // Mass-energy relation
            'einstein': {
                patterns: [
                    /E\s*=\s*mc\^?2/i,
                    /E\s*=\s*m\s*c\^?2/i
                ],
                sm: (m = 1) => `E = ${m}c²`,
                gift: (m = 1) => {
                    const correction = this.constants.xi * this.constants.tau;
                    const E_gift = m * correction * Math.pow(this.physical.c, 2);
                    return `E = ${m} × ξ×τ × c² = ${E_gift.toExponential(3)} J (GIFT geometric correction)`;
                },
                derivation: 'GIFT adds geometric corrections: E = ξ×τ × mc², where ξ = 5π/16, τ = 8γ^(5π/12)'
            },
            
            // Strong sector
            'strong_coupling': {
                patterns: [
                    /α_?s\s*=\s*√2\s*\/\s*12/i,
                    /α_?s\s*=\s*sqrt\(2\)\s*\/\s*12/i
                ],
                sm: () => 'α_s = √2/12',
                gift: () => {
                    const alpha_s = Math.sqrt(2) / 12;
                    return `α_s(M_Z) = ${alpha_s.toFixed(6)} (GIFT: α_s = √2/12)`;
                },
                derivation: 'GIFT derives strong coupling from geometric constraint: α_s = √2/12'
            },
            
            // Cosmological sector
            'hubble_constant': {
                patterns: [
                    /H_?0\s*=\s*67\.36\s*×\s*\(ζ₃\/ξ\)\^β₀/i,
                    /H_?0\s*=\s*67\.36\s*\*\s*\(ζ₃\/ξ\)\^β₀/i
                ],
                gift: () => {
                    const H0 = 67.36 * Math.pow(this.constants.zeta_3 / this.constants.xi, this.constants.beta_0);
                    return `H₀ = ${H0.toFixed(2)} km/s/Mpc (GIFT: H₀ = 67.36 × (ζ₃/ξ)^β₀)`;
                },
                sm: () => 'H₀ = 67.36 × (ζ₃/ξ)^β₀ km/s/Mpc',
                derivation: 'GIFT resolves Hubble tension: H₀ = 67.36 × (ζ₃/ξ)^β₀, giving 72.93 km/s/Mpc'
            },
            
            // QCD scale
            'qcd_scale': {
                patterns: [
                    /Λ_?QCD\s*=\s*k\s*×\s*8\.38/i,
                    /Lambda_?QCD\s*=\s*k\s*\*\s*8\.38/i
                ],
                sm: () => 'Λ_QCD = k × 8.38 MeV',
                gift: () => {
                    const Lambda_QCD = this.constants.k * 8.38;
                    return `Λ_QCD = ${Lambda_QCD.toFixed(2)} MeV (GIFT: Λ_QCD = k × 8.38)`;
                },
                derivation: 'GIFT derives QCD scale from family factor: Λ_QCD = k × 8.38 MeV, where k = 26.465...'
            },
            
            // Pion decay constant
            'pion_decay': {
                patterns: [
                    /f_?π\s*=\s*48\s*×\s*e/i,
                    /f_?pi\s*=\s*48\s*\*\s*e/i
                ],
                sm: () => 'f_π = 48 × e MeV',
                gift: () => {
                    const f_pi = 48 * Math.E;
                    return `f_π = ${f_pi.toFixed(2)} MeV (GIFT: f_π = 48 × e)`;
                },
                derivation: 'GIFT derives pion decay constant from geometric factor: f_π = 48 × e MeV'
            }
        };
    }
    
    /**
     * Main translation method
     */
    translate(expression, fromFormat, toFormat) {
        try {
            const cleanExpr = expression.trim();
            
            // Try equation pattern matching first
            const patternResult = this.matchEquationPatterns(cleanExpr, fromFormat, toFormat);
            if (patternResult.success) {
                return patternResult;
            }
            
            // Try mathematical expression evaluation
            const mathResult = this.evaluateMathematicalExpression(cleanExpr, fromFormat, toFormat);
            if (mathResult.success) {
                return mathResult;
            }
            
            // Fallback to symbolic translation
            return this.symbolicTranslation(cleanExpr, fromFormat, toFormat);
            
        } catch (error) {
            return {
                success: false,
                error: error.message,
                confidence: 0.0
            };
        }
    }
    
    /**
     * Match against known equation patterns
     */
    matchEquationPatterns(expression, fromFormat, toFormat) {
        for (let [name, patternData] of Object.entries(this.equationPatterns)) {
            for (let pattern of patternData.patterns) {
                if (pattern.test(expression)) {
                    let result;
                    
                    if (fromFormat === 'SM' && toFormat === 'GIFT' && patternData.gift) {
                        result = typeof patternData.gift === 'function' ? patternData.gift() : patternData.gift;
                    } else if (fromFormat === 'GIFT' && toFormat === 'SM' && patternData.sm) {
                        result = typeof patternData.sm === 'function' ? patternData.sm() : patternData.sm;
                    } else {
                        continue;
                    }
                    
                    return {
                        success: true,
                        translated: result,
                        explanation: patternData.derivation || 'Known equation pattern',
                        confidence: 0.95,
                        method: 'pattern_matching',
                        equation_type: name
                    };
                }
            }
        }
        
        return { success: false };
    }
    
    /**
     * Evaluate mathematical expressions with GIFT constants
     */
    evaluateMathematicalExpression(expression, fromFormat, toFormat) {
        try {
            let result = expression;
            let hasCalculations = false;
            let calculatedValue = null;
            
            // Replace GIFT constants with their values
            const constantMap = {
                'ξ': this.constants.xi,
                'τ': this.constants.tau,
                'β₀': this.constants.beta_0,
                'δ': this.constants.delta,
                'ζ₂': this.constants.zeta_2,
                'ζ₃': this.constants.zeta_3,
                'γ': this.constants.gamma,
                'φ': this.constants.phi,
                'k': this.constants.k,
                'F_α': this.constants.F_alpha,
                'F_β': this.constants.F_beta
            };
            
            // Check if expression contains GIFT constants
            let containsConstants = false;
            for (let [symbol, value] of Object.entries(constantMap)) {
                if (expression.includes(symbol)) {
                    containsConstants = true;
                    if (toFormat === 'SM') {
                        result = result.replace(new RegExp(symbol, 'g'), `(${value.toFixed(6)})`);
                    }
                }
            }
            
            // Don't modify pure numerical expressions without GIFT constants
            if (!containsConstants && /^[A-Za-z_]*\s*=\s*[\d\.\s\+\-\*\/\^\(\)]+$/.test(expression.trim())) {
                return {
                    success: true,
                    translated: expression,
                    explanation: 'Numerical expression without GIFT constants',
                    confidence: 0.5,
                    method: 'no_translation_needed'
                };
            }
            
            // Try to evaluate mathematical expressions
            if (containsConstants || /[+\-*/^()]/.test(expression)) {
                try {
                    let evalExpr = result
                        .replace(/π/g, 'Math.PI')
                        .replace(/√/g, 'Math.sqrt')
                        .replace(/\^/g, '**')
                        .replace(/×/g, '*')
                        .replace(/÷/g, '/')
                        .replace(/e(?![0-9])/g, 'Math.E');
                    
                    // Remove units for calculation
                    evalExpr = evalExpr.replace(/\s*(km\/s\/Mpc|MeV|GeV|eV|J|m|s|kg)/g, '');
                    
                    // Safe evaluation
                    calculatedValue = this.safeEval(evalExpr);
                    
                    if (typeof calculatedValue === 'number' && !isNaN(calculatedValue)) {
                        hasCalculations = true;
                        result += ` = ${calculatedValue.toFixed(6)}`;
                    }
                } catch (evalError) {
                    // If evaluation fails, keep symbolic form
                }
            }
            
            return {
                success: true,
                translated: result,
                explanation: hasCalculations ? 'Mathematical expression with calculated values' : 'Symbolic translation with GIFT constants',
                confidence: hasCalculations ? 0.85 : 0.7,
                method: hasCalculations ? 'mathematical_evaluation' : 'symbolic_replacement',
                calculated_value: calculatedValue
            };
            
        } catch (error) {
            return {
                success: false,
                error: `Mathematical evaluation error: ${error.message}`
            };
        }
    }
    
    /**
     * Safe mathematical evaluation
     */
    safeEval(expression) {
        // Remove dangerous functions and only allow safe mathematical operations
        const sanitized = expression.replace(/[^0-9+\-*/().\sMath.PIe]/g, '');
        
        // Create a safe evaluation context
        const context = {
            Math: Math,
            PI: Math.PI,
            E: Math.E
        };
        
        // Use Function constructor for safer evaluation than eval()
        const func = new Function('Math', 'PI', 'E', `return ${sanitized}`);
        return func(context.Math, context.PI, context.E);
    }
    
    /**
     * Symbolic translation between SM and GIFT
     */
    symbolicTranslation(expression, fromFormat, toFormat) {
        let result = expression;
        
        const symbolMap = {
            'α': 'α_gift',
            'α_s': 'α_s_gift',
            'θ_W': 'θ_W_gift',
            'Λ_QCD': 'Λ_QCD_gift',
            'm_H': 'm_H_gift',
            'H₀': 'H_0_gift',
            'H_0': 'H_0_gift',
            'Ω_Λ': 'Ω_DE_gift',
            'Ω_m': 'Ω_m_gift',
            'f_π': 'f_π_gift',
            'G_F': 'G_F_gift',
            'η_B': 'η_B_gift'
        };
        
        const reverseMap = {};
        for (let [sm, gift] of Object.entries(symbolMap)) {
            reverseMap[gift] = sm;
        }
        
        if (fromFormat === 'SM' && toFormat === 'GIFT') {
            for (let [sm, gift] of Object.entries(symbolMap)) {
                result = result.replace(new RegExp(sm, 'g'), gift);
            }
        } else if (fromFormat === 'GIFT' && toFormat === 'SM') {
            for (let [gift, sm] of Object.entries(reverseMap)) {
                result = result.replace(new RegExp(gift, 'g'), sm);
            }
        }
        
        return {
            success: true,
            translated: result,
            explanation: 'Symbolic translation using GIFT formalism',
            confidence: 0.6,
            method: 'symbolic_replacement'
        };
    }
    
    /**
     * Get available GIFT constants and their values
     */
    getConstants() {
        return {
            geometric: {
                xi: { value: this.constants.xi, description: 'Projection efficiency (5π/16)' },
                tau: { value: this.constants.tau, description: 'Mass hierarchy generator' },
                beta_0: { value: this.constants.beta_0, description: 'Dimensional anomaly parameter' },
                delta: { value: this.constants.delta, description: 'Koide relation parameter' }
            },
            mathematical: {
                zeta_2: { value: this.constants.zeta_2, description: 'Basel constant (π²/6)' },
                zeta_3: { value: this.constants.zeta_3, description: 'Apéry\'s constant' },
                gamma: { value: this.constants.gamma, description: 'Euler-Mascheroni constant' },
                phi: { value: this.constants.phi, description: 'Golden ratio' }
            },
            derived: {
                k: { value: this.constants.k, description: 'Family factor' },
                F_alpha: { value: this.constants.F_alpha, description: 'Single-sector correction' },
                F_beta: { value: this.constants.F_beta, description: 'Multi-sector correction' }
            }
        };
    }
    
    /**
     * Get equation patterns and their derivations
     */
    getEquationPatterns() {
        const patterns = {};
        for (let [name, data] of Object.entries(this.equationPatterns)) {
            patterns[name] = {
                sm: data.sm,
                gift: data.gift,
                derivation: data.derivation
            };
        }
        return patterns;
    }
}
