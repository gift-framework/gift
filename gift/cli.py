"""
Command-line interface for GIFT framework
"""

import argparse
import sys
from .core import GIFTConstants, GIFTCalculator, GIFTValidator

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="GIFT Framework - Geometric Information Field Theory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gift-validate                    # Run full validation
  gift-validate --summary          # Show validation summary only
  gift-validate --observable alpha_inv_0  # Check specific observable
        """
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "--summary", 
        action="store_true",
        help="Show validation summary only"
    )
    
    parser.add_argument(
        "--observable", 
        type=str,
        help="Check specific observable (e.g., alpha_inv_0, sin2_theta_W)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize GIFT framework
        constants = GIFTConstants()
        calculator = GIFTCalculator(constants)
        validator = GIFTValidator(calculator)
        
        if args.observable:
            # Check specific observable
            report = validator.get_validation_report()
            if args.observable in report:
                data = report[args.observable]
                print(f"Observable: {args.observable}")
                print(f"Predicted: {data['predicted']:.6f}")
                print(f"Experimental: {data['experimental']:.6f}")
                print(f"Relative error: {data['relative_error_percent']:.3f}%")
            else:
                print(f"Unknown observable: {args.observable}")
                print(f"Available observables: {', '.join(report.keys())}")
                sys.exit(1)
        else:
            # Run full validation
            if args.summary:
                validator.print_summary()
            else:
                print("GIFT Framework Validation")
                print("=" * 50)
                validator.print_summary()
                
                if args.verbose:
                    print("\nDetailed Results:")
                    print("-" * 50)
                    report = validator.get_validation_report()
                    for observable, data in report.items():
                        print(f"{observable:20}: {data['predicted']:10.6f} (exp: {data['experimental']:10.6f}, error: {data['relative_error_percent']:6.3f}%)")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
