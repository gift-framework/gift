// GIFT Summary Generator
class GIFTSummaryGenerator {
    constructor() {
        this.sectorData = {
            gauge: {
                title: "Gauge Sectors",
                description: "Electromagnetic, weak, and strong force predictions",
                keyFormulas: [
                    "α = 1/137.036 (fine structure constant)",
                    "sin²θ_W = 0.2312 (weak mixing angle)",
                    "α_s = 1/9 (strong coupling at M_Z)",
                    "m_W = 80.4 GeV (W boson mass)",
                    "m_Z = 91.2 GeV (Z boson mass)"
                ],
                predictions: [
                    "U(1) gauge group from H⁰(K₇) = 1",
                    "SU(2) gauge group from H²(K₇) = 21", 
                    "SU(3) gauge group from H³(K₇) = 77",
                    "Gauge coupling unification at ~1 TeV",
                    "Geometric origin of electroweak mixing"
                ],
                validation: [
                    "LHC measurements: m_W, m_Z within 0.1%",
                    "LEP precision tests: sin²θ_W agreement",
                    "QCD running: α_s evolution consistent",
                    "Electromagnetic precision: α measurements",
                    "Future tests: LHC Run 3, ILC precision"
                ],
                references: [
                    "GIFT Technical Supplement (Section 4.2)",
                    "Computational Support Notebook (Cells 45-67)",
                    "PDG 2024: Gauge boson properties",
                    "LHCb Collaboration: Electroweak measurements"
                ]
            },
            
            fermion: {
                title: "Fermion Sectors", 
                description: "Quark and lepton mass predictions and flavor physics",
                keyFormulas: [
                    "m_e = 0.511 MeV (electron mass)",
                    "m_μ = 105.7 MeV (muon mass)",
                    "m_τ = 1.777 GeV (tau mass)",
                    "m_t = 173 GeV (top quark mass)",
                    "V_CKM mixing matrix elements"
                ],
                predictions: [
                    "Lepton mass hierarchy from K₇ geometry",
                    "Quark mass pattern from dimensional reduction",
                    "CKM mixing from geometric phases",
                    "Neutrino masses from K₇ topology",
                    "Flavor violation suppressed by geometry"
                ],
                validation: [
                    "Tau mass: LHC precision measurements",
                    "Top mass: Tevatron + LHC combined",
                    "CKM elements: B-factory precision",
                    "Neutrino masses: oscillation experiments",
                    "Lepton universality: LHCb tests"
                ],
                references: [
                    "GIFT Technical Supplement (Section 5.1)",
                    "Computational Support Notebook (Cells 68-89)",
                    "PDG 2024: Fermion properties",
                    "Belle II Collaboration: Flavor physics"
                ]
            },
            
            scalar: {
                title: "Scalar Sectors",
                description: "Higgs boson properties and scalar field dynamics", 
                keyFormulas: [
                    "m_H = 125.1 GeV (Higgs boson mass)",
                    "λ_H = 0.13 (Higgs self-coupling)",
                    "v = 246 GeV (electroweak vev)",
                    "y_t = 1.0 (top Yukawa coupling)",
                    "Br(H→γγ) = 2.27×10⁻³ (branching ratio)"
                ],
                predictions: [
                    "Higgs mass from K₇ cohomology (H⁰(K₇) = 1)",
                    "Self-coupling from geometric constraints",
                    "Yukawa couplings from dimensional reduction",
                    "Branching ratios from gauge unification",
                    "Higgs portal to dark matter"
                ],
                validation: [
                    "Higgs mass: ATLAS/CMS combined (125.09±0.24 GeV)",
                    "Signal strengths: γγ, ZZ, WW channels",
                    "Yukawa couplings: tH, bH, τH production",
                    "Self-coupling: HH production limits",
                    "Future tests: HL-LHC, ILC precision"
                ],
                references: [
                    "GIFT Technical Supplement (Section 6.3)",
                    "Computational Support Notebook (Cells 90-112)",
                    "ATLAS Collaboration: Higgs properties",
                    "CMS Collaboration: Higgs measurements"
                ]
            },
            
            cosmo: {
                title: "Cosmological Sectors",
                description: "Hubble constant, dark energy, and cosmological evolution",
                keyFormulas: [
                    "H₀ = 67.4 km/s/Mpc (Hubble constant)",
                    "Ω_m = 0.315 (matter density parameter)",
                    "Ω_Λ = 0.685 (dark energy parameter)",
                    "w = -1.0 (dark energy equation of state)",
                    "A_s = 2.1×10⁻⁹ (scalar amplitude)"
                ],
                predictions: [
                    "Hubble constant from geometric time evolution",
                    "Dark energy from K₇ compactification scale",
                    "Matter density from dimensional reduction",
                    "Inflation from geometric phase transitions",
                    "Large-scale structure from information flow"
                ],
                validation: [
                    "H₀ tension: Planck vs local measurements",
                    "Dark energy: Supernova cosmology",
                    "Matter density: Galaxy clustering",
                    "Inflation: CMB temperature fluctuations",
                    "Structure: Weak lensing surveys"
                ],
                references: [
                    "GIFT Technical Supplement (Section 7.2)",
                    "Computational Support Notebook (Cells 113-135)",
                    "Planck Collaboration: Cosmological parameters",
                    "DES Collaboration: Dark energy survey"
                ]
            }
        };
    }

