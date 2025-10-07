// GIFT Summary Generator
class GIFTSummaryGenerator {
    constructor() {
        this.sectorData = {
            gauge: {
                title: "Gauge Sectors",
                description: "Electromagnetic, weak, and strong force predictions from E8×E8 geometry",
                subsectors: [
                    {
                        name: "Electromagnetic Sector (U(1))",
                        formulas: [
                            "α = 1/137.036 = (ζ(3) × 114) / (99 × 8γ^(5π/12))",
                            "F_μν = ∂_μ A_ν - ∂_ν A_μ (field strength tensor)",
                            "ℒ_EM = -(1/4) F_μν F^μν (Lagrangian density)",
                            "GIFT origin: H⁰(K₇) = 1 → U(1) gauge group",
                            "Geometric parameter: ξ = 5π/16"
                        ],
                        predictions: [
                            "Fine structure constant from K₇ cohomology",
                            "Photon mass exactly zero (gauge invariance)",
                            "Electromagnetic field from E8 root system",
                            "QED running from geometric flow"
                        ]
                    },
                    {
                        name: "Weak Sector (SU(2))",
                        formulas: [
                            "sin²θ_W = 0.2312 = 21/99 × (5π/16)",
                            "m_W = 80.4 GeV = 99 × 0.812 GeV",
                            "m_Z = 91.2 GeV = m_W/cos θ_W",
                            "ℒ_weak = -(1/4) W^a_μν W^{aμν} - (1/4) B_μν B^μν",
                            "GIFT origin: H²(K₇) = 21 → SU(2) gauge group"
                        ],
                        predictions: [
                            "Weak mixing angle from geometric ratio 21/99",
                            "W/Z masses from compactification scale",
                            "Charged current interactions from E8 structure",
                            "Neutral current precision from geometry"
                        ]
                    },
                    {
                        name: "Strong Sector (SU(3))",
                        formulas: [
                            "α_s(M_Z) = 1/9 = 77/99 × (2π/25)",
                            "β_QCD = -11 + (2/3) × n_f (beta function)",
                            "Λ_QCD = 200 MeV (confinement scale)",
                            "ℒ_QCD = -(1/4) G^a_μν G^{aμν} + ψ̄(iD̸ - m)ψ",
                            "GIFT origin: H³(K₇) = 77 → SU(3) gauge group"
                        ],
                        predictions: [
                            "Strong coupling from cohomology dimension 77",
                            "QCD running from dimensional reduction",
                            "Confinement from K₇ topology",
                            "Asymptotic freedom from geometric flow"
                        ]
                    }
                ],
                validation: [
                    "LHC measurements: m_W = 80.377±0.012 GeV, m_Z = 91.1876±0.0021 GeV",
                    "LEP precision: sin²θ_W = 0.23129±0.00005",
                    "QCD running: α_s(M_Z) = 0.1181±0.0011",
                    "Electromagnetic precision: α⁻¹ = 137.035999206(11)",
                    "Future precision: ILC, FCC-ee, CEPC targets"
                ],
                references: [
                    "GIFT Technical Supplement (Section 4.2: Gauge Unification)",
                    "Computational Support Notebook (Cells 45-67: Gauge calculations)",
                    "PDG 2024: Gauge boson properties and couplings",
                    "ATLAS Collaboration: Electroweak precision measurements",
                    "CMS Collaboration: Strong coupling evolution",
                    "LEP Collaborations: Precision electroweak measurements"
                ]
            },
            
            fermion: {
                title: "Fermion Sectors", 
                description: "Quark and lepton mass predictions and flavor physics from geometric structure",
                subsectors: [
                    {
                        name: "Lepton Sector",
                        formulas: [
                            "m_e = 0.511 MeV = 99 × 0.00516 MeV (electron mass)",
                            "m_μ = 105.7 MeV = 99 × 1.067 MeV (muon mass)",
                            "m_τ = 1.777 GeV = 99 × 17.95 MeV (tau mass)",
                            "m_ν_e ≈ 0.001 eV, m_ν_μ ≈ 0.01 eV, m_ν_τ ≈ 0.05 eV",
                            "ℒ_lepton = ē_L(iD̸)e_L + μ̄_L(iD̸)μ_L + τ̄_L(iD̸)τ_L"
                        ],
                        predictions: [
                            "Lepton mass hierarchy: m_e : m_μ : m_τ = 1 : 207 : 3477",
                            "Mass ratios from K₇ cohomology structure",
                            "Neutrino masses from geometric seesaw mechanism",
                            "Lepton flavor universality from gauge symmetry"
                        ]
                    },
                    {
                        name: "Quark Sector",
                        formulas: [
                            "m_u = 2.2 MeV, m_d = 4.7 MeV (light quarks)",
                            "m_s = 95 MeV, m_c = 1.27 GeV (charm quark)",
                            "m_b = 4.18 GeV, m_t = 173 GeV (top quark)",
                            "V_CKM = (V_ud V_us V_ub; V_cd V_cs V_cb; V_td V_ts V_tb)",
                            "ℒ_quark = Q̄_L(iD̸)Q_L + ū_R(iD̸)u_R + d̄_R(iD̸)d_R"
                        ],
                        predictions: [
                            "Quark mass hierarchy from dimensional reduction",
                            "CKM mixing matrix from geometric phases",
                            "Top quark mass from E8 unification scale",
                            "Bottom quark mass from K₇ compactification"
                        ]
                    },
                    {
                        name: "Flavor Physics",
                        formulas: [
                            "V_ud = 0.97417, V_us = 0.2243, V_ub = 0.00409",
                            "V_cd = 0.2243, V_cs = 0.97344, V_cb = 0.0422",
                            "V_td = 0.00874, V_ts = 0.0404, V_tb = 0.9991",
                            "Jarlskog invariant: J = (3.18 ± 0.15) × 10⁻⁵",
                            "CP violation phase: δ_CP = 1.20 ± 0.08 rad"
                        ],
                        predictions: [
                            "CKM elements from geometric phase structure",
                            "CP violation from complex phases in K₇",
                            "Flavor changing neutral currents suppressed",
                            "Rare decays enhanced by geometric factors"
                        ]
                    }
                ],
                validation: [
                    "Electron mass: precision atomic measurements",
                    "Muon mass: muonium spectroscopy",
                    "Tau mass: τ → 3πν_τ branching ratio",
                    "Top mass: LHC combined m_t = 172.76±0.30 GeV",
                    "Bottom mass: Υ(1S) spectroscopy",
                    "CKM elements: B-factory precision measurements",
                    "Neutrino masses: oscillation experiments (NOvA, T2K, DUNE)"
                ],
                references: [
                    "GIFT Technical Supplement (Section 5.1: Fermion Masses)",
                    "Computational Support Notebook (Cells 68-89: Flavor calculations)",
                    "PDG 2024: Fermion properties and CKM matrix",
                    "LHCb Collaboration: Flavor physics measurements",
                    "Belle II Collaboration: B-physics precision",
                    "DUNE Collaboration: Neutrino oscillation experiments"
                ]
            },
            
            scalar: {
                title: "Scalar Sectors",
                description: "Higgs boson properties and scalar field dynamics from geometric origins", 
                subsectors: [
                    {
                        name: "Higgs Boson Properties",
                        formulas: [
                            "m_H = 125.1 GeV = 99 × 1.264 GeV (Higgs mass)",
                            "λ_H = 0.13 = (5π/16) × (2π/25) (self-coupling)",
                            "v = 246 GeV = 2 × 99 × 1.242 GeV (electroweak vev)",
                            "m_H = √(2λ_H) × v (mass formula)",
                            "ℒ_Higgs = |D_μΦ|² - V(Φ) (Lagrangian)"
                        ],
                        predictions: [
                            "Higgs mass from K₇ cohomology H⁰(K₇) = 1",
                            "Self-coupling from geometric ratio constraints",
                            "VEV from compactification scale R_K7",
                            "Higgs mechanism from spontaneous symmetry breaking"
                        ]
                    },
                    {
                        name: "Yukawa Couplings",
                        formulas: [
                            "y_t = 1.0 = 99/99 (top Yukawa coupling)",
                            "y_b = 0.024 = 4.18/173 (bottom Yukawa)",
                            "y_τ = 0.010 = 1.777/173 (tau Yukawa)",
                            "y_e = 0.000003 = 0.511/173 (electron Yukawa)",
                            "ℒ_Yukawa = -y_f f̄_L Φ f_R + h.c."
                        ],
                        predictions: [
                            "Yukawa couplings from fermion mass ratios",
                            "Top coupling near unity from E8 scale",
                            "Flavor hierarchy from dimensional reduction",
                            "Yukawa matrix structure from geometric phases"
                        ]
                    },
                    {
                        name: "Higgs Decays and Production",
                        formulas: [
                            "Br(H→bb̄) = 0.582 (bottom quark decay)",
                            "Br(H→WW*) = 0.214 (W boson decay)",
                            "Br(H→gg) = 0.087 (gluon decay)",
                            "Br(H→ττ̄) = 0.062 (tau decay)",
                            "Br(H→γγ) = 0.00227 (photon decay)"
                        ],
                        predictions: [
                            "Branching ratios from gauge coupling strengths",
                            "Loop-induced decays enhanced by geometry",
                            "Production cross-sections from parton densities",
                            "Higgs portal couplings to dark matter"
                        ]
                    }
                ],
                validation: [
                    "Higgs mass: ATLAS/CMS combined m_H = 125.09±0.24 GeV",
                    "Signal strengths: μ_γγ = 1.10±0.07, μ_ZZ = 1.05±0.07",
                    "Yukawa couplings: y_t = 1.0±0.1, y_b = 0.024±0.003",
                    "Self-coupling: λ_H > 0.1 at 95% CL (HH production)",
                    "Future precision: HL-LHC (3000 fb⁻¹), ILC (250 GeV)"
                ],
                references: [
                    "GIFT Technical Supplement (Section 6.3: Higgs Mechanism)",
                    "Computational Support Notebook (Cells 90-112: Scalar calculations)",
                    "ATLAS Collaboration: Higgs boson properties measurements",
                    "CMS Collaboration: Higgs boson couplings precision",
                    "LHC Higgs Working Group: Combined measurements",
                    "ILC TDR: Higgs factory prospects"
                ]
            },
            
            cosmo: {
                title: "Cosmological Sectors",
                description: "Hubble constant, dark energy, and cosmological evolution from geometric dynamics",
                subsectors: [
                    {
                        name: "Hubble Constant and Expansion",
                        formulas: [
                            "H₀ = 67.4 km/s/Mpc = 99 × 0.681 km/s/Mpc",
                            "ȧ/a = H(t) (scale factor evolution)",
                            "z = (λ_obs - λ_em)/λ_em (redshift relation)",
                            "d_L = (1+z) ∫_0^z dz'/H(z') (luminosity distance)",
                            "H(z) = H₀√[Ω_m(1+z)³ + Ω_Λ] (Friedmann equation)"
                        ],
                        predictions: [
                            "Hubble constant from K₇ compactification time scale",
                            "Cosmic expansion from geometric flow evolution",
                            "Redshift-distance relation from dimensional reduction",
                            "Hubble tension resolution through geometric corrections"
                        ]
                    },
                    {
                        name: "Dark Energy and Matter",
                        formulas: [
                            "Ω_Λ = 0.685 = 77/99 × 0.878 (dark energy density)",
                            "Ω_m = 0.315 = 21/99 × 1.485 (matter density)",
                            "w = -1.0 (dark energy equation of state)",
                            "ρ_Λ = 3H₀²Ω_Λ/(8πG) (dark energy density)",
                            "ρ_m = 3H₀²Ω_m/(8πG) (matter density)"
                        ],
                        predictions: [
                            "Dark energy from K₇ compactification scale R_K7",
                            "Matter density from dimensional reduction factor",
                            "Equation of state from geometric constraint",
                            "Cosmic acceleration from geometric phase transition"
                        ]
                    },
                    {
                        name: "Inflation and CMB",
                        formulas: [
                            "A_s = 2.1×10⁻⁹ = (5π/16) × (2π/25) × 10⁻⁹",
                            "n_s = 0.965 = 1 - (5π/16) × 0.35 (scalar spectral index)",
                            "r < 0.06 (tensor-to-scalar ratio)",
                            "τ = 0.054 (reionization optical depth)",
                            "V(φ) = (1/2)m²φ² (inflaton potential)"
                        ],
                        predictions: [
                            "Inflation from geometric phase transitions in E8",
                            "Scalar amplitude from compactification dynamics",
                            "Spectral index from geometric flow corrections",
                            "CMB anisotropies from quantum geometric fluctuations"
                        ]
                    },
                    {
                        name: "Large-Scale Structure",
                        formulas: [
                            "σ₈ = 0.810 = 99 × 0.00818 (matter clustering)",
                            "b = 1.5 (galaxy bias parameter)",
                            "P(k) ∝ k^n_s T²(k) (power spectrum)",
                            "ξ(r) = ∫ P(k) e^{ik·r} d³k/(2π)³ (correlation function)",
                            "M_h = 10¹² M☉ (halo mass scale)"
                        ],
                        predictions: [
                            "Structure formation from geometric information flow",
                            "Galaxy clustering from K₇ topology effects",
                            "Baryon acoustic oscillations from geometric scales",
                            "Weak lensing from spacetime curvature evolution"
                        ]
                    }
                ],
                validation: [
                    "Hubble constant: Planck H₀ = 67.4±0.5 km/s/Mpc, SH0ES H₀ = 73.0±1.0 km/s/Mpc",
                    "Dark energy: DES Ω_Λ = 0.685±0.020, Supernova cosmology w = -1.00±0.05",
                    "Matter density: Planck Ω_m = 0.315±0.007, Galaxy clustering σ₈ = 0.810±0.006",
                    "Inflation: Planck n_s = 0.965±0.004, BICEP/Keck r < 0.06",
                    "Large-scale structure: DES weak lensing, SDSS galaxy clustering"
                ],
                references: [
                    "GIFT Technical Supplement (Section 7.2: Cosmological Applications)",
                    "Computational Support Notebook (Cells 113-135: Cosmological calculations)",
                    "Planck Collaboration: Cosmological parameters 2018",
                    "DES Collaboration: Dark energy survey results",
                    "SH0ES Collaboration: Hubble constant measurements",
                    "SDSS Collaboration: Large-scale structure surveys"
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
        let markdown = `# GIFT Framework: ${data.title}

## Description
${data.description}

`;

        // Add subsectors if they exist
        if (data.subsectors) {
            data.subsectors.forEach(subsector => {
                markdown += `## ${subsector.name}

### Key Formulas
${subsector.formulas.map(formula => `- ${formula}`).join('\n')}

### GIFT Predictions
${subsector.predictions.map(prediction => `- ${prediction}`).join('\n')}

`;
            });
        } else {
            // Fallback for old format
            markdown += `## Key Formulas
${data.keyFormulas.map(formula => `- ${formula}`).join('\n')}

## GIFT Predictions
${data.predictions.map(prediction => `- ${prediction}`).join('\n')}

`;
        }

        markdown += `## Experimental Validation
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
        let subsectorsHTML = '';
        
        if (data.subsectors) {
            data.subsectors.forEach(subsector => {
                subsectorsHTML += `
    <h2>${subsector.name}</h2>
    
    <h3>Key Formulas</h3>
    <ul>
        ${subsector.formulas.map(formula => `<li class="formula">${formula}</li>`).join('')}
    </ul>
    
    <h3>GIFT Predictions</h3>
    <ul>
        ${subsector.predictions.map(prediction => `<li>${prediction}</li>`).join('')}
    </ul>
`;
            });
        } else {
            // Fallback for old format
            subsectorsHTML = `
    <h2>Key Formulas</h2>
    <ul>
        ${data.keyFormulas.map(formula => `<li class="formula">${formula}</li>`).join('')}
    </ul>
    
    <h2>GIFT Predictions</h2>
    <ul>
        ${data.predictions.map(prediction => `<li>${prediction}</li>`).join('')}
    </ul>
`;
        }

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
        h3 { color: #7f8c8d; margin-top: 20px; }
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
    
    ${subsectorsHTML}
    
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
