import React, { useState, useEffect } from 'react';

export default function Simulator() {
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeGoal, setActiveGoal] = useState<any>(null);
  const [simulationResult, setSimulationResult] = useState<any>(null);
  const [selectedPlan, setSelectedPlan] = useState('plan_a');

  useEffect(() => {
    fetch('http://localhost:8001/api/goals')
      .then(res => res.json())
      .then(data => {
        if (data && data.length > 0) {
          setActiveGoal(data[data.length - 1]);
        }
      })
      .catch(console.error);
  }, []);

  const runSimulation = async () => {
    if (!activeGoal) return;
    setRunning(true);
    setProgress(0);
    setSimulationResult(null);

    // Start fake progress bar
    const interval = setInterval(() => setProgress(p => Math.min(p + 10, 90)), 200);

    try {
      const planToSimulate = activeGoal.plan?.[selectedPlan] || [];
      const res = await fetch('http://localhost:8001/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan: planToSimulate, goal_title: activeGoal.title })
      });
      const data = await res.json();
      
      clearInterval(interval);
      setProgress(100);
      setSimulationResult(data);
    } catch (e) {
      clearInterval(interval);
      setProgress(100);
      setSimulationResult({ success_probability: 0, critique: "Error communicating with Simulator Kernel." });
    }
    setRunning(false);
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold mb-2">Speculative Simulator</h1>
          <p className="text-md-sys-color-secondary">Dry-run plans against the world model before execution.</p>
        </div>
        <button 
          onClick={runSimulation}
          disabled={running || !activeGoal}
          className="bg-ecos-warning text-[#18181b] px-6 py-2 rounded font-bold flex items-center gap-2 hover:opacity-90 disabled:opacity-50 transition-opacity"
        >
          <span className="material-symbols-outlined">play_arrow</span>
          {running ? 'Simulating...' : 'Run Simulation'}
        </button>
      </header>

      {/* Main Panel */}
      <div className="bg-md-sys-color-surface-variant border border-md-sys-color-outline-variant rounded-xl p-6 flex flex-col flex-1 min-h-0">
        
        {/* Top Controls */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-md-sys-color-surface p-4 rounded border border-md-sys-color-outline-variant">
            <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest mb-1">TARGET PLAN</div>
            <select 
              value={selectedPlan} 
              onChange={e => setSelectedPlan(e.target.value)}
              className="bg-transparent text-sm w-full outline-none font-bold"
            >
              <option value="plan_a">Plan Alpha ({activeGoal ? activeGoal.title : 'Loading...'})</option>
              <option value="plan_b">Plan Beta ({activeGoal ? activeGoal.title : 'Loading...'})</option>
            </select>
          </div>
          <div className="bg-md-sys-color-surface p-4 rounded border border-md-sys-color-outline-variant">
            <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest mb-1">MONTE CARLO ITERATIONS</div>
            <div className="text-sm font-bold font-mono">1,000</div>
          </div>
          <div className="bg-md-sys-color-surface p-4 rounded border border-md-sys-color-outline-variant">
            <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest mb-1">SUCCESS PROBABILITY</div>
            <div className={`text-xl font-bold ${simulationResult ? 'text-ecos-success' : 'text-md-sys-color-secondary'}`}>
              {simulationResult ? `${(simulationResult.success_probability * 100).toFixed(1)}%` : '--%'}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        {(running || progress > 0) && (
          <div className="mb-6">
            <div className="h-2 bg-md-sys-color-surface rounded-full overflow-hidden">
              <div 
                className="h-full bg-ecos-warning transition-all duration-200 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Logs */}
        <div className="flex-1 bg-[#09090b] rounded border border-md-sys-color-outline-variant p-4 font-mono text-sm overflow-y-auto">
          <div className="text-md-sys-color-secondary mb-2">// ECOS SIMULATOR KERNEL initialized</div>
          {progress > 10 && <div className="text-ecos-success">Connecting to World Model context... OK</div>}
          {progress > 40 && <div className="text-ecos-success">Parsing Plan logic gates... OK</div>}
          {progress > 70 && <div className="text-ecos-warning">Running speculative LLM inference loops...</div>}
          {simulationResult && (
            <div className="mt-4 border-t border-md-sys-color-outline-variant pt-4 text-md-sys-color-on-background">
              --- SIMULATION COMPLETE ---<br/>
              Result: {simulationResult.success_probability > 0.7 ? 'High likelihood of success.' : 'High risk of failure paths.'}<br/>
              Critique: {simulationResult.critique}
            </div>
          )}
        </div>
      </div>
      </div>
    </div>
  );
}
