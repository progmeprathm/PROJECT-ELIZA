import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../store';

export default function Home() {
  const navigate = useNavigate();
  const persona = localStorage.getItem('eliza_persona') || 'User';
  
  const goals = useAppStore(state => state.goals);
  const setGoals = useAppStore(state => state.setGoals);
  const addGoal = useAppStore(state => state.addGoal);
  const trace = useAppStore(state => state.trace);

  useEffect(() => {
    // 1. Fetch Goals
    fetch('http://localhost:8001/api/goals')
      .then(res => res.json())
      .then(data => setGoals(data))
      .catch(err => console.error("Failed to fetch goals", err));
  }, [setGoals]);

  const handleCreateGoal = async () => {
    const goalTitle = prompt("What is your new goal?");
    if (!goalTitle) return;

    const newGoalId = `goal_${Date.now()}`;
    try {
      const res = await fetch('http://localhost:8001/api/goals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: newGoalId, title: goalTitle, priority: "High" })
      });
      
      if (res.ok) {
        const createdGoal = await res.json();
        addGoal(createdGoal);
        navigate(`/workspace/${createdGoal.id}`);
      } else {
        alert("Failed to create goal. Is the backend running?");
      }
    } catch (err) {
      alert("Failed to connect to the ECOS Kernel.");
    }
  };

  const currentGoal = goals.length > 0 ? goals[goals.length - 1] : null;

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out]">
      <header className="flex justify-between items-end border-b border-md-sys-color-outline-variant pb-6 mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Good Morning.</h1>
          <p className="text-md-sys-color-secondary">Persona: {persona}</p>
        </div>
        <button 
          className="bg-md-sys-color-on-surface text-md-sys-color-background px-4 py-2 rounded-lg font-medium flex items-center gap-2 hover:opacity-90"
          onClick={handleCreateGoal}
        >
          <span className="material-symbols-outlined text-sm">add</span>
          Create New Goal
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Focus Column */}
        <div className="lg:col-span-2 flex flex-col gap-8">
          
          <section>
            <h2 className="text-sm font-bold tracking-wider text-md-sys-color-secondary mb-4">TODAY'S FOCUS</h2>
            {currentGoal ? (
              <div 
                className="p-6 rounded-xl bg-md-sys-color-surface border border-md-sys-color-outline-variant hover:border-md-sys-color-primary cursor-pointer transition-colors"
                onClick={() => navigate(`/workspace/${currentGoal.id}`)}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-bold text-xl mb-1">{currentGoal.title}</h3>
                    <span className="text-xs font-bold tracking-wider text-md-sys-color-secondary">{currentGoal.status} | Priority: {currentGoal.priority}</span>
                  </div>
                  <span className="text-2xl font-bold font-mono text-ecos-success">{Math.round(currentGoal.progress)}%</span>
                </div>
                <div className="w-full bg-md-sys-color-surface-variant h-2 rounded-full overflow-hidden">
                  <div className="bg-ecos-success h-full" style={{ width: `${currentGoal.progress}%` }}></div>
                </div>
              </div>
            ) : (
              <div className="p-6 rounded-xl border border-dashed border-md-sys-color-outline-variant text-center text-md-sys-color-secondary">
                No active goals. Create one to begin the Golden Loop.
              </div>
            )}
          </section>

          <section>
            <h2 className="text-sm font-bold tracking-wider text-md-sys-color-secondary mb-4">CURRENT THOUGHT STREAM</h2>
            <div className="p-6 rounded-xl bg-md-sys-color-surface-variant border border-md-sys-color-outline-variant">
              <div className="flex items-center gap-3 text-md-sys-color-tertiary font-mono text-sm mb-2">
                <span className="material-symbols-outlined text-sm animate-spin">sync</span>
                <span>[{trace.module}]</span>
              </div>
              <p className="text-sm text-md-sys-color-secondary ml-7">{trace.content}</p>
            </div>
          </section>

        </div>

        {/* Sidebar Column */}
        <div className="flex flex-col gap-8">
          
          <section>
            <h2 className="text-sm font-bold tracking-wider text-md-sys-color-secondary mb-4">SYSTEM STATS</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-md-sys-color-surface border border-md-sys-color-outline-variant flex flex-col justify-center items-center">
                <span className="text-2xl font-bold text-ecos-success mb-1">{goals.length}</span>
                <span className="text-xs text-md-sys-color-secondary text-center">Active Goals</span>
              </div>
              <div className="p-4 rounded-xl bg-md-sys-color-surface border border-md-sys-color-outline-variant flex flex-col justify-center items-center">
                <span className="text-2xl font-bold text-md-sys-color-primary mb-1">Live</span>
                <span className="text-xs text-md-sys-color-secondary text-center">WebSocket</span>
              </div>
            </div>
          </section>

        </div>
      </div>
    </div>
  );
}
