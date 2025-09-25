#!/usr/bin/env python3
"""
GIFT Translator Demo - Examples of bidirectional translation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gift_translator import GIFTTranslator

def main():
    print("🔬 GIFT Translator Demo")
    print("=" * 60)
    print("Bidirectional translation between Standard Model and GIFT formalism")
    print()
    
    translator = GIFTTranslator()
    
    # Test expressions
    test_expressions = [
        # Famous equations
        ("E = mc²", "SM", "GIFT", "Einstein mass-energy relation"),
        ("α = e²/(4πε₀ℏc)", "SM", "GIFT", "Fine structure constant"),
        ("sin²θ_W = g'²/(g² + g'²)", "SM", "GIFT", "Weinberg angle"),
        
        # GIFT expressions
        ("ξ = 5π/16", "GIFT", "SM", "GIFT geometric parameter ξ"),
        ("α⁻¹ = ζ₃ × 114 - 1/24", "GIFT", "SM", "GIFT fine structure prediction"),
        ("sin²θ_W = ζ₂ - √2", "GIFT", "SM", "GIFT Weinberg angle prediction"),
        
        # Physical quantities
        ("α", "SM", "GIFT", "Fine structure constant symbol"),
        ("Λ_QCD", "SM", "GIFT", "QCD scale parameter"),
        ("H₀", "SM", "GIFT", "Hubble constant"),
        
        # Mathematical expressions
        ("π²/6", "SM", "GIFT", "Basel constant"),
        ("ζ₃", "GIFT", "SM", "Apéry's constant in GIFT"),
    ]
    
    print("🧪 Translation Examples:")
    print("-" * 60)
    
    for i, (expression, from_format, to_format, description) in enumerate(test_expressions, 1):
        print(f"\n{i}. {description}")
        print(f"   {from_format} → {to_format}")
        print(f"   Input: {expression}")
        
        result = translator.translate(expression, from_format, to_format)
        
        if result['success']:
            print(f"   ✅ Output: {result['translated']}")
            print(f"   📝 Explanation: {result['explanation']}")
            print(f"   🎯 Confidence: {result['confidence']:.1%}")
            
            if result.get('warnings'):
                for warning in result['warnings']:
                    print(f"   ⚠️  Warning: {warning}")
        else:
            print(f"   ❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("🎮 Interactive Demo")
    print("=" * 60)
    
    # Interactive mode
    print("\nEnter expressions to translate (or 'quit' to exit):")
    print("Format: <expression> <from> <to>")
    print("Examples:")
    print("  E = mc² SM GIFT")
    print("  ξ = 5π/16 GIFT SM")
    print("  α SM GIFT")
    print()
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            parts = user_input.split()
            if len(parts) < 3:
                print("❌ Format: <expression> <from> <to>")
                continue
            
            expression = ' '.join(parts[:-2])
            from_format = parts[-2].upper()
            to_format = parts[-1].upper()
            
            if from_format not in ['SM', 'GIFT'] or to_format not in ['SM', 'GIFT']:
                print("❌ Formats must be 'SM' or 'GIFT'")
                continue
            
            result = translator.translate(expression, from_format, to_format)
            
            if result['success']:
                print(f"✅ {result['translated']}")
                print(f"📝 {result['explanation']}")
                print(f"🎯 Confidence: {result['confidence']:.1%}")
            else:
                print(f"❌ {result['error']}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
