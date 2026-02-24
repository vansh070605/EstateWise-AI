const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:5000'
    : '/api'; // In Vercel, everything under /api routes to our Python function

let basePriceUSD = 0;
const exchangeRates = {
    'USD': { rate: 1, symbol: '$', locale: 'en-US' },
    'INR': { rate: 83.50, symbol: '₹', locale: 'en-IN' },
    'EUR': { rate: 0.92, symbol: '€', locale: 'de-DE' },
    'GBP': { rate: 0.78, symbol: '£', locale: 'en-GB' }
};

function showView(viewId) {
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });

    const target = document.getElementById(viewId + '-view');
    if (target) {
        target.classList.add('active');
        window.scrollTo(0, 0);
    }
}

function changeCurrency() {
    updateDisplayedPrice();
}

function updateDisplayedPrice() {
    const currency = document.getElementById('currency-selector').value;
    const config = exchangeRates[currency];
    const convertedPrice = basePriceUSD * config.rate;

    const formattedPrice = new Intl.NumberFormat(config.locale, {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(convertedPrice);

    const priceDisplay = document.getElementById('predicted-price');
    if (priceDisplay) {
        priceDisplay.innerText = formattedPrice;
    }
}

async function predict(type) {
    let payload = {};
    let endpoint = '';

    if (type === 'simple') {
        const area = document.getElementById('gen-area').value;
        const bedrooms = document.getElementById('gen-bed').value;
        const age = document.getElementById('gen-age').value;

        if (!area || !bedrooms || !age) {
            alert("Please provide all housing specs for analysis.");
            return;
        }

        payload = { area, bedrooms, age };
        endpoint = '/predict_simple';
    } else {
        const area = document.getElementById('town-area').value;
        const town = document.getElementById('town-name').value;

        if (!area) {
            alert("Please provide the property area.");
            return;
        }

        payload = { area, town };
        endpoint = '/predict_town';
    }

    const btn = document.querySelector('.view.active .predict-btn');
    const originalText = btn.innerText;
    btn.innerText = 'Analyzing Market...';
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Prediction failed');

        const data = await response.json();

        // Store base price in USD
        basePriceUSD = data.prediction;

        // Update display with current currency
        updateDisplayedPrice();

        showView('prediction');
    } catch (error) {
        console.error('Error:', error);
        alert("The intelligence engine is taking a break. Please ensure the backend server is running.");
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

window.onload = () => {
    showView('welcome');
};
