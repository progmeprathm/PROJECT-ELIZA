/**
 * ELIZA Goal-Centric Frontend SPA Logic (Fully Connected to ECOS Backend)
 */

let state = {
  persona: null,
  activeGoals: [],
  currentGoalId: null,
  dashboardStats: null
};

document.addEventListener('DOMContentLoaded', () => {
  initAppState();
  initOnboarding();
  initModals();
  initCompanionChat();
  
  // Periodic UI Updates
  setInterval(fetchBackendState, 3000);
});

// GLOBAL FETCH OVERRIDE FOR MULTI-TENANT
const originalFetch = window.fetch;
window.fetch = async function() {
    let [resource, config] = arguments;
    
    // Inject headers
    if (!config) config = {};
    if (!config.headers) config.headers = {};
    
    config.headers['X-User-ID'] = localStorage.getItem('eliza_user_id') || 'default-user';
    
    const oai = localStorage.getItem('eliza_key_openai');
    if (oai) config.headers['X-OpenAI-Key'] = oai;
    
    const groq = localStorage.getItem('eliza_key_groq');
    if (groq) config.headers['X-Groq-Key'] = groq;
    
    return originalFetch(resource, config);
};


/* =========================================================
   1. STATE MANAGEMENT & ROUTING
   ========================================================= */
async function fetchBackendState() {
  if (!state.persona) return; // Only fetch if onboarded
  
  try {
    const goalsRes = await fetch('/api/goals');
    const goalsData = await goalsRes.json();
    state.activeGoals = goalsData.goals;
    
    const dashRes = await fetch('/api/dashboard');
    const dashData = await dashRes.json();
    state.dashboardStats = dashData;
    
    // Re-render current screen
    const homeScreen = document.getElementById('screen-home');
    if (!homeScreen.classList.contains('hidden')) {
      renderHomeDashboard();
    }
    
    const wsScreen = document.getElementById('screen-workspace');
    if (!wsScreen.classList.contains('hidden') && state.currentGoalId) {
      openWorkspace(state.currentGoalId);
    }
  } catch (err) {
    console.error("Failed to fetch live backend state:", err);
  }
}

async function initAppState() {
  const savedPersona = localStorage.getItem('eliza_persona');
  
  if (savedPersona) {
    state.persona = savedPersona;
    document.getElementById('lbl-persona').innerText = savedPersona;
    document.getElementById('lbl-home-persona').innerText = `Persona: ${savedPersona}`;
    
    await fetchBackendState();
    navigateTo('home');
  } else {
    navigateTo('onboarding');
  }

  // Home Button (Logo)
  document.getElementById('btn-go-home').addEventListener('click', () => {
    if (state.persona) navigateTo('home');
  });

  // Reset Button
  document.getElementById('btn-reset').addEventListener('click', () => {
    localStorage.removeItem('eliza_persona');
    state.persona = null;
    state.activeGoals = [];
    navigateTo('onboarding');
  });
}

function navigateTo(screenName) {
  // Hide all screens
  document.getElementById('screen-onboarding').classList.add('hidden');
  document.getElementById('screen-home').classList.add('hidden');
  document.getElementById('screen-workspace').classList.add('hidden');
  
  // Show target
  const target = document.getElementById(`screen-${screenName}`);
  if (target) {
    target.classList.remove('hidden');
  }

  // Trigger screen-specific initializers
  if (screenName === 'home') {
    renderHomeDashboard();
  }
}

/* =========================================================
   2. ONBOARDING (SCREEN A)
   ========================================================= */
function initOnboarding() {
  const cards = document.querySelectorAll('.persona-card');
  cards.forEach(card => {
    card.addEventListener('click', async () => {
      
      // Save Multi-Tenant Credentials
      const uid = document.getElementById('inp-auth-user').value.trim();
      const oai = document.getElementById('inp-key-openai').value.trim();
      const groq = document.getElementById('inp-key-groq').value.trim();
      
      if(uid) localStorage.setItem('eliza_user_id', uid);
      if(oai) localStorage.setItem('eliza_key_openai', oai);
      if(groq) localStorage.setItem('eliza_key_groq', groq);

      const selected = card.getAttribute('data-persona');
      localStorage.setItem('eliza_persona', selected);
      
      try {
        // Kickstart with a welcome message to the shell/chat
        await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: "Hello ELIZA, I am booting the system as a " + selected, assistant: 'architect' })
        });
      } catch (err) {
        console.warn("Boot chat failed (e.g. LLM rate limit), continuing boot sequence:", err);
      }
      
      initAppState(); // Re-evaluate and route to Home
    });
  });
}

/* =========================================================
   3. HOME DASHBOARD (SCREEN B)
   ========================================================= */
