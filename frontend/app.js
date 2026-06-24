const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000/api' 
    : 'https://<your-railway-domain>.up.railway.app/api'; // Replace with your actual Railway domain

// State
let selectedBudget = 'Medium';
let selectedCuisines = new Set();
let locationOptions = [];

// DOM Elements
const locationSelect = document.getElementById('locationSelect');
const budgetBtns = document.querySelectorAll('.budget-btn');
const cuisineContainer = document.getElementById('cuisineContainer');
const ratingInput = document.getElementById('ratingInput');
const ratingDisplay = document.getElementById('ratingDisplay');
const form = document.getElementById('preferenceForm');
const requirementsInput = document.getElementById('requirementsInput');

// States
const heroState = document.getElementById('heroState');
const loadingState = document.getElementById('loadingState');
const emptyState = document.getElementById('emptyState');
const resultsState = document.getElementById('resultsState');
const emptyTitle = document.getElementById('emptyTitle');
const emptyMessage = document.getElementById('emptyMessage');

// Output Elements
const summaryText = document.getElementById('summaryText');
const filterChips = document.getElementById('filterChips');
const resultsGrid = document.getElementById('resultsGrid');

// Event Listeners
budgetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        selectedBudget = btn.dataset.budget;
        budgetBtns.forEach(b => {
            b.className = 'budget-btn flex-1 py-2 rounded-xl border border-outline-variant/30 text-on-surface-variant hover:border-secondary hover:text-secondary transition-all';
        });
        btn.className = 'budget-btn flex-1 py-2 rounded-xl border-2 border-secondary bg-secondary/10 text-secondary transition-all';
    });
});

ratingInput.addEventListener('input', (e) => {
    ratingDisplay.textContent = parseFloat(e.target.value).toFixed(1);
});

// Initialization
async function init() {
    try {
        const [locRes, cuiRes] = await Promise.all([
            fetch(`${API_BASE}/metadata/locations`),
            fetch(`${API_BASE}/metadata/cuisines`)
        ]);
        
        if (locRes.ok) {
            const locations = await locRes.json();
            locationSelect.innerHTML = '<option value="">Select a location...</option>';
            locations.forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc;
                opt.textContent = loc;
                locationSelect.appendChild(opt);
            });
        }
        
        if (cuiRes.ok) {
            const cuisines = await cuiRes.json();
            cuisineContainer.innerHTML = '';
            
            // "Select Any" option
            const selectAny = document.createElement('span');
            selectAny.className = 'px-3 py-1 rounded-full border border-primary text-primary text-label-sm font-label-md bg-primary/10 cursor-pointer neon-glow select-none';
            selectAny.textContent = 'Select Any';
            selectAny.addEventListener('click', () => {
                selectedCuisines.clear();
                document.querySelectorAll('.cuisine-pill').forEach(pill => {
                    pill.className = 'cuisine-pill px-3 py-1 rounded-full border border-outline-variant/30 text-on-surface-variant text-label-sm font-label-md hover:border-primary hover:text-primary transition-all cursor-pointer select-none';
                });
                selectAny.className = 'px-3 py-1 rounded-full border border-primary text-primary text-label-sm font-label-md bg-primary/10 cursor-pointer neon-glow select-none';
            });
            cuisineContainer.appendChild(selectAny);

            cuisines.forEach(cui => {
                const span = document.createElement('span');
                span.className = 'cuisine-pill px-3 py-1 rounded-full border border-outline-variant/30 text-on-surface-variant text-label-sm font-label-md hover:border-primary hover:text-primary transition-all cursor-pointer select-none';
                span.textContent = cui;
                span.addEventListener('click', () => {
                    if (selectedCuisines.has(cui)) {
                        selectedCuisines.delete(cui);
                        span.className = 'cuisine-pill px-3 py-1 rounded-full border border-outline-variant/30 text-on-surface-variant text-label-sm font-label-md hover:border-primary hover:text-primary transition-all cursor-pointer select-none';
                        if (selectedCuisines.size === 0) {
                            selectAny.className = 'px-3 py-1 rounded-full border border-primary text-primary text-label-sm font-label-md bg-primary/10 cursor-pointer neon-glow select-none';
                        }
                    } else {
                        selectedCuisines.add(cui);
                        span.className = 'cuisine-pill px-3 py-1 rounded-full border border-primary text-primary text-label-sm font-label-md bg-primary/10 cursor-pointer neon-glow select-none';
                        selectAny.className = 'px-3 py-1 rounded-full border border-outline-variant/30 text-on-surface-variant text-label-sm font-label-md hover:border-primary hover:text-primary transition-all cursor-pointer select-none';
                    }
                });
                cuisineContainer.appendChild(span);
            });
        }
    } catch (e) {
        console.error("Failed to load metadata", e);
        cuisineContainer.innerHTML = '<span class="text-error">Failed to load API. Is backend running?</span>';
    }
}

function showState(state) {
    [heroState, loadingState, emptyState, resultsState].forEach(el => el.classList.add('hidden'));
    document.getElementById(`${state}State`).classList.remove('hidden');
}

