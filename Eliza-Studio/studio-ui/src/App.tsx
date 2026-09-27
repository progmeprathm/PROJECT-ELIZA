import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Workspace from './pages/Workspace';
import Onboarding from './pages/Onboarding';
import ErrorBoundary from './components/ErrorBoundary';
import { useAppStore } from './store';

// New Modules
import Memory from './pages/Memory';
import Planner from './pages/Planner';
import Simulator from './pages/Simulator';
import WorldModel from './pages/WorldModel';
import Goals from './pages/Goals';
import Projects from './pages/Projects';
import Agents from './pages/Agents';
import Skills from './pages/Skills';
import Knowledge from './pages/Knowledge';
import Marketplace from './pages/Marketplace';
import Benchmarks from './pages/Benchmarks';
import Settings from './pages/Settings';
import Chat from './pages/Chat';

function App() {
  const [persona, setPersona] = useState<string | null>(localStorage.getItem('eliza_persona'));
  const navigate = useNavigate();
  const connectWebSocket = useAppStore(state => state.connectWebSocket);

  useEffect(() => {
    if (!persona) {
      navigate('/onboarding');
    } else if (window.location.pathname === '/onboarding') {
      navigate('/');
    }
  }, [persona, navigate]);
  
  useEffect(() => {
    if (persona) {
      connectWebSocket();
    }
  }, [persona, connectWebSocket]);

  if (!persona) {
    return <Onboarding setPersona={setPersona} />;
  }

  return (
    <div className="flex h-screen bg-md-sys-color-background text-md-sys-color-on-background">
      <Sidebar />
      <div className="flex-1 flex flex-col relative overflow-hidden">
        {/* Top Status Bar (Minimal) */}
        <header className="h-12 border-b border-md-sys-color-outline-variant flex items-center justify-between px-4 bg-md-sys-color-surface z-10 shrink-0">
          <div className="text-sm font-medium text-md-sys-color-secondary flex items-center gap-2">
            <span className="material-symbols-outlined text-sm">bolt</span>
            ELIZA Studio
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-md-sys-color-secondary">{persona}</span>
            <button 
              className="text-xs text-md-sys-color-primary bg-md-sys-color-surface-variant px-2 py-1 rounded hover:opacity-80"
              onClick={() => {
                localStorage.clear();
                setPersona(null);
              }}
            >
              Reset
            </button>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          <ErrorBoundary>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/workspace/:id" element={<Workspace />} />
              <Route path="/onboarding" element={<Onboarding setPersona={setPersona} />} />
              
              {/* Full OS Modules */}
              <Route path="/chat" element={<Chat />} />
              <Route path="/goals" element={<Goals />} />
              <Route path="/memory" element={<Memory />} />
              <Route path="/world" element={<WorldModel />} />
              <Route path="/planner" element={<Planner />} />
              <Route path="/simulation" element={<Simulator />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/knowledge" element={<Knowledge />} />
              <Route path="/skills" element={<Skills />} />
              <Route path="/agents" element={<Agents />} />
              <Route path="/marketplace" element={<Marketplace />} />
              <Route path="/benchmarks" element={<Benchmarks />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </ErrorBoundary>
        </main>
      </div>
    </div>
  );
}

export default App;