    generateSummary(sector, format) {
        const data = this.sectorData[sector];
        if (!data) {
            this.showStatus('Error: Invalid sector', 'error');
            return;
        }

        if (format === 'md') {
            this.generateMarkdown(data);
        } else if (format === 'pdf') {
            this.generatePDF(data);
        } else {
            this.showStatus('Error: Invalid format', 'error');
        }
    }

    generateMarkdown(data) {
        const markdown = `# GIFT Framework: ${data.title}

## Description
${data.description}

## Key Formulas
${data.keyFormulas.map(formula => `- ${formula}`).join('\n')}

## GIFT Predictions
${data.predictions.map(prediction => `- ${prediction}`).join('\n')}

## Experimental Validation
${data.validation.map(validation => `- ${validation}`).join('\n')}

## References
${data.references.map(ref => `- ${ref}`).join('\n')}

---
*Generated by GIFT Summary Generator*
*Framework under theoretical development - predictions require validation*
`;

        this.downloadFile(markdown, `gift_${data.title.toLowerCase().replace(/\s+/g, '_')}_summary.md`, 'text/markdown');
        this.showStatus(`Markdown summary for ${data.title} generated successfully`, 'success');
    }

    generatePDF(data) {
        // Create HTML content for PDF generation
        const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        ul { margin: 10px 0; }
        li { margin: 5px 0; }
        .formula { background: #f8f9fa; padding: 10px; border-left: 4px solid #3498db; margin: 10px 0; }
        .footer { margin-top: 50px; font-size: 0.9em; color: #7f8c8d; border-top: 1px solid #bdc3c7; padding-top: 20px; }
    </style>
</head>
<body>
    <h1>GIFT Framework: ${data.title}</h1>
    
    <h2>Description</h2>
    <p>${data.description}</p>
    
    <h2>Key Formulas</h2>
    <ul>
        ${data.keyFormulas.map(formula => `<li class="formula">${formula}</li>`).join('')}
    </ul>
    
    <h2>GIFT Predictions</h2>
    <ul>
        ${data.predictions.map(prediction => `<li>${prediction}</li>`).join('')}
    </ul>
    
    <h2>Experimental Validation</h2>
    <ul>
        ${data.validation.map(validation => `<li>${validation}</li>`).join('')}
    </ul>
    
    <h2>References</h2>
    <ul>
        ${data.references.map(ref => `<li>${ref}</li>`).join('')}
    </ul>
    
    <div class="footer">
        <p><strong>Generated by GIFT Summary Generator</strong></p>
        <p><em>Framework under theoretical development - predictions require validation</em></p>
        <p>Generated on: ${new Date().toLocaleDateString()}</p>
    </div>
</body>
</html>`;

        // For PDF generation, we'll use the browser's print functionality
        // In a real implementation, you might want to use a library like jsPDF or Puppeteer
        this.generatePDFFromHTML(htmlContent, `gift_${data.title.toLowerCase().replace(/\s+/g, '_')}_summary.pdf`);
        this.showStatus(`PDF summary for ${data.title} generated successfully`, 'success');
    }

    generatePDFFromHTML(htmlContent, filename) {
        // Create a new window with the HTML content
        const printWindow = window.open('', '_blank');
        printWindow.document.write(htmlContent);
        printWindow.document.close();
        
        // Wait for content to load, then trigger print
        printWindow.onload = function() {
            printWindow.print();
            // Close the window after printing
            setTimeout(() => printWindow.close(), 1000);
        };
    }

    generateAllSummaries(format) {
        const sectors = Object.keys(this.sectorData);
        let completed = 0;
        
        this.showStatus(`Generating ${sectors.length} summaries...`, 'success');
        
        sectors.forEach((sector, index) => {
            setTimeout(() => {
                this.generateSummary(sector, format);
                completed++;
                
                if (completed === sectors.length) {
                    setTimeout(() => {
                        this.showStatus(`All ${sectors.length} summaries generated successfully`, 'success');
                    }, 500);
                }
            }, index * 1000); // Stagger the generation
        });
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    showStatus(message, type) {
        const status = document.getElementById('status');
        status.textContent = message;
        status.className = `status ${type}`;
        status.style.display = 'block';
        
        // Hide status after 5 seconds
        setTimeout(() => {
            status.style.display = 'none';
        }, 5000);
    }
}

// Initialize the generator
const generator = new GIFTSummaryGenerator();

// Global functions for HTML onclick events
function generateSummary(sector, format) {
    generator.generateSummary(sector, format);
}

function generateAllSummaries(format) {
    generator.generateAllSummaries(format);
}
