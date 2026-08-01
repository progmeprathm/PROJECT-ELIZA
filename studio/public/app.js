/**
 * ELIZA Goal-Centric Frontend SPA Logic
 */

let state = {
  persona: null,
  activeGoals: [],
  currentGoalId: null
};

document.addEventListener('DOMContentLoaded', () => {
  initAppState();
  initOnboarding();
  initModals();
  initCompanionChat();
  
  // Periodic UI Updates
  setInterval(updateLiveState, 3000);
});

/* =========================================================
   1. STATE MANAGEMENT & ROUTING
   ========================================================= */
function initAppState() {
  const savedPersona = localStorage.getItem('eliza_persona');
  const savedGoals = localStorage.getItem('eliza_goals');
  
  if (savedPersona) {
    state.persona = savedPersona;
    document.getElementById('lbl-persona').innerText = savedPersona;
    document.getElementById('lbl-home-persona').innerText = `Persona: ${savedPersona}`;
    if (savedGoals) {
      state.activeGoals = JSON.parse(savedGoals);
    }
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
    localStorage.removeItem('eliza_goals');
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
  target.classList.remove('hidden');

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
    card.addEventListener('click', () => {
      const selected = card.getAttribute('data-persona');
      localStorage.setItem('eliza_persona', selected);
      
      // Default goal for demo purposes
      const defaultGoals = [{
        id: 'g-1',
        title: 'Build ECOS Kernel',
        priority: 'High',
        progress: 0.14,
        status: 'EXECUTING',
        activity: 'Designing Scheduler',
        nextStep: 'Kernel Interfaces',
        plan: [
          { name: 'Architecture', status: 'done' },
          { name: 'Kernel', status: 'active' },
          { name: 'Scheduler', status: 'pending' },
          { name: 'Testing', status: 'pending' }
        ]
      }];
      
      localStorage.setItem('eliza_goals', JSON.stringify(defaultGoals));
      
      initAppState(); // Re-evaluate and route to Home
    });
  });
}

/* =========================================================
   3. HOME DASHBOARD (SCREEN B)
   ========================================================= */
function renderHomeDashboard() {
  const container = document.getElementById('home-active-goals');
  
  if (state.activeGoals.length === 0) {
    container.innerHTML = `
      <div class="p-6 rounded-xl bg-surface-variant border border-outline-variant text-center">
        <p class="text-secondary mb-4">No active goals. Let's start building.</p>
        <md-filled-button onclick="document.getElementById('modal-create-goal').show()">Create Your First Goal</md-filled-button>
      </div>
    `;
    return;
  }

  container.innerHTML = state.activeGoals.map(g => `
    <div class="p-6 rounded-xl bg-surface border border-outline-variant hover:border-primary cursor-pointer transition-colors" onclick="openWorkspace('${g.id}')">
      <div class="flex justify-between items-start mb-4">
        <div>
          <h3 class="font-bold text-lg mb-1">${g.title}</h3>
          <span class="text-xs text-secondary font-bold tracking-wider">${g.status} | Priority: ${g.priority}</span>
        </div>
        <span class="text-xl font-bold font-mono text-success">${Math.round(g.progress * 100)}%</span>
      </div>
      <md-linear-progress value="${g.progress}" class="w-full"></md-linear-progress>
    </div>
  `).join('');
}

/* =========================================================
   4. WORKSPACE (SCREEN C)
   ========================================================= */
function openWorkspace(goalId) {
  state.currentGoalId = goalId;
  const goal = state.activeGoals.find(g => g.id === goalId);
  if (!goal) return;

  // Populate Workspace DOM
  document.getElementById('ws-title').innerText = goal.title;
  document.getElementById('ws-goal-title').innerText = goal.title;
  document.getElementById('ws-status').innerText = goal.status;
  document.getElementById('ws-progress-bar').value = goal.progress;
  document.getElementById('ws-progress-text').innerText = `${Math.round(goal.progress * 100)}%`;
  document.getElementById('ws-activity').innerText = goal.activity;
  
  const treeContainer = document.getElementById('ws-plan-tree');
  treeContainer.innerHTML = goal.plan.map(p => {
    let color = 'text-secondary';
    let icon = 'radio_button_unchecked';
    if(p.status === 'done') { color = 'text-success'; icon = 'check_circle'; }
    if(p.status === 'active') { color = 'text-primary'; icon = 'play_circle'; }
    
    return `
      <div class="flex items-center gap-3 py-1">
        <md-icon class="text-sm ${color}">${icon}</md-icon>
        <span class="text-sm font-medium ${p.status==='active' ? 'text-on-surface' : 'text-secondary'}">${p.name}</span>
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
  
  // Submit New Goal
  document.getElementById('btn-submit-goal').addEventListener('click', () => {
    const title = document.getElementById('inp-goal-title').value.trim();
    if (!title) return;

    const newGoal = {
      id: `g-${Date.now()}`,
      title: title,
      priority: document.getElementById('inp-goal-priority').value,
      progress: 0,
      status: 'PLANNING',
      activity: 'Decomposing objectives',
      nextStep: 'Resource allocation',
      plan: [
        { name: 'Research Phase', status: 'active' },
        { name: 'Execution Phase', status: 'pending' },
        { name: 'Review Phase', status: 'pending' }
      ]
    };

    state.activeGoals.push(newGoal);
    localStorage.setItem('eliza_goals', JSON.stringify(state.activeGoals));
    
    modalCreate.close();
    document.getElementById('inp-goal-title').value = '';
    
    // Jump straight into the new goal workspace
    openWorkspace(newGoal.id);
  });

  // Trace Modal
  const modalTrace = document.getElementById('modal-trace');
  document.getElementById('btn-trace').addEventListener('click', () => {
    document.getElementById('trace-modal-body').innerHTML = `
      <div class="flex-col gap-4 text-sm">
        <div>
          <span class="text-secondary font-bold text-xs tracking-wider">EVIDENCE</span>
          <ul class="font-mono text-success mt-1 list-none pl-0">
            <li>├── Kernel constraints verified</li>
            <li>├── Workload benchmarked</li>
          </ul>
        </div>
        <div>
          <span class="text-secondary font-bold text-xs tracking-wider">CONFIDENCE</span>
          <div class="font-mono text-tertiary mt-1">87%</div>
        </div>
      </div>
    `;
    modalTrace.show();
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
        <div class="bg-primary-container text-on-primary-container rounded-2xl rounded-tr-sm p-4 text-sm leading-relaxed">${text}</div>
      </div>
    `;
    container.insertAdjacentHTML('beforeend', userMsgHtml);
    inputUser.value = '';
    container.scrollTop = container.scrollHeight;

    // Call Backend
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
            <span class="material-symbols-outlined text-primary text-sm">smart_toy</span>
            <span class="text-secondary text-xs font-bold tracking-wider">ELIZA</span>
          </div>
          <div class="bg-surface-variant border border-outline-variant rounded-2xl rounded-tl-sm p-4 text-sm text-on-surface leading-relaxed">
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

function updateLiveState() {
  // If we are in the workspace and we have an active goal, we could poll for progress updates here.
  // In a real app, this would hit /api/goals/:id
}
