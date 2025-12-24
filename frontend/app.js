// Use dynamic API_BASE from config.js
const API_BASE = window.APP_CONFIG.API_BASE;

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    document.getElementById('nav-' + sectionId).classList.add('active');
}

async function refreshStats() {
    try {
        const res = await fetch(`${API_BASE}/stats`);
        const data = await res.json();
        document.getElementById('stat-total').textContent = data.total_calls;
        document.getElementById('stat-active').textContent = data.active_calls;
        document.getElementById('stat-completed').textContent = data.completed_calls;
        document.getElementById('stat-avg').textContent = Math.round(data.average_duration) + 's';
        document.getElementById('stat-minutes').textContent = Math.round(data.total_conversation_minutes);
    } catch (e) {
        alert('Error loading statistics: ' + e.message);
    }
}

async function loadCalls() {
    try {
        const res = await fetch(`${API_BASE}/calls`);
        const data = await res.json();
        const list = document.getElementById('calls-list');
        
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
        alert('Error loading calls: ' + e.message);
    }
}

async function searchTranscript() {
    const callId = document.getElementById('search-call').value;
    if (!callId) {
        alert('Please enter a call ID');
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}/calls/${callId}/transcript`);
        const data = await res.json();
        const display = document.getElementById('transcript-display');
        
        if (!data.transcript || data.transcript.length === 0) {
            display.innerHTML = '<p class="empty-state">No transcript found</p>';
            return;
        }
        
        const turns = JSON.parse(data.transcript) || [];
        display.innerHTML = turns.map(turn => `
            <div class="transcript-turn ${turn.role}">
                <div class="transcript-label">${turn.role === 'user' ? 'You' : 'Assistant'}:</div>
                <div>${turn.text}</div>
            </div>
        `).join('');
    } catch (e) {
        alert('Error loading transcript: ' + e.message);
    }
}

async function createCall() {
    const userId = document.getElementById('user-id').value;
    const profile = document.getElementById('voice-profile').value;
    
    if (!userId) {
        alert('Please enter a user ID');
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}/calls`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: userId, voice_profile: profile})
        });
        const data = await res.json();
        const msg = document.getElementById('create-response');
        msg.className = 'response-message success';
        msg.textContent = `Call created! ID: ${data.call_id}`;
    } catch (e) {
        const msg = document.getElementById('create-response');
        msg.className = 'response-message error';
        msg.textContent = 'Error: ' + e.message;
    }
}

window.addEventListener('load', () => {
    refreshStats();
    setInterval(refreshStats, 5000);
});
