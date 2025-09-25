"""
Command-line interface for GIFT Translator
"""

import argparse
import sys
from .core import GIFTTranslator

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="GIFT Translator - Bidirectional translation between SM and GIFT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gift-translate "E = mc²" --from SM --to GIFT
  gift-translate "ξ = 5π/16" --from GIFT --to SM
  gift-translate "α" --from SM --to GIFT
  gift-translate --interactive
        """
    )
    
    parser.add_argument(
        "expression", 
        nargs="?",
        help="Expression to translate"
    )
    
    parser.add_argument(
        "--from", "-f",
        dest="from_format",
        choices=["SM", "GIFT"],
        default="SM",
        help="Source format (default: SM)"
    )
    
    parser.add_argument(
        "--to", "-t",
        dest="to_format",
        choices=["SM", "GIFT"],
        default="GIFT",
        help="Target format (default: GIFT)"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    translator = GIFTTranslator()
    
    if args.interactive:
        interactive_mode(translator)
    elif args.expression:
        translate_single(translator, args.expression, args.from_format, args.to_format, args.verbose)
    else:
        parser.print_help()

def translate_single(translator, expression, from_format, to_format, verbose):
    """Translate a single expression"""
    result = translator.translate(expression, from_format, to_format)
    
    if result['success']:
        print(f"✅ {result['translated']}")
        if verbose:
            print(f"📝 {result['explanation']}")
            print(f"🎯 Confidence: {result['confidence']:.1%}")
            if result.get('warnings'):
                for warning in result['warnings']:
                    print(f"⚠️  {warning}")
    else:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)

def interactive_mode(translator):
    """Interactive translation mode"""
    print("🔬 GIFT Translator - Interactive Mode")
    print("=" * 50)
    print("Enter expressions to translate (or 'quit' to exit):")
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
