// ========== BACKGROUND RANDOMIZER ==========
function initBackground() {
    const container = document.getElementById('bgContainer');
    if (!container) return;

    let images = [];
    try {
        images = JSON.parse(container.dataset.images || '[]');
    } catch (e) {
        console.warn('Failed to parse images:', e);
        return;
    }

    if (images.length === 0) return;

    // Determine how many tiles based on screen size
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth < 1200;
    const tileCount = isMobile ? 4 : (isTablet ? 9 : 16);

    // Shuffle images and pick enough to fill tiles
    const shuffled = [...images].sort(() => Math.random() - 0.5);
    const selected = [];
    for (let i = 0; i < tileCount; i++) {
        selected.push(shuffled[i % shuffled.length]);
    }

    // Shuffle again for variety
    selected.sort(() => Math.random() - 0.5);

    container.innerHTML = '';
    selected.forEach(src => {
        const img = document.createElement('img');
        img.src = 'images/' + src;
        img.alt = '';
        img.loading = 'lazy';
        container.appendChild(img);
    });
}

// ========== NAVIGATION ==========
function initNav() {
    const navBar = document.getElementById('navBar');
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    const anchorBtn = document.getElementById('navAnchorBtn');

    if (!navBar) return;

    // Mobile toggle
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            navToggle.classList.toggle('active');
        });
    }

    // Anchor / pin toggle
    let isPinned = localStorage.getItem('navPinned') !== 'false';
    updatePinState();

    if (anchorBtn) {
        anchorBtn.addEventListener('click', () => {
            isPinned = !isPinned;
            localStorage.setItem('navPinned', isPinned);
            updatePinState();
        });
    }

    function updatePinState() {
        if (!navBar) return;
        if (isPinned) {
            navBar.classList.add('floating');
            navBar.classList.remove('unpinned');
            anchorBtn.classList.remove('unpinned');
        } else {
            navBar.classList.remove('floating');
            navBar.classList.add('unpinned');
            anchorBtn.classList.add('unpinned');
        }
    }

    // Add shadow on scroll when pinned
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        if (!isPinned) return;
        const currentScroll = window.scrollY;
        if (currentScroll > 10) {
            navBar.classList.add('shadow');
        } else {
            navBar.classList.remove('shadow');
        }
        lastScroll = currentScroll;
    });
}

// ========== MLG EASTER EGG ==========
function initMlg() {
    // Load the real AWP sound from the provided MP3
    const soundPath = document.body.dataset.soundPath || 'audio/awp.mp3';
    const awpSound = new Audio(soundPath);
    awpSound.volume = 0.3;
    awpSound.load();

    function playAwp() {
        try {
            const clone = awpSound.cloneNode();
            clone.volume = 0.3;
            clone.play().catch(() => {}); // Ignore autoplay restrictions
        } catch (e) {
            console.warn('AWP sound failed:', e);
        }
    }

    function showCrossmark(x, y) {
        const crossmark = document.createElement('div');
        crossmark.className = 'mlg-crossmark';
        crossmark.style.left = x + 'px';
        crossmark.style.top = y + 'px';
        // Rendered SVG hitmarker: 4 diagonal lines with rounded caps,
        // red outline + white inner, 40% gap toward center, 60% line length
        crossmark.innerHTML = `
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Red outlines (thick, behind) -->
                <line x1="34" y1="34" x2="10" y2="10" stroke="#B22222" stroke-width="10" stroke-linecap="round"/>
                <line x1="66" y1="34" x2="90" y2="10" stroke="#B22222" stroke-width="10" stroke-linecap="round"/>
                <line x1="34" y1="66" x2="10" y2="90" stroke="#B22222" stroke-width="10" stroke-linecap="round"/>
                <line x1="66" y1="66" x2="90" y2="90" stroke="#B22222" stroke-width="10" stroke-linecap="round"/>
                <!-- White inner lines (thin, on top) -->
                <line x1="34" y1="34" x2="10" y2="10" stroke="white" stroke-width="5" stroke-linecap="round"/>
                <line x1="66" y1="34" x2="90" y2="10" stroke="white" stroke-width="5" stroke-linecap="round"/>
                <line x1="34" y1="66" x2="10" y2="90" stroke="white" stroke-width="5" stroke-linecap="round"/>
                <line x1="66" y1="66" x2="90" y2="90" stroke="white" stroke-width="5" stroke-linecap="round"/>
            </svg>
        `;
        document.body.appendChild(crossmark);
        setTimeout(() => crossmark.remove(), 450);
    }

    document.addEventListener('click', (e) => {
        // Don't trigger on buttons, links, or interactive elements
        const tag = e.target.tagName.toLowerCase();
        if (['a', 'button', 'input', 'textarea', 'select'].includes(tag)) return;
        if (e.target.closest('a') || e.target.closest('button')) return;

        playAwp();
        showCrossmark(e.clientX, e.clientY);
    });
}

// ========== INIT ==========
document.addEventListener('DOMContentLoaded', () => {
    initBackground();
    initNav();
    initMlg();
});
