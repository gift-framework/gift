"""
Web interface for GIFT Translator (Flask-based)
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from .core import GIFTTranslator, TranslationError

# Get the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(os.path.dirname(current_dir), 'templates')

app = Flask(__name__, template_folder=templates_dir)
translator = GIFTTranslator()

@app.route('/')
def index():
    """Main translation interface"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """Handle translation requests"""
    try:
        data = request.get_json()
        
        expression = data.get('expression', '').strip()
        from_format = data.get('from_format', 'SM')
        to_format = data.get('to_format', 'GIFT')
        
        if not expression:
            return jsonify({
                'success': False,
                'error': 'No expression provided'
            })
        
        # Perform translation
        result = translator.translate(expression, from_format, to_format)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/examples')
def examples():
    """Get example expressions"""
    examples = {
        'equations': [
            'E = mc²',
            'α = e²/(4πε₀ℏc)',
            'sin²θ_W = g\'²/(g² + g\'²)',
            'Q = (√m_e + √m_μ + √m_τ)²/(m_e + m_μ + m_τ)',
            'H₀ = 100h km/s/Mpc'
        ],
        'quantities': [
            'α',
            'α_s',
            'θ_W',
            'Λ_QCD',
            'm_H',
            'H₀'
        ],
        'gift_expressions': [
            'ξ = 5π/16',
            'τ = 8·γ^(5π/12)',
            'α⁻¹ = ζ₃ × 114 - 1/24',
            'sin²θ_W = ζ₂ - √2',
            'H₀ = 67.36 × (ζ₃/ξ)^β₀'
        ]
    }
    return jsonify(examples)

@app.route('/info')
def info():
    """Get translation information"""
    info = {
        'available_translations': translator.get_available_translations(),
        'supported_formats': ['SM', 'GIFT'],
        'confidence_levels': {
            'high': '0.9-1.0 (Known equations, exact conversions)',
            'medium': '0.7-0.9 (Physical quantities, mathematical expressions)',
            'low': '0.3-0.7 (Generic symbolic translation)'
        },
        'limitations': [
            'Some translations may not preserve exact physical meaning',
            'Complex mathematical expressions may require manual verification',
            'GIFT formalism is based on geometric principles and may differ from SM'
        ]
    }
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
