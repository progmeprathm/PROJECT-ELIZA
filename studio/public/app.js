/**
 * Layer 1: Human E.L.I.Z.A. Frontend Logic
 * Replaces the technical OS control deck with a personal intelligence interface.
 */

let state = {
  userName: 'Prathmesh',
  behavior: 'Just answer me',
  activeProjects: [],
  currentProjectId: null
};

document.addEventListener('DOMContentLoaded', () => {
  initAppState();
  initOnboarding();
  initHome();
  initWorkspace();
  
  // Background polling for OS telemetry (only for Layer 2 metrics and Goal state)
  setInterval(fetchBackendState, 3000);
});

// --- GLOBAL FETCH WRAPPER ---
// Inject user ID, API keys, and Offline Mode flag from localStorage
const originalFetch = window.fetch;
window.fetch = async function() {
    let [resource, config] = arguments;
    if (!config) config = {};
    if (!config.headers) config.headers = {};
    
    config.headers['X-User-ID'] = localStorage.getItem('eliza_user_id') || 'default';
    const oai = localStorage.getItem('eliza_key_openai');
    if (oai) config.headers['X-OpenAI-Key'] = oai;
    const groq = localStorage.getItem('eliza_key_groq');
    if (groq) config.headers['X-Groq-Key'] = groq;
    
    const isLocal = localStorage.getItem('eliza_force_local');
    if (isLocal === 'true') {
        config.headers['X-Force-Local'] = 'true';
    }
    
    return originalFetch(resource, config);
};


/* =========================================================
   ROUTING & STATE
   ========================================================= */
async function initAppState() {
  const savedName = localStorage.getItem('eliza_human_name');
  if (savedName) {
    state.userName = savedName;
    document.getElementById('lbl-greeting-name').innerText = savedName;
    
    await fetchBackendState();
    navigateTo('home');
  } else {
    navigateTo('onboarding');
  }
}

function navigateTo(screenId) {
  document.querySelectorAll('.screen').forEach(s => {
    s.classList.add('hidden');
    s.style.opacity = '0';
  });
  
  const target = document.getElementById(`screen-${screenId}`);
  if (target) {
    target.classList.remove('hidden');
    setTimeout(() => {
      target.style.opacity = '1';
    }, 50);
  }

  if (screenId === 'home') {
    renderHomeProjects();
  }
}

async function fetchBackendState() {
  if (!localStorage.getItem('eliza_human_name')) return;
  
  try {
    const goalsRes = await fetch('/api/goals');
    const goalsData = await goalsRes.json();
    state.activeProjects = goalsData.goals || [];
    
    if (!document.getElementById('screen-home').classList.contains('hidden')) {
      renderHomeProjects();
    }
    
    if (!document.getElementById('screen-workspace').classList.contains('hidden') && state.currentProjectId) {
      updateWorkspacePlan();
    }
    
    // Also fetch Layer 2 metrics if overlay is open
    const overlay = document.getElementById('advanced-overlay');
    if (!overlay.classList.contains('hidden')) {
      const dashRes = await fetch('/api/dashboard');
      const dashData = await dashRes.json();
      renderAdvancedMetrics(dashData);
    }
  } catch (e) {
    console.error("Backend fetch error:", e);
  }
}

/* =========================================================
   ONBOARDING
   ========================================================= */
function initOnboarding() {
  const btns = document.querySelectorAll('.behavior-btn');
  btns.forEach(b => {
    b.addEventListener('click', () => {
      btns.forEach(btn => btn.classList.remove('border-primary', 'ring-2', 'ring-primary/20'));
      b.classList.add('border-primary', 'ring-2', 'ring-primary/20');
      state.behavior = b.getAttribute('data-behavior');
    });
  });

  document.getElementById('btn-finish-onboarding').addEventListener('click', () => {
    const name = document.getElementById('inp-user-name').value.trim() || 'Guest';
    localStorage.setItem('eliza_human_name', name);
    localStorage.setItem('eliza_behavior', state.behavior);
    
    const isLocal = document.getElementById('chk-local-mode').checked;
    localStorage.setItem('eliza_force_local', isLocal ? 'true' : 'false');
    
    initAppState();
  });
}

/* =========================================================
   HOME (TODAY) COMMAND CENTER
   ========================================================= */
