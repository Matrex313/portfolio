// ================== SIDEBAR ==================
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
    document.body.style.overflow = sidebar.classList.contains('active') ? 'hidden' : 'auto';
}

// Close sidebar when clicking overlay
document.getElementById('overlay')?.addEventListener('click', () => {
    document.getElementById('sidebar').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
    document.body.style.overflow = 'auto';
});

// ================== AVATAR DROPDOWN ==================
document.querySelector('.avatar')?.addEventListener('click', function(e) {
    e.stopPropagation();
    const dropdown = this.nextElementSibling;
    dropdown.classList.toggle('active');
});

document.addEventListener('click', (e) => {
    const dropdown = document.querySelector('.dropdown');
    if (dropdown && !e.target.closest('.avatar-container')) {
        dropdown.classList.remove('active');
    }
});

// ================== TABS ==================
function switchTab(index) {
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach((tab, i) => {
        tab.classList.toggle('active', i === index);
    });

    contents.forEach((content, i) => {
        content.classList.toggle('active', i === index);
    });
}

// ================== ACCORDION ==================
function toggleAccordion(header) {
    const body = header.nextElementSibling;
    const allBodies = document.querySelectorAll('.accordion-body');
    const allHeaders = document.querySelectorAll('.accordion-header');

    // Close all other accordions
    allBodies.forEach(b => b.classList.remove('active'));
    allHeaders.forEach(h => h.classList.remove('active'));

    // Open current
    header.classList.toggle('active');
    body.classList.toggle('active');
}

// ================== MODAL ==================
function showModal() {
    const modal = document.getElementById('modal');
    const overlay = document.getElementById('overlay');
    modal.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('modal');
    const overlay = document.getElementById('overlay');
    modal.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal when clicking overlay
document.getElementById('overlay')?.addEventListener('click', (e) => {
    if (e.target === document.getElementById('overlay')) {
        const modal = document.getElementById('modal');
        if (modal.classList.contains('active')) {
            closeModal();
        }
    }
});

// ================== POPUP ==================
function showPopup() {
    const popup = document.getElementById('popup');
    const overlay = document.getElementById('overlay');
    popup.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closePopup() {
    const popup = document.getElementById('popup');
    const overlay = document.getElementById('overlay');
    popup.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// ================== DRAWER ==================
function showDrawer() {
    const drawer = document.getElementById('drawer');
    const overlay = document.getElementById('overlay');
    drawer.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeDrawer() {
    const drawer = document.getElementById('drawer');
    const overlay = document.getElementById('overlay');
    drawer.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// ================== ALERTS ==================
function showAlert(type, message) {
    const container = document.getElementById('alertContainer');
    const alert = document.createElement('div');
    alert.className = `alert-item ${type}`;
    alert.innerHTML = `${message}`;
    
    container.appendChild(alert);
    
    setTimeout(() => {
        alert.style.animation = 'slide-in-left 0.3s ease reverse';
        setTimeout(() => alert.remove(), 300);
    }, 3000);
}

// ================== FORM SUBMISSION ==================
function submitForm(event) {
    event.preventDefault();
    
    const amount = document.getElementById('tradeAmount').value;
    const notes = document.getElementById('tradeNotes').value;
    
    if (!amount) {
        showAlert('error', '❌ الرجاء إدخال المبلغ');
        return;
    }
    
    showAlert('success', `✅ تم حفظ الصفقة بمبلغ $${amount}`);
    document.querySelector('.form').reset();
}

// ================== VIEW TOGGLE (GRID/LIST) ==================
function switchView(view) {
    const gridView = document.getElementById('gridView');
    const listView = document.getElementById('listView');
    const toggleBtns = document.querySelectorAll('.toggle-btn');

    if (view === 'grid') {
        gridView.style.display = 'block';
        listView.style.display = 'none';
        toggleBtns[0].classList.add('active');
        toggleBtns[1].classList.remove('active');
    } else {
        gridView.style.display = 'none';
        listView.style.display = 'block';
        toggleBtns[0].classList.remove('active');
        toggleBtns[1].classList.add('active');
    }
}

// ================== SEARCH FUNCTIONALITY ==================
document.getElementById('searchInput')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(searchTerm) ? 'flex' : 'none';
    });
});

// ================== SMOOTH SCROLL ==================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ================== ANIMATIONS ON SCROLL ==================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.card, .grid-item, .list-item, .feature-box, .menu-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.5s ease';
    observer.observe(el);
});

// ================== RIPPLE EFFECT ==================
document.querySelectorAll('.btn, .btn-icon, .menu-item, .card').forEach(element => {
    element.addEventListener('click', function(e) {
        if (this.tagName === 'BUTTON' || this.classList.contains('btn')) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.position = 'absolute';
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.animation = 'ripple-animation 0.6s ease-out';
            ripple.style.pointerEvents = 'none';

            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        }
    });
});

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple-animation {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(1);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ================== LIVE PRICE UPDATES ==================
function updatePrices() {
    const priceElements = document.querySelectorAll('.card-price');
    priceElements.forEach(el => {
        const currentPrice = parseFloat(el.textContent.replace('$', '').replace(',', ''));
        const change = (Math.random() - 0.5) * 100;
        const newPrice = currentPrice + change;
        el.textContent = '$' + newPrice.toFixed(2);
        
        // Add animation
        el.style.animation = 'none';
        setTimeout(() => {
            el.style.animation = 'price-pulse 0.5s ease';
        }, 10);
    });
}

// Price update animation
const priceStyle = document.createElement('style');
priceStyle.textContent = `
    @keyframes price-pulse {
        0% {
            color: #09c372;
        }
        50% {
            color: #ffd700;
        }
        100% {
            color: #09c372;
        }
    }
`;
document.head.appendChild(priceStyle);

// Update prices every 3 seconds
setInterval(updatePrices, 3000);

// ================== KEYBOARD SHORTCUTS ==================
document.addEventListener('keydown', function(e) {
    // Escape - close modals
    if (e.key === 'Escape') {
        closeModal();
        closePopup();
        closeDrawer();
        document.getElementById('sidebar').classList.remove('active');
        document.getElementById('overlay').classList.remove('active');
    }
    
    // Ctrl/Cmd + K - focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('searchInput')?.focus();
    }
});

