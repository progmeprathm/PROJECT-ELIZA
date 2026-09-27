document.addEventListener('DOMContentLoaded', () => {
    // Check local storage for settings
    const storedOpenai = localStorage.getItem('eliza_studio_openai');
    const storedGroq = localStorage.getItem('eliza_studio_groq');
    const storedForceLocal = localStorage.getItem('eliza_studio_force_local');

    if (storedOpenai) document.getElementById('set-openai').value = storedOpenai;
    if (storedGroq) document.getElementById('set-groq').value = storedGroq;
    if (storedForceLocal === 'true') document.getElementById('set-local-mode').checked = true;

    // Fetch Interceptor for injecting settings into Headers
    const originalFetch = window.fetch;
    window.fetch = async function(...args) {
        let [resource, config] = args;
        
        if (typeof resource === 'string' && resource.startsWith('/api/')) {
            config = config || {};
            config.headers = config.headers || {};
            
            const openai = localStorage.getItem('eliza_studio_openai');
            const groq = localStorage.getItem('eliza_studio_groq');
            const forceLocal = localStorage.getItem('eliza_studio_force_local');

            if (openai) config.headers['X-OpenAI-Key'] = openai;
            if (groq) config.headers['X-Groq-Key'] = groq;
            if (forceLocal === 'true') config.headers['X-Force-Local'] = 'true';
            config.headers['X-User-ID'] = 'studio-operator';
        }
        
        return originalFetch(resource, config);
    };

    initObservability();
});

// Studio State Engine
const StudioState = {
    runtime_id: "sys",
    goals: [],
    agents: [],
    memory_tiers: [],
    timeline: []
};

async function initObservability() {
    try {
        // 1. Fetch Canonical State Snapshot
        const res = await fetch('/api/state');
        if (res.ok) {
            const data = await res.json();
            StudioState.runtime_id = data.runtime_id;
            StudioState.goals = data.goals || [];
            StudioState.agents = data.agents || [];
            StudioState.memory_tiers = data.memory_tiers || [];
            renderState();
        }
    } catch (e) {
        console.error("Failed to load initial state", e);
    }

    // 2. Connect EventSource for Live Updates
    const eventSource = new EventSource('/api/stream');
    
    eventSource.onmessage = function(e) {
        // Catch-all or unnamed events
    };

    // Example explicit event handlers
    const handleEvent = (e) => {
        const payload = JSON.parse(e.data);
        const log = document.getElementById('activity-log');
        if (!log) return;
        const entry = document.createElement('div');
        entry.innerHTML = `<span class="text-blue-400">[${e.type}]</span> <span class="text-gray-400">${payload.source || 'Sys'}:</span> ${JSON.stringify(payload.payload)}`;
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
    };

    eventSource.addEventListener('AgentStateChanged', handleEvent);
    eventSource.addEventListener('TaskDelegated', handleEvent);
    eventSource.addEventListener('ModelRequested', handleEvent);
    eventSource.addEventListener('ModelResponded', handleEvent);
    eventSource.addEventListener('ModelRouterFailover', handleEvent);
    eventSource.addEventListener('GoalTreeUpdated', handleEvent);

    eventSource.onerror = function(e) {
        console.error("SSE connection lost. Reconnecting...");
        // Browser automatically reconnects EventSource
    };
}

function renderState() {
    // Re-render UI components based on StudioState
    console.log("State Updated:", StudioState);
}

function toggleSettings() {
    const modal = document.getElementById('modal-settings');
    if (modal.classList.contains('hidden')) {
        modal.classList.remove('hidden');
        // small delay for transition
        setTimeout(() => {
            modal.classList.remove('opacity-0');
        }, 10);
    } else {
        modal.classList.add('opacity-0');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
    }
}

function saveSettings() {
    const openai = document.getElementById('set-openai').value;
    const groq = document.getElementById('set-groq').value;
    const forceLocal = document.getElementById('set-local-mode').checked;

    localStorage.setItem('eliza_studio_openai', openai);
    localStorage.setItem('eliza_studio_groq', groq);
    localStorage.setItem('eliza_studio_force_local', forceLocal);

    // Flash success button briefly
    const btn = event.target;
    const oldText = btn.innerText;
    btn.innerText = "Settings Saved!";
    btn.classList.add("bg-success", "hover:bg-green-600");
    btn.classList.remove("bg-primary", "hover:bg-blue-600");
    
    setTimeout(() => {
        btn.innerText = oldText;
        btn.classList.remove("bg-success", "hover:bg-green-600");
        btn.classList.add("bg-primary", "hover:bg-blue-600");
        toggleSettings();
    }, 1000);
}

// Simulated Input handler
document.querySelector('input[type="text"]').addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && this.value.trim() !== '') {
        const log = document.getElementById('activity-log');
        
        const newGoal = document.createElement('div');
        newGoal.innerHTML = `<span class="text-white">> MISSION RECEIVED:</span> ${this.value}`;
        log.appendChild(newGoal);
        
        const dispatch = document.createElement('div');
        dispatch.innerHTML = `> CoordinatorAgent routing new goal...`;
        log.appendChild(dispatch);
        
        this.value = '';
        log.scrollTop = log.scrollHeight;
    }
});
