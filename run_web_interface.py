#!/usr/bin/env python3
"""
Simple script to run the GIFT Translator web interface
"""

import os
import sys
from flask import Flask, render_template_string, request, jsonify

# Add current directory to path
sys.path.insert(0, '.')

# Read the HTML template
template_path = os.path.join('templates', 'index.html')
with open(template_path, 'r', encoding='utf-8') as f:
    html_template = f.read()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/translate', methods=['POST'])
def translate():
    """Handle translation requests"""
    try:
        from gift_translator import GIFTTranslator
        
        data = request.get_json()
        expression = data.get('expression', '').strip()
        from_format = data.get('from_format', 'SM')
        to_format = data.get('to_format', 'GIFT')
        
        if not expression:
            return {'success': False, 'error': 'No expression provided'}
        
        translator = GIFTTranslator()
        result = translator.translate(expression, from_format, to_format)
        
        return result
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

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
    return examples

if __name__ == '__main__':
    print("🔬 GIFT.TRANSLATOR.EXE - MATRIX MODE")
    print("=" * 50)
    print("Starting web server...")
    print("Open: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