function renderHomeDashboard() {
  const container = document.getElementById('home-active-goals');
  
  if (!state.activeGoals || state.activeGoals.length === 0 || state.activeGoals[0].id === 'sys') {
    container.innerHTML = `
      <div class="p-6 rounded-xl bg-surface border text-center shadow-sm">
        <p class="text-secondary font-mono text-sm mb-4">SYSTEM IDLE. AWAITING INSTRUCTION DISPATCH.</p>
        <button class="px-4 py-2 bg-primary text-white rounded font-mono text-sm hover:shadow-glow transition-all" onclick="document.getElementById('modal-create-goal').show()">ASSIGN GOAL TO E.L.I.Z.A.</button>
      </div>
    `;
    
    // Update live dashboard stats as well
    if (state.dashboardStats) {
      updateDashboardStatsUI();
    }
    return;
  }

  container.innerHTML = state.activeGoals.map(g => `
    <div class="p-5 rounded-lg bg-surface border hover:border-primary hover:shadow-glow cursor-pointer transition-all" onclick="openWorkspace('${g.id}')">
      <div class="flex justify-between items-start mb-3">
        <div>
          <h3 class="font-bold text-sm text-on-surface mb-1">${g.description || g.title}</h3>
          <span class="text-[10px] font-mono text-secondary tracking-wider">${(g.status || 'ACTIVE').toUpperCase()} | PRI: ${g.priority}</span>
        </div>
        <span class="text-lg font-bold font-mono text-cyan">${Math.round((g.progress || 0.1) * 100)}%</span>
      </div>
      <div class="w-full bg-background h-1.5 rounded-full overflow-hidden border">
        <div class="bg-gradient-to-r from-primary to-cyan h-full" style="width: ${(g.progress || 0.1) * 100}%"></div>
      </div>
    </div>
  `).join('');
  
  if (state.dashboardStats) {
    updateDashboardStatsUI();
  }
}

function updateDashboardStatsUI() {
  const ds = state.dashboardStats;
  const streamHtml = `
    <div class="code-block flex-col gap-2">
      <div class="flex justify-between text-xs text-secondary border-b border-outline-variant pb-2 mb-2">
        <span>[ECOS] STREAM</span>
        <span class="animate-pulse text-primary">● LIVE</span>
      </div>
      <div class="flex items-center gap-3 font-mono text-xs">
        <span class="text-tertiary">sys></span>
        <span class="text-on-surface">Scheduler Queue: ${ds.scheduler_queue_depth} Tasks</span>
      </div>
      <div class="flex items-center gap-3 font-mono text-xs">
        <span class="text-tertiary">sys></span>
        <span class="text-cyan">Memory Allocations: ${ds.memory_usage_mb} objects</span>
      </div>
      <div class="flex items-center gap-3 font-mono text-xs">
        <span class="text-tertiary">sys></span>
        <span class="text-secondary">Active Subroutines: ${ds.active_processes.length}</span>
      </div>
    </div>
  `;
  
  // Inject stream if element exists
  const streamSection = document.querySelectorAll('#screen-home section')[1];
  if (streamSection && streamSection.querySelector('.code-block')) {
    streamSection.querySelector('.code-block').outerHTML = streamHtml;
  }
}

/* =========================================================
   4. WORKSPACE (SCREEN C)
   ========================================================= */
function openWorkspace(goalId) {
  state.currentGoalId = goalId;
  const goal = state.activeGoals.find(g => g.id === goalId);
  if (!goal) return;

  // Populate Workspace DOM
  document.getElementById('ws-goal-title').innerText = goal.description || goal.title;
  document.getElementById('ws-status').innerText = (goal.status || 'EXECUTING').toUpperCase();
  document.getElementById('ws-progress-bar').value = goal.progress || 0.1;
  document.getElementById('ws-progress-text').innerText = `${Math.round((goal.progress || 0.1) * 100)}%`;
  
  const fill = document.getElementById('ws-progress-bar-fill');
  if (fill) {
    fill.style.width = `${(goal.progress || 0.1) * 100}%`;
  }

  document.getElementById('ws-activity').innerText = `Running Kernel Process`;
  
  const treeContainer = document.getElementById('ws-plan-tree');
  const plan = goal.subgoals || [{name: 'Compile Objective', status: 'done'}, {name: 'Allocate Execution Block', status: 'active'}];
  
  treeContainer.innerHTML = plan.map(p => {
    let color = 'text-secondary';
    let icon = 'radio_button_unchecked';
    if(p.status === 'done') { color = 'text-cyan'; icon = 'check_circle'; }
    if(p.status === 'active') { color = 'text-primary animate-pulse'; icon = 'play_circle'; }
    
    return `
      <div class="flex items-center gap-3 py-1">
        <md-icon class="text-[14px] ${color}">${icon}</md-icon>
        <span class="text-xs font-mono ${p.status==='active' ? 'text-on-surface font-bold' : 'text-secondary'}">${p.description || p.name}</span>
      </div>
    `;
  }).join('');

  navigateTo('workspace');
}

