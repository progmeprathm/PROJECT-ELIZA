import React, { useState, useEffect } from 'react';

export default function Planner() {
  const [activeGoal, setActiveGoal] = useState<any>(null);

  useEffect(() => {
    fetch('http://localhost:8001/api/goals')
      .then(res => res.json())
      .then(data => {
        if (data && data.length > 0) {
          // Grab the most recent goal
          setActiveGoal(data[data.length - 1]);
        }
      })
      .catch(console.error);
  }, []);

  if (!activeGoal) {
    return (
      <div className="p-8 flex items-center justify-center h-full text-md-sys-color-secondary">
        No active goals found. Create a goal in the Workspace to see cognitive planning!
      </div>
    );
  }

  // Parse the dual-tree plan. If it's the old array format, mock a dual format.
  const planA = activeGoal.plan?.plan_a || (Array.isArray(activeGoal.plan) ? activeGoal.plan : []);
  const planB = activeGoal.plan?.plan_b || [{"name": "Awaiting Plan B generation...", "status": "pending"}];

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Cognitive Planner</h1>
        <p className="text-md-sys-color-secondary">Review alternative goal decompositions and their theoretical outcomes.</p>
      </header>

      <div className="flex items-center gap-4 mb-8 bg-md-sys-color-surface-variant p-4 rounded-xl border border-md-sys-color-outline-variant">
        <span className="material-symbols-outlined text-md-sys-color-tertiary">account_tree</span>
        <div>
          <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest">ACTIVE GOAL ANALYSIS</div>
          <div className="font-bold text-lg">{activeGoal.title}</div>
        </div>
      </div>

      {/* Plans Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Plan A */}
        <div className="p-6 rounded-xl bg-md-sys-color-surface border-2 border-md-sys-color-tertiary relative flex flex-col">
          <div className="absolute top-0 right-0 bg-md-sys-color-tertiary text-md-sys-color-on-tertiary px-3 py-1 rounded-bl-lg rounded-tr-lg text-xs font-bold tracking-widest">
            RECOMMENDED (SAFE)
          </div>
          
          <h2 className="text-2xl font-bold mb-6">Plan Alpha</h2>
          
          <div className="grid grid-cols-3 gap-2 mb-6">
            <div className="bg-md-sys-color-surface-variant p-3 rounded text-center">
              <div className="text-[10px] font-bold text-md-sys-color-secondary tracking-widest mb-1">COST</div>
              <div className="text-ecos-success font-bold">Low</div>
            </div>
            <div className="bg-md-sys-color-surface-variant p-3 rounded text-center">
              <div className="text-[10px] font-bold text-md-sys-color-secondary tracking-widest mb-1">RISK</div>
              <div className="text-ecos-success font-bold">Low</div>
            </div>
            <div className="bg-md-sys-color-surface-variant p-3 rounded text-center">
              <div className="text-[10px] font-bold text-md-sys-color-secondary tracking-widest mb-1">TIME</div>
              <div className="text-md-sys-color-on-surface font-bold">Iterative</div>
            </div>
          </div>

          <div className="flex-1">
            <h3 className="text-sm font-bold text-md-sys-color-secondary tracking-widest mb-3">DECOMPOSITION</h3>
            <ul className="flex flex-col gap-3">
              {planA.map((step: any, i: number) => (
                <li key={i} className="flex gap-3 text-sm">
                  <span className="text-md-sys-color-tertiary font-bold">{i + 1}.</span>
                  <span>{step.name}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <button className="w-full mt-6 bg-md-sys-color-tertiary text-md-sys-color-on-tertiary py-3 rounded-lg font-bold hover:opacity-90 transition-opacity">
            Select Plan Alpha
          </button>
        </div>

        {/* Plan B */}
        <div className="p-6 rounded-xl bg-md-sys-color-surface border border-md-sys-color-outline-variant flex flex-col">
          <h2 className="text-2xl font-bold mb-6 text-md-sys-color-secondary">Plan Beta (Aggressive)</h2>
          
          <div className="grid grid-cols-3 gap-2 mb-6 opacity-70">
            <div className="bg-md-sys-color-surface-variant p-3 rounded text-center">
              <div className="text-[10px] font-bold text-md-sys-color-secondary tracking-widest mb-1">COST</div>
              <div className="text-ecos-warning font-bold">Med</div>
            </div>
            <div className="bg-md-sys-color-surface-variant p-3 rounded text-center">
              <div className="text-[10px] font-bold text-md-sys-color-secondary tracking-widest mb-1">RISK</div>
              <div className="text-md-sys-color-error font-bold">High</div>
            </div>
            <div className="bg-md-sys-color-surface-variant p-3 rounded text-center">
              <div className="text-[10px] font-bold text-md-sys-color-secondary tracking-widest mb-1">TIME</div>
              <div className="text-ecos-success font-bold">Fast</div>
            </div>
          </div>

          <div className="flex-1 opacity-70">
            <h3 className="text-sm font-bold text-md-sys-color-secondary tracking-widest mb-3">DECOMPOSITION</h3>
            <ul className="flex flex-col gap-3">
              {planB.map((step: any, i: number) => (
                <li key={i} className="flex gap-3 text-sm text-md-sys-color-secondary">
                  <span className="font-bold">{i + 1}.</span>
                  <span>{step.name}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <button className="w-full mt-6 bg-md-sys-color-surface-variant text-md-sys-color-on-surface py-3 rounded-lg font-bold hover:bg-[#27272a] transition-colors">
            Select Plan Beta
          </button>
        </div>

      </div>
    </div>
  );
}