function initHome() {
  const omniInput = document.getElementById('inp-omnibar');
  const btnSend = document.getElementById('btn-omnibar-send');

  const dispatchFromHome = async () => {
    const text = omniInput.value.trim();
    if(!text) return;
    
    // Create goal in backend
    try {
      await fetch('/api/goals/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal: text, priority: 10 })
      });
      omniInput.value = '';
      
      // Force fetch to get new ID
      await fetchBackendState();
      
      if(state.activeProjects.length > 0) {
        const newest = state.activeProjects[state.activeProjects.length - 1];
        openWorkspace(newest.id);
        
        // Push initial chat
        addChatMessage(text, 'user');
        sendChatToBackend(text);
      }
    } catch (e) {
      console.error(e);
    }
  };

  btnSend.addEventListener('click', dispatchFromHome);
  omniInput.addEventListener('keyup', (e) => {
    if(e.key === 'Enter') dispatchFromHome();
  });
}

function renderHomeProjects() {
  const container = document.getElementById('home-projects-list');
  if (state.activeProjects.length === 0 || state.activeProjects[0].id === 'sys') {
    container.innerHTML = `<p class="text-secondary text-sm">No active projects. Ask E.L.I.Z.A. to start something.</p>`;
    return;
  }

  container.innerHTML = state.activeProjects.map(p => `
    <div onclick="openWorkspace('${p.id}')" class="p-4 rounded-xl border border-outline bg-surface/50 hover:bg-surface cursor-pointer transition-colors flex justify-between items-center group">
      <div class="flex items-center gap-4">
        <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
          <span class="material-symbols-outlined">folder</span>
        </div>
        <div>
          <h4 class="font-medium">${p.title || p.description}</h4>
          <p class="text-sm text-secondary">${(p.status || 'Active').toLowerCase()}</p>
        </div>
      </div>
      <span class="material-symbols-outlined text-secondary opacity-0 group-hover:opacity-100 transition-opacity">arrow_forward</span>
    </div>
  `).join('');
}


/* =========================================================
   WORKSPACE & CHAT
   ========================================================= */
function openWorkspace(projectId) {
  state.currentProjectId = projectId;
  const p = state.activeProjects.find(x => x.id === projectId);
  if(p) {
    document.getElementById('ws-project-title').innerText = p.title || p.description;
    document.getElementById('ws-mobile-title').innerText = p.title || p.description;
  }
  updateWorkspacePlan();
  navigateTo('workspace');
}

function updateWorkspacePlan() {
  if(!state.currentProjectId) return;
  const p = state.activeProjects.find(x => x.id === state.currentProjectId);
  if(!p) return;
  
  document.getElementById('ws-project-status').innerText = `${Math.round((p.progress || 0.1) * 100)}% Complete`;
  
  const planContainer = document.getElementById('ws-project-plan');
  const subs = p.subgoals || [{name: 'Analyzing request...', status: 'active'}];
  
  planContainer.innerHTML = subs.map(sub => {
    let icon = 'circle';
    let iconClass = 'text-outline';
    let textClass = 'text-secondary';
    
    if(sub.status === 'done') {
      icon = 'check_circle';
      iconClass = 'text-green-500';
    } else if (sub.status === 'active') {
      icon = 'radio_button_checked';
      iconClass = 'text-primary animate-pulse';
      textClass = 'text-on-surface font-medium';
    }
    
    return `
      <div class="flex items-start gap-3">
        <span class="material-symbols-outlined text-sm mt-0.5 ${iconClass}">${icon}</span>
        <span class="text-sm ${textClass}">${sub.description || sub.name}</span>
      </div>
    `;
  }).join('');
}

function initWorkspace() {
  const input = document.getElementById('inp-chat-msg');
  const btn = document.getElementById('btn-chat-send');
  
  const submitChat = () => {
    const text = input.value.trim();
    if(!text) return;
    addChatMessage(text, 'user');
    input.value = '';
    sendChatToBackend(text);
  };
  
  btn.addEventListener('click', submitChat);
  input.addEventListener('keyup', (e) => {
    if(e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitChat();
    }
  });
}

function addChatMessage(text, sender, traceData = null) {
  const container = document.getElementById('chat-history');
  
  const formatMarkdown = (str) => {
    return str.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
  };
  
  let html = '';
  if (sender === 'user') {
    html = `
      <div class="msg-user">
        ${formatMarkdown(text)}
      </div>
    `;
  } else {
    html = `
      <div class="msg-assistant relative group">
        ${formatMarkdown(text)}
        ${traceData ? `
          <div class="mt-3 pt-3 border-t border-outline flex justify-end">
            <button onclick='showWhyModal(${JSON.stringify(traceData).replace(/'/g, "&apos;")})' class="text-xs font-medium text-secondary hover:text-primary transition-colors flex items-center gap-1 opacity-0 group-hover:opacity-100">
              <span class="material-symbols-outlined text-[14px]">psychology</span> Why?
            </button>
          </div>
        ` : ''}
      </div>
    `;
  }
  
  container.insertAdjacentHTML('beforeend', html);
  container.scrollTop = container.scrollHeight;
}

async function sendChatToBackend(text) {
  document.getElementById('chat-typing-indicator').classList.remove('hidden');
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    
    document.getElementById('chat-typing-indicator').classList.add('hidden');
    
    if(data.chat) {
      addChatMessage(data.chat.response, 'assistant', data.chat.trace);
    }
  } catch (e) {
    document.getElementById('chat-typing-indicator').classList.add('hidden');
    addChatMessage("I'm sorry, I encountered a connection error.", 'assistant');
  }
}

/* =========================================================
   LAYER 2 & EXPLAINABILITY
   ========================================================= */
window.toggleAdvancedMode = function() {
  const overlay = document.getElementById('advanced-overlay');
  if (overlay.classList.contains('hidden')) {
    overlay.classList.remove('hidden');
    setTimeout(() => overlay.style.opacity = '1', 10);
    fetchBackendState();
  } else {
    overlay.style.opacity = '0';
    setTimeout(() => overlay.classList.add('hidden'), 300);
  }
};

window.showWhyModal = function(traceObj) {
  const modal = document.getElementById('modal-why');
  const content = document.getElementById('why-content');
  
  content.innerHTML = `
    <div>
      <h3 class="text-sm font-bold text-secondary uppercase tracking-wider mb-2">My Understanding</h3>
      <p class="text-base">${traceObj.goal_description || 'Synthesize user intent'}</p>
    </div>
    
    <div>
      <h3 class="text-sm font-bold text-secondary uppercase tracking-wider mb-2">Evidence Considered</h3>
      <ul class="list-disc pl-5 text-sm space-y-1">
        ${(traceObj.evidence || []).map(e => `<li>${e}</li>`).join('') || '<li>General world knowledge</li>'}
      </ul>
    </div>
    
    <div>
      <h3 class="text-sm font-bold text-secondary uppercase tracking-wider mb-2">Assumptions</h3>
      <ul class="list-disc pl-5 text-sm space-y-1 text-yellow-600 dark:text-yellow-400">
        ${(traceObj.assumptions || []).map(a => `<li>${a}</li>`).join('') || '<li>No major assumptions made.</li>'}
      </ul>
    </div>
  `;
  
  modal.classList.remove('hidden');
  modal.classList.add('flex');
};

function renderAdvancedMetrics(dashData) {
  document.getElementById('adv-telemetry').innerHTML = `
    <div>Scheduler Queue: ${dashData.scheduler_queue_depth}</div>
    <div>Uptime: ${dashData.uptime_seconds}s</div>
    <div>CPU Bound Usage: ${dashData.cpu_usage_pct}%</div>
    <div>Mem Bound: ${dashData.memory_usage_mb} objects</div>
    <div>Reasoning Stage: ${dashData.reasoning_stage}</div>
  `;
}

/* =========================================================
   SETTINGS MODAL LOGIC
   ========================================================= */
window.toggleSettings = function() {
  const modal = document.getElementById('modal-settings');
  if (modal.classList.contains('hidden')) {
    // Populate with current values
    document.getElementById('set-name').value = localStorage.getItem('eliza_human_name') || '';
    document.getElementById('set-openai').value = localStorage.getItem('eliza_key_openai') || '';
    document.getElementById('set-groq').value = localStorage.getItem('eliza_key_groq') || '';
    document.getElementById('set-local-mode').checked = localStorage.getItem('eliza_force_local') === 'true';
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    setTimeout(() => modal.style.opacity = '1', 10);
  } else {
    modal.style.opacity = '0';
    setTimeout(() => {
      modal.classList.remove('flex');
      modal.classList.add('hidden');
    }, 300);
  }
};

window.saveSettings = function() {
  const name = document.getElementById('set-name').value.trim();
  const oai = document.getElementById('set-openai').value.trim();
  const groq = document.getElementById('set-groq').value.trim();
  const isLocal = document.getElementById('set-local-mode').checked;
  
  if (name) localStorage.setItem('eliza_human_name', name);
  if (oai) localStorage.setItem('eliza_key_openai', oai);
  if (groq) localStorage.setItem('eliza_key_groq', groq);
  localStorage.setItem('eliza_force_local', isLocal ? 'true' : 'false');
  
  if (name) document.getElementById('lbl-greeting-name').innerText = name;
  
  window.toggleSettings();
};