// Form Submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!locationSelect.value) {
        alert("Please select a location.");
        return;
    }
    
    const payload = {
        location: locationSelect.value,
        budget_tier: selectedBudget,
        min_rating: parseFloat(ratingInput.value),
        preferred_cuisines: Array.from(selectedCuisines),
        specific_requirements: requirementsInput.value || null
    };

    // UI Updates
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon');
    const submitBtn = document.getElementById('submitBtn');
    
    btnText.textContent = 'Processing Palate...';
    btnIcon.textContent = 'progress_activity';
    btnIcon.classList.add('animate-spin');
    submitBtn.disabled = true;
    showState('loading');

    try {
        const response = await fetch(`${API_BASE}/recommendations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.detail || "Error fetching recommendations");
        
        if (data.recommendations.length === 0) {
            emptyTitle.textContent = "No perfect matches found";
            emptyMessage.textContent = data.summary || "Your filters are currently too narrow. Try broadening your location or budget.";
            showState('empty');
        } else {
            renderResults(data);
            showState('results');
        }
        
    } catch (err) {
        console.error(err);
        emptyTitle.textContent = "An error occurred";
        emptyMessage.textContent = err.message;
        showState('empty');
    } finally {
        btnText.textContent = 'Get Recommendations';
        btnIcon.textContent = 'bolt';
        btnIcon.classList.remove('animate-spin');
        submitBtn.disabled = false;
    }
});

function renderResults(data) {
    summaryText.innerHTML = data.summary;
    
    // Render Filters
    const filters = data.metadata.filters_applied;
    filterChips.innerHTML = '';
    
    if (filters.location) {
        filterChips.innerHTML += `<div class="px-5 py-2 rounded-full glass border border-primary text-primary text-label-md flex items-center whitespace-nowrap shadow-sm shadow-primary/20">${filters.location}</div>`;
    }
    if (filters.budget_tier) {
        filterChips.innerHTML += `<div class="px-5 py-2 rounded-full glass border border-outline-variant/30 text-on-surface-variant text-label-md flex items-center whitespace-nowrap">${filters.budget_tier} Tier</div>`;
    }
    if (filters.min_rating) {
        filterChips.innerHTML += `<div class="px-5 py-2 rounded-full glass border border-outline-variant/30 text-on-surface-variant text-label-md flex items-center whitespace-nowrap">${filters.min_rating}+ Rating</div>`;
    }
    if (filters.preferred_cuisines && filters.preferred_cuisines.length > 0) {
        filters.preferred_cuisines.forEach(c => {
             filterChips.innerHTML += `<div class="px-5 py-2 rounded-full glass border border-outline-variant/30 text-on-surface-variant text-label-md flex items-center whitespace-nowrap">${c}</div>`;
        });
    }
    filterChips.innerHTML += `<div class="ml-auto flex items-center gap-2 text-on-surface-variant text-label-sm"><span class="material-symbols-outlined">sort</span>Sort by: AI Rank</div>`;
    
    // Render Grid
    resultsGrid.innerHTML = '';
    data.recommendations.forEach((rec, idx) => {
        // Just use a nice placeholder gradient or abstract image since we don't have real images in the dataset
        const imageUrl = `https://source.unsplash.com/800x600/?restaurant,food,${encodeURIComponent(rec.cuisine.split(',')[0] || 'dining')}&sig=${rec.id}`;
        
        const cardHtml = `
        <div class="group card-hover-effect glass bg-surface-container/30 border border-outline-variant/20 rounded-[24px] overflow-hidden transition-all duration-500">
            <div class="relative h-64 overflow-hidden bg-surface-variant/50">
                <div class="absolute inset-0 flex items-center justify-center text-outline-variant">
                    <span class="material-symbols-outlined text-6xl">restaurant</span>
                </div>
                <!-- Real images are hard to source deterministically without API, using a stylish gradient fallback -->
                <div class="absolute inset-0 bg-gradient-to-br from-surface-variant to-background mix-blend-overlay"></div>
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                
                <div class="absolute top-4 left-4 bg-${idx === 0 ? 'primary text-on-primary' : 'surface-variant text-on-surface'} font-bold px-4 py-1.5 rounded-lg text-label-md shadow-xl">
                    #${rec.rank} Match
                </div>
                <div class="absolute bottom-4 left-6 right-6">
                    <div class="flex justify-between items-end">
                        <div>
                            <h4 class="font-headline-md text-headline-md text-white mb-1 truncate max-w-[200px]" title="${rec.name}">${rec.name}</h4>
                            <div class="flex items-center gap-2 text-on-surface-variant">
                                <span class="material-symbols-outlined text-primary text-lg" data-weight="fill">star</span>
                                <span class="text-white font-bold">${rec.rating}</span>
                                <span class="mx-1">•</span>
                                <span class="text-white/80 truncate max-w-[100px]" title="${rec.cuisine}">${rec.cuisine}</span>
                            </div>
                        </div>
                        <div class="text-right">
                            <p class="text-white/60 text-label-sm uppercase tracking-tighter">Cost for two</p>
                            <p class="text-primary font-bold text-headline-md">₹${rec.estimated_cost}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="p-6 space-y-4">
                <div class="bg-primary-container/10 border border-primary-container/20 rounded-2xl p-4 min-h-[100px]">
                    <div class="flex items-center gap-2 mb-2 text-primary font-bold text-label-md">
                        <span class="material-symbols-outlined text-[18px]">psychology</span>
                        AI Rationale
                    </div>
                    <p class="text-on-surface-variant text-body-md typewriter-text" style="white-space: normal; animation: none; border-right: none;">
                        ${rec.explanation}
                    </p>
                </div>
            </div>
        </div>
        `;
        resultsGrid.innerHTML += cardHtml;
    });
}

init();