// ================== NOTIFICATIONS ==================
function sendNotification(title, options = {}) {
    if ('Notification' in window) {
        if (Notification.permission === 'granted') {
            new Notification(title, options);
        }
    }
}

// Request notification permission
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// ================== LOCAL STORAGE ==================
function saveSettings(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function loadSettings(key) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

// Save user preferences
document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        saveSettings('viewMode', this.textContent.trim());
    });
});

// ================== DARK MODE TOGGLE ==================
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    saveSettings('darkMode', isDark);
}

// Load saved dark mode preference
const savedDarkMode = loadSettings('darkMode');
if (savedDarkMode) {
    document.body.classList.add('dark-mode');
}

// ================== PERFORMANCE MONITORING ==================
window.addEventListener('load', () => {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log('Page Load Time:', pageLoadTime + 'ms');
});

// ================== LAZY LOADING IMAGES ==================
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ================== CHART/GRAPH SIMULATION ==================
function createMiniChart() {
    const prices = [100, 120, 115, 130, 125, 140, 135];
    const max = Math.max(...prices);
    const min = Math.min(...prices);
    
    return prices.map(price => {
        const height = ((price - min) / (max - min)) * 100;
        return height;
    });
}

// ================== CURRENCY FORMATTER ==================
function formatCurrency(value) {
    return new Intl.NumberFormat('ar-SA', {
        style: 'currency',
        currency: 'SAR'
    }).format(value);
}

// ================== TIME FORMATTER ==================
function formatTime(date) {
    return new Intl.DateTimeFormat('ar-SA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// ================== DEBOUNCE FUNCTION ==================
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// ================== THROTTLE FUNCTION ==================
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ================== COPY TO CLIPBOARD ==================
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('success', '✅ تم النسخ إلى الحافظة');
    }).catch(() => {
        showAlert('error', '❌ فشل النسخ');
    });
}

// Make code boxes copyable
document.querySelectorAll('.glow-box code').forEach(codeBox => {
    codeBox.style.cursor = 'pointer';
    codeBox.addEventListener('click', function() {
        copyToClipboard(this.textContent);
    });
});

// ================== NETWORK STATUS ==================
window.addEventListener('online', () => {
    showAlert('success', '✅ اتصال بالإنترنت استعاد');
});

window.addEventListener('offline', () => {
    showAlert('error', '❌ لا يوجد اتصال بالإنترنت');
});

// ================== PAGE VISIBILITY ==================
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('Page is hidden');
    } else {
        console.log('Page is visible');
        updatePrices(); // Update prices when tab becomes active
    }
});

// ================== INITIALIZATION ==================
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ تم تحميل منصة التداول بنجاح!');
    
    // Initialize tooltips
    document.querySelectorAll('[title]').forEach(el => {
        el.style.cursor = 'help';
    });
    
    // Set first tab as active
    if (document.querySelectorAll('.tab-btn').length > 0) {
        switchTab(0);
    }
    
    // Log system info
    console.log('System Info:', {
        userAgent: navigator.userAgent,
        language: navigator.language,
        online: navigator.onLine,
        cores: navigator.hardwareConcurrency
    });
});

// ================== ERROR HANDLING ==================
window.addEventListener('error', (e) => {
    console.error('Error:', e.error);
    showAlert('error', '❌ حدث خطأ: ' + e.message);
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled Promise Rejection:', e.reason);
    showAlert('error', '❌ خطأ غير متوقع');
});

// ================== EXPORT DATA FUNCTION ==================
function exportData(data, filename) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

// ================== IMPORT DATA FUNCTION ==================
function importData(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const data = JSON.parse(e.target.result);
            showAlert('success', '✅ تم استيراد البيانات بنجاح');
            console.log('Imported Data:', data);
        } catch (error) {
            showAlert('error', '❌ فشل استيراد البيانات');
        }
    };
    reader.readAsText(file);
}

// ================== SAMPLE DATA ==================
const sampleTradeData = {
    trades: [
        { id: 1, asset: 'Bitcoin', amount: 2.5, price: 42350, date: new Date() },
        { id: 2, asset: 'Ethereum', amount: 15, price: 2845, date: new Date() },
        { id: 3, asset: 'Gold', amount: 50, price: 2125, date: new Date() }
    ],
    portfolio: {
        balance: 25450.80,
        dayProfit: 1250.50,
        yearReturn: 18.5
    }
};

// Export sample data button functionality (if needed)
window.exportSampleData = () => {
    exportData(sampleTradeData, 'trades-data.json');
    showAlert('success', '✅ تم تصدير البيانات');
};

console.log('✅ جميع السكريبتات تم تحميلها بنجاح!');