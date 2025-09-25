# 🔬 GIFT TRANSLATOR - MATRIX MODE

**Style Terminal/Matrix avec fond noir et vert néon**

## 🚀 Utilisation

### Interface Web (Style Matrix)
```bash
# Démarrer le serveur
python -m gift_translator.web_interface

# Ouvrir http://localhost:5000
# Interface style Pi-boy de Fallout avec:
# - Fond noir
# - Texte vert néon (#00ff00)
# - Police monospace (Courier New)
# - Boutons carrés style terminal
# - Effets de glow/box-shadow
```

### Ligne de Commande
```bash
# Mode interactif Matrix
python -m gift_translator.cli --interactive

# Traduction directe
python -m gift_translator.cli "E = mc²" --from SM --to GIFT

# Test avec style Matrix
python test_translator.py
```

## 🎮 Fonctionnalités

### ✅ **Input persistant**
- L'expression originale reste dans la zone source après traduction
- Seule la zone cible est mise à jour avec le résultat

### 🎨 **Style Matrix/Terminal**
- **Fond**: Noir (#000000)
- **Texte principal**: Vert néon (#00ff00)
- **Texte secondaire**: Vert foncé (#00aa00)
- **Police**: Courier New (monospace)
- **Boutons**: Carrés avec bordures vertes et effets glow
- **Effets**: Box-shadow, text-shadow pour effet néon

### 🔄 **Traductions bidirectionnelles**
| Expression SM | → Expression GIFT | Confiance |
|---------------|-------------------|-----------|
| `E = mc²` | `E = ξ·τ·c²·m` | 95% |
| `α = e²/(4πε₀ℏc)` | `α⁻¹ = ζ₃ × 114 - 1/24` | 95% |
| `sin²θ_W = g'²/(g² + g'²)` | `sin²θ_W = ζ₂ - √2` | 95% |
| `ξ = 5π/16` | `ξ ≈ 0.9817` | 80% |

## 🎯 **Exemples d'utilisation**

### Interface Web
1. Ouvrir http://localhost:5000
2. Taper `E = mc²` dans la zone SM
3. Cliquer sur "TRANSLATE.EXE"
4. Voir le résultat dans la zone GIFT : `E = ξ·τ·c²·m`
5. L'input original reste dans la zone SM

### CLI Interactif
```
> E = mc² SM GIFT
✅ E = ξ·τ·c²·m
📝 GIFT geometric corrections to mass-energy relation
🎯 Confidence: 95.0%

> ξ = 5π/16 GIFT SM
✅ ξ ≈ 0.9817
📝 GIFT geometric constants converted to Standard Model parameters
🎯 Confidence: 80.0%
```

## 🎨 **Style Matrix - Détails**

### Couleurs
- **Vert néon principal**: `#00ff00`
- **Vert foncé**: `#00aa00`
- **Vert aqua**: `#00ffaa`
- **Jaune warning**: `#ffff00`
- **Rouge erreur**: `#ff0000`

### Effets
- **Glow**: `box-shadow: 0 0 10px #00ff00`
- **Text shadow**: `text-shadow: 0 0 5px #00ff00`
- **Bordures**: `border: 2px solid #00ff00`

### Typographie
- **Police**: `'Courier New', 'Monaco', 'Menlo', monospace`
- **Style**: Uppercase, letter-spacing
- **Taille**: Responsive, lisible

## 🐛 **Bugs connus**
- Substitutions répétitives dans certaines expressions complexes
- Certaines traductions peuvent nécessiter une vérification manuelle
- Le style Matrix peut être intense pour certains utilisateurs

## 🚀 **Améliorations futures**
- [ ] Correction des bugs de substitution
- [ ] Plus d'équations connues
- [ ] Mode sombre/clair toggle
- [ ] Export des traductions
- [ ] Historique des traductions

---

**GIFT.TRANSLATOR.EXE - READY FOR QUANTUM TRANSLATION** 🚀
