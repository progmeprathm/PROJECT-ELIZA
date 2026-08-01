import React, { useState, useEffect } from 'react';

interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string;
  status: string;
}

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  
  useEffect(() => {
    fetch('http://localhost:8001/api/agents')
      .then(res => res.json())
      .then(data => setAgents(data))
      .catch(err => console.error(err));
  }, []);

  const spawnAgent = () => {
    fetch('http://localhost:8001/api/agents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'New Agent', role: 'Worker', capabilities: '[]' })
    })
    .then(res => res.json())
    .then(data => setAgents([...agents, data]))
    .catch(err => console.error(err));
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Agent Swarm</h1>
        <p className="text-md-sys-color-secondary">Manage sub-personas and delegated cognitive workers.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {agents.map(agent => (
          <div key={agent.id} className="bg-md-sys-color-surface-variant p-6 rounded-xl border border-md-sys-color-outline-variant flex flex-col">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-ecos-success flex items-center justify-center text-[#111] font-bold">{agent.name.charAt(0).toUpperCase()}</div>
              <div>
                <h2 className="font-bold">{agent.name}</h2>
                <div className={`text-xs tracking-widest font-bold ${agent.status.toLowerCase() === 'online' ? 'text-ecos-success' : 'text-md-sys-color-secondary'}`}>{agent.status.toUpperCase()}</div>
              </div>
            </div>
            <p className="text-sm text-md-sys-color-secondary mb-4 flex-1">
              Role: {agent.role}
            </p>
            <div className="text-xs bg-md-sys-color-surface p-2 rounded text-center">ID: {agent.id}</div>
          </div>
        ))}

        <div onClick={spawnAgent} className="bg-md-sys-color-surface p-6 rounded-xl border border-md-sys-color-outline-variant border-dashed cursor-pointer hover:border-md-sys-color-secondary transition-colors flex flex-col items-center justify-center text-md-sys-color-secondary min-h-[200px]">
          <span className="material-symbols-outlined text-4xl mb-2">add_circle</span>
          <h2 className="font-bold">Spawn Agent</h2>
        </div>
      </div>
    </div>
  );
}
