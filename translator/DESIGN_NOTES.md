# GIFT Translator - Design Notes

## Design Philosophy

**Minimalist Terminal Aesthetic**
- Pure black background (#000000)
- Neon green accent (#00ff41)
- Clean typography with modern sans-serif fonts
- No gradients, shadows, or decorative elements

## Mobile-First Responsive Design

### Breakpoints
- **Desktop**: 1200px+ (3-column layout)
- **Tablet**: 768px-1199px (stacked layout)
- **Mobile**: 480px-767px (single column, optimized spacing)
- **Small Mobile**: <480px (compact layout)

### Mobile Optimizations
1. **Grid Layout**: Switches from 3-column to single-column on mobile
2. **Swap Button**: Moves to top of layout on mobile for better UX
3. **Typography**: Responsive font sizes (2.5rem → 1.8rem on mobile)
4. **Spacing**: Reduced padding and margins for mobile screens
5. **Touch Targets**: Minimum 44px touch targets for buttons
6. **Viewport**: Optimized meta tags for mobile rendering

### Key CSS Features
```css
/* Mobile-first responsive grid */
.translation-area {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 20px;
}

@media (max-width: 768px) {
    .translation-area {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .swap-button {
        order: -1;
        margin: 0 auto 20px;
    }
}
```

## Typography

### Font Stack
```css
font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Code Font
```css
font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

### Typography Scale
- **H1**: 2.5rem (desktop) → 1.8rem (mobile)
- **Body**: 1rem
- **Code**: 14px (desktop) → 13px (mobile)
- **Labels**: 14px uppercase with letter-spacing

## Color Scheme

### Primary Colors
- **Background**: #000000 (pure black)
- **Text**: #00ff41 (neon green)
- **Borders**: #00ff41 (neon green)
- **Accent**: #ff0040 (neon red for errors)

### Interactive States
- **Hover**: Background fills with accent color, text inverts
- **Focus**: Clean outline with accent color
- **Active**: Maintains hover state

## Accessibility

### Features
- High contrast ratio (black/green)
- Keyboard navigation support
- Screen reader friendly
- Touch-friendly mobile interface
- Semantic HTML structure

### Keyboard Shortcuts
- **Ctrl+Enter**: Translate formula
- **Tab**: Navigate between elements
- **Enter**: Submit forms

## Performance

### Optimizations
- Pure CSS (no external dependencies)
- Minimal JavaScript
- Optimized for mobile networks
- Fast loading times
- No external fonts required

## Browser Support

### Modern Browsers
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

### Mobile Browsers
- iOS Safari 12+
- Chrome Mobile 60+
- Samsung Internet 8+

## Testing

### Mobile Testing
- iPhone SE (375px)
- iPhone 12 (390px)
- Samsung Galaxy S21 (360px)
- iPad (768px)

### Desktop Testing
- 1920x1080 (Full HD)
- 1366x768 (Common laptop)
- 2560x1440 (2K displays)

## Future Enhancements

### Potential Improvements
1. **Dark Mode Toggle**: Switch between themes
2. **Font Size Controls**: Accessibility options
3. **Export Functions**: Save translations
4. **History**: Previous translations
5. **Advanced Mode**: More complex formulas

### Technical Debt
- Consider CSS Grid fallbacks for older browsers
- Add progressive enhancement for JavaScript
- Implement service worker for offline functionality