/* =========================================================
   5. MODALS & INTERACTIONS
   ========================================================= */
function initModals() {
  const modalCreate = document.getElementById('modal-create-goal');
  
  // Home Screen Create Button
  document.getElementById('btn-open-create-goal').addEventListener('click', () => modalCreate.show());
  document.getElementById('btn-cancel-goal').addEventListener('click', () => modalCreate.close());
  
  // Submit New Goal -> Send to ECOS Backend!
  document.getElementById('btn-submit-goal').addEventListener('click', async () => {
    const title = document.getElementById('inp-goal-title').value.trim();
    if (!title) return;
    
    const prioStr = document.getElementById('inp-goal-priority').value;
    let prioInt = 10;
    if (prioStr === 'Medium') prioInt = 5;
    if (prioStr === 'Low') prioInt = 2;

    try {
      // Actually command the ECOS Kernel
      await fetch('/api/goals/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal: title, priority: prioInt })
      });
      
      // Close modal and force state refresh
      modalCreate.close();
      document.getElementById('inp-goal-title').value = '';
      
      await fetchBackendState();
      
      // Jump straight into the new goal workspace
      if (state.activeGoals.length > 0 && state.activeGoals[0].id !== 'sys') {
        openWorkspace(state.activeGoals[state.activeGoals.length-1].id);
      }
    } catch (err) {
      console.error("Failed to create goal in backend", err);
    }
  });

  // Trace Modal (Wired to Backend API)
  const modalTrace = document.getElementById('modal-trace');
  document.getElementById('btn-trace').addEventListener('click', async () => {
    try {
      const resp = await fetch('/api/memory'); // Or reflection
      const data = await resp.json();
      
      let memHtml = data.tiers.map(t => {
        if(t.count === 0) return '';
        return `<li>├── ${t.name}: ${t.count} items</li>`;
      }).join('');
      
      document.getElementById('trace-modal-body').innerHTML = `
        <div class="flex-col gap-4 text-sm">
          <div>
            <span class="text-secondary font-bold text-xs tracking-wider">ECOS KERNEL MEMORY HIERARCHY</span>
            <ul class="font-mono text-tertiary mt-1 list-none pl-0">
              ${memHtml || '<li>├── Kernel Memory Unallocated</li>'}
            </ul>
          </div>
        </div>
      `;
      modalTrace.show();
    } catch (e) {
      console.error(e);
    }
  });
  document.getElementById('btn-close-trace').addEventListener('click', () => modalTrace.close());
}

/* =========================================================
   6. CHAT & API
   ========================================================= */
function initCompanionChat() {
  const btnSend = document.getElementById('btn-send-chat');
  const inputUser = document.getElementById('chat-user-input');
  const container = document.getElementById('chat-messages-container');

  const sendMessage = async () => {
    const text = inputUser.value.trim();
    if (!text) return;

    // Append User Message
    const userMsgHtml = `
      <div class="msg msg-user self-end w-full max-w-[85%]">
        <div class="bg-primary-container border border-primary text-on-surface rounded p-3 text-xs font-mono leading-relaxed shadow-glow">
          <span class="text-[10px] text-primary block mb-1">USER ></span>
          ${text}
        </div>
      </div>
    `;
    container.insertAdjacentHTML('beforeend', userMsgHtml);
    inputUser.value = '';
    container.scrollTop = container.scrollHeight;

    // Call Backend ModelRouter
    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, assistant: 'architect' })
      });
      const data = await resp.json();
      const chat = data.chat;

      const formatMarkdown = (txt) => {
        return txt.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
      };

      const assistantMsgHtml = `
        <div class="msg msg-assistant self-start w-full max-w-[85%]">
          <div class="flex items-center gap-2 mb-1">
            <span class="material-symbols-outlined text-tertiary text-sm">memory</span>
            <span class="text-secondary text-[10px] font-mono font-bold tracking-wider">E.L.I.Z.A. // COMPANION</span>
          </div>
          <div class="bg-surface border rounded p-3 text-xs font-mono text-on-surface leading-relaxed shadow-sm">
            ${formatMarkdown(chat.response)}
          </div>
        </div>
      `;
      container.insertAdjacentHTML('beforeend', assistantMsgHtml);
      container.scrollTop = container.scrollHeight;
    } catch (e) {
      console.error('Error sending chat message:', e);
    }
  };

  btnSend.addEventListener('click', sendMessage);
  inputUser.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
}
