// Use dynamic API_BASE from config.js
const API_BASE = window.APP_CONFIG.API_BASE;

// Track backend availability
let backendAvailable = false;

// Demo/mock data for when backend is not available
const DEMO_STATS = {
    total_calls: 0,
    active_calls: 0,
    completed_calls: 0,
    average_duration: 0,
    total_conversation_minutes: 0
};

/**
 * Safely fetch and parse JSON response
 * Handles cases where response is not JSON (e.g., HTML error pages)
 */
async function safeFetch(url, options = {}) {
    const response = await fetch(url, options);
    
    // Check if response is OK
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    // Check content-type to ensure we're getting JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Backend returned non-JSON response. Is the backend server running?');
    }
    
    return response.json();
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    document.getElementById('nav-' + sectionId).classList.add('active');
}

/**
 * Display error message inline instead of using alert()
 */
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<p class="error-message" style="color: #dc3545; padding: 10px; background: #f8d7da; border-radius: 5px; margin: 10px 0;">${message}</p>`;
    }
}

async function refreshStats() {
    // If backend is not available, use demo data without trying to fetch
    if (!backendAvailable) {
        document.getElementById('stat-total').textContent = DEMO_STATS.total_calls;
        document.getElementById('stat-active').textContent = DEMO_STATS.active_calls;
        document.getElementById('stat-completed').textContent = DEMO_STATS.completed_calls;
        document.getElementById('stat-avg').textContent = Math.round(DEMO_STATS.average_duration) + 's';
        document.getElementById('stat-minutes').textContent = Math.round(DEMO_STATS.total_conversation_minutes);
        return;
    }
    
    try {
        const data = await safeFetch(`${API_BASE}/stats`);
        document.getElementById('stat-total').textContent = data.total_calls;
        document.getElementById('stat-active').textContent = data.active_calls;
        document.getElementById('stat-completed').textContent = data.completed_calls;
        document.getElementById('stat-avg').textContent = Math.round(data.average_duration) + 's';
        document.getElementById('stat-minutes').textContent = Math.round(data.total_conversation_minutes);
    } catch (e) {
        // Silently fail if backend is not available - the warning banner already shows
        console.error('Error loading statistics:', e.message);
    }
}

async function loadCalls() {
    const list = document.getElementById('calls-list');
    
    // If backend is not available, show appropriate message
    if (!backendAvailable) {
        list.innerHTML = '<p class="empty-state">Backend not connected. Please configure your backend server to view calls.</p>';
        return;
    }
    
    try {
        const data = await safeFetch(`${API_BASE}/calls`);
        
        if (!data.calls || data.calls.length === 0) {
            list.innerHTML = '<p class="empty-state">No active calls</p>';
            return;
        }
        
        list.innerHTML = data.calls.map(call => `
            <div class="call-item">
                <div class="call-id">ID: ${call.call_id}</div>
                <div>User: ${call.user_id}</div>
                <div>Profile: ${call.voice_profile}</div>
                <span class="call-status ${call.status === 'active' ? 'active' : 'completed'}">${call.status}</span>
            </div>
        `).join('');
    } catch (e) {
        console.error('Error loading calls:', e.message);
        list.innerHTML = `<p class="error-message" style="color: #dc3545; padding: 10px; background: #f8d7da; border-radius: 5px;">Error loading calls: ${e.message}</p>`;
    }
}

async function searchTranscript() {
    const callId = document.getElementById('search-call').value;
    const display = document.getElementById('transcript-display');
    
    if (!callId) {
        display.innerHTML = '<p class="error-message" style="color: #dc3545; padding: 10px; background: #f8d7da; border-radius: 5px;">Please enter a call ID</p>';
        return;
    }
    
    // If backend is not available, show appropriate message
    if (!backendAvailable) {
        display.innerHTML = '<p class="empty-state">Backend not connected. Please configure your backend server to search transcripts.</p>';
        return;
    }
    
    try {
        const data = await safeFetch(`${API_BASE}/calls/${callId}/transcript`);
        
        if (!data.transcript || data.transcript.length === 0) {
            display.innerHTML = '<p class="empty-state">No transcript found</p>';
            return;
        }
        
        const turns = typeof data.transcript === 'string' ? JSON.parse(data.transcript) : data.transcript;
        if (!turns || turns.length === 0) {
            display.innerHTML = '<p class="empty-state">No transcript found</p>';
            return;
        }
        
        display.innerHTML = turns.map(turn => `
            <div class="transcript-turn ${turn.role}">
                <div class="transcript-label">${turn.role === 'user' ? 'You' : 'Assistant'}:</div>
                <div>${turn.text}</div>
            </div>
        `).join('');
    } catch (e) {
        console.error('Error loading transcript:', e.message);
        display.innerHTML = `<p class="error-message" style="color: #dc3545; padding: 10px; background: #f8d7da; border-radius: 5px;">Error loading transcript: ${e.message}</p>`;
    }
}

async function createCall() {
    const userId = document.getElementById('user-id').value;
    const profile = document.getElementById('voice-profile').value;
    const msg = document.getElementById('create-response');
    
    if (!userId) {
        msg.className = 'response-message error';
        msg.textContent = 'Please enter a user ID';
        return;
    }
    
    // If backend is not available, show appropriate message
    if (!backendAvailable) {
        msg.className = 'response-message error';
        msg.textContent = 'Backend not connected. Please configure your backend server to create calls.';
        return;
    }
    
    try {
        const data = await safeFetch(`${API_BASE}/calls`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: userId, voice_profile: profile})
        });
        msg.className = 'response-message success';
        msg.textContent = `Call created! ID: ${data.call_id}`;
    } catch (e) {
        console.error('Error creating call:', e.message);
        msg.className = 'response-message error';
        msg.textContent = 'Error: ' + e.message;
    }
}

window.addEventListener('load', async () => {
    // Check backend connectivity first
    await checkBackendConnection();
    
    // Then load initial stats
    refreshStats();
    
    // Set up periodic refresh only if backend is available
    setInterval(refreshStats, 5000);
});

async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE}/health`, { 
            mode: 'cors'
        });
        
        // Check if response is OK and JSON
        if (response.ok) {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                if (data.status === 'healthy') {
                    // Backend is accessible and healthy
                    backendAvailable = true;
                    document.getElementById('backend-warning').style.display = 'none';
                    console.log('Backend connected successfully');
                    return;
                }
            }
        }
        throw new Error('Backend health check failed');
    } catch (e) {
        // Backend is not accessible, show warning
        backendAvailable = false;
        console.warn('Backend connection failed:', e.message);
        document.getElementById('backend-warning').style.display = 'block';
    }
}