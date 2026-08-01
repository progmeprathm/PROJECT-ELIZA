import React, { useState } from 'react';
import { useParams } from 'react-router-dom';

export default function Workspace() {
  const { id } = useParams();
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Three candidate designs found.\n\n- Simple implementation\n- High-performance implementation\n- Distributed implementation' }
  ]);

  const handleSend = () => {
    if (!chatInput.trim()) return;
    setMessages(prev => [...prev, { role: 'user', text: chatInput }]);
    setChatInput('');
    
    // Mock response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        text: 'Decision logged. I will simulate the high-performance implementation.' 
      }]);
    }, 1000);
  };

  return (
    <div className="flex h-full w-full animate-[fadeIn_0.3s_ease-out]">
      
      {/* LEFT PANE: Persistent Goal State */}
      <aside className="w-[45%] h-full bg-md-sys-color-surface border-r border-md-sys-color-outline-variant overflow-y-auto p-6 flex flex-col gap-8">
        
        <header>
          <div className="text-xs font-bold text-md-sys-color-primary tracking-wider mb-2">EXECUTING</div>
          <h1 className="text-2xl font-bold mb-4">Build ECOS Kernel {id === 'new' ? '(New)' : ''}</h1>
          <div className="flex items-center gap-4 mb-2">
            <div className="flex-1 bg-md-sys-color-surface-variant h-2 rounded-full overflow-hidden">
              <div className="bg-ecos-success h-full" style={{ width: '63%' }}></div>
            </div>
            <span className="text-sm font-bold font-mono text-ecos-success">63%</span>
          </div>
        </header>

        <section className="p-5 rounded-xl bg-md-sys-color-surface-variant border border-md-sys-color-outline-variant">
          <div className="text-xs font-bold text-md-sys-color-secondary tracking-wider mb-2">CURRENT ACTIVITY</div>
          <div className="font-medium text-lg text-md-sys-color-tertiary mb-4">Designing Scheduler</div>
          
          <div className="text-xs font-bold text-md-sys-color-secondary tracking-wider mb-2">NEXT STEP</div>
          <div className="font-mono text-sm bg-md-sys-color-background p-3 rounded-md text-md-sys-color-primary">Kernel Interfaces</div>
        </section>

        <section>
          <h2 className="text-sm font-bold tracking-wider text-md-sys-color-secondary mb-4">DECOMPOSED PLAN</h2>
          <div className="flex flex-col gap-2 border-l-2 border-md-sys-color-outline-variant ml-2 pl-4">
            
            <div className="flex items-center gap-3 py-1">
              <span className="material-symbols-outlined text-sm text-ecos-success">check_circle</span>
              <span className="text-sm font-medium text-md-sys-color-secondary line-through">Architecture</span>
            </div>
            
            <div className="flex items-center gap-3 py-1">
              <span className="material-symbols-outlined text-sm text-md-sys-color-primary">play_circle</span>
              <span className="text-sm font-medium text-md-sys-color-on-surface">Kernel</span>
            </div>

            <div className="flex items-center gap-3 py-1 pl-6">
              <span className="material-symbols-outlined text-sm text-md-sys-color-primary animate-pulse">sync</span>
              <span className="text-sm font-medium text-md-sys-color-on-surface">Scheduler</span>
            </div>

            <div className="flex items-center gap-3 py-1 pl-6">
              <span className="material-symbols-outlined text-sm text-md-sys-color-secondary">radio_button_unchecked</span>
              <span className="text-sm font-medium text-md-sys-color-secondary">State Manager</span>
            </div>
            
            <div className="flex items-center gap-3 py-1">
              <span className="material-symbols-outlined text-sm text-md-sys-color-secondary">radio_button_unchecked</span>
              <span className="text-sm font-medium text-md-sys-color-secondary">Testing</span>
            </div>

          </div>
        </section>

        <section>
          <h2 className="text-sm font-bold tracking-wider text-md-sys-color-secondary mb-4">RETRIEVED CONTEXT</h2>
          <div className="flex gap-2 flex-wrap">
            <span className="px-3 py-1 rounded-full bg-md-sys-color-background border border-md-sys-color-outline-variant text-xs text-md-sys-color-secondary">Kernel Spec</span>
            <span className="px-3 py-1 rounded-full bg-md-sys-color-background border border-md-sys-color-outline-variant text-xs text-md-sys-color-secondary">Protocol</span>
            <span className="px-3 py-1 rounded-full bg-md-sys-color-background border border-md-sys-color-outline-variant text-xs text-md-sys-color-secondary">Previous Decisions</span>
          </div>
        </section>

      </aside>

      {/* RIGHT PANE: Conversational Interface */}
      <main className="flex-1 h-full bg-md-sys-color-background flex flex-col relative">
        <div className="p-4 border-b border-md-sys-color-outline-variant flex items-center justify-between bg-md-sys-color-surface/90 backdrop-blur sticky top-0 z-10">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-md-sys-color-primary text-sm">smart_toy</span>
            <span className="font-bold text-sm text-md-sys-color-secondary">ELIZA Companion</span>
          </div>
          <button className="text-xs border border-md-sys-color-outline-variant px-3 py-1 rounded hover:bg-md-sys-color-surface-variant transition-colors">
            Reasoning Inspector
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
          
          <div className="self-end w-full max-w-[85%]">
            <div className="bg-md-sys-color-primary-container text-md-sys-color-on-primary-container rounded-2xl rounded-tr-sm p-4 text-sm leading-relaxed">
              Design the scheduler.
            </div>
          </div>

          {messages.map((msg, i) => (
            <div key={i} className={`w-full max-w-[85%] ${msg.role === 'user' ? 'self-end' : 'self-start'}`}>
              {msg.role === 'assistant' && (
                <div className="flex items-center gap-2 mb-1">
                  <span className="material-symbols-outlined text-md-sys-color-primary text-sm">smart_toy</span>
                  <span className="text-md-sys-color-secondary text-xs font-bold tracking-wider">ELIZA</span>
                </div>
              )}
              <div className={`rounded-2xl p-4 text-sm leading-relaxed whitespace-pre-wrap ${
                msg.role === 'user' 
                  ? 'bg-md-sys-color-primary-container text-md-sys-color-on-primary-container rounded-tr-sm' 
                  : 'bg-md-sys-color-surface-variant border border-md-sys-color-outline-variant text-md-sys-color-on-surface rounded-tl-sm'
              }`}>
                {msg.text}
              </div>
              {msg.role === 'assistant' && (
                <div className="mt-2 flex gap-2">
                  <button className="text-xs bg-md-sys-color-surface border border-md-sys-color-outline-variant px-2 py-1 rounded hover:text-md-sys-color-primary transition-colors">Open Comparison</button>
                  <button className="text-xs bg-md-sys-color-surface border border-md-sys-color-outline-variant px-2 py-1 rounded hover:text-ecos-warning transition-colors">Open Simulation</button>
                </div>
              )}
            </div>
          ))}

        </div>

        <div className="p-4 bg-md-sys-color-surface border-t border-md-sys-color-outline-variant shrink-0">
          <div className="relative">
            <input 
              type="text" 
              className="w-full bg-md-sys-color-surface-variant border border-md-sys-color-outline-variant rounded-full py-3 pl-4 pr-12 text-sm text-md-sys-color-on-surface focus:outline-none focus:border-md-sys-color-primary transition-colors"
              placeholder="Guide ELIZA's work..."
              value={chatInput}
              onChange={e => setChatInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
            />
            <button 
              className="absolute right-2 top-1.5 bottom-1.5 w-8 h-8 rounded-full bg-md-sys-color-primary text-md-sys-color-on-primary flex items-center justify-center hover:opacity-90 transition-opacity"
              onClick={handleSend}
            >
              <span className="material-symbols-outlined text-sm">send</span>
            </button>
          </div>
          <div className="text-center text-xs text-md-sys-color-secondary mt-3">
            Use the chat to provide context, review decisions, or ask for explanations.
          </div>
        </div>
      </main>

    </div>
  );
}
