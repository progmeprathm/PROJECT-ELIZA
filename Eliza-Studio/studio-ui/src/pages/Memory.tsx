import React, { useState, useEffect } from 'react';

const memoryTiers = ['Working', 'Semantic', 'Episodic', 'Long-Term', 'Archived'];

export default function Memory() {
  const [activeTier, setActiveTier] = useState('Working');
  const [memories, setMemories] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://localhost:8001/api/memory')
      .then(res => res.json())
      .then(data => setMemories(data))
      .catch(console.error);
  }, []);

  const filteredMemories = memories.filter(m => m.tier === activeTier);

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Memory Architecture</h1>
        <p className="text-md-sys-color-secondary">Inspect how ELIZA retains, structures, and retrieves information.</p>
      </header>

      {/* Tabs */}
      <div className="flex border-b border-md-sys-color-outline-variant mb-6 overflow-x-auto">
        {memoryTiers.map(tier => (
          <button
            key={tier}
            onClick={() => setActiveTier(tier)}
            className={`px-6 py-3 font-medium transition-colors whitespace-nowrap ${
              activeTier === tier 
                ? 'text-ecos-success border-b-2 border-ecos-success' 
                : 'text-md-sys-color-secondary hover:text-md-sys-color-on-background hover:bg-md-sys-color-surface-variant'
            }`}
          >
            {tier}
          </button>
        ))}
      </div>

      {/* Content Area */}
      <div className="flex-1 flex gap-8 min-h-0">
        
        {/* Left List */}
        <div className="w-[400px] flex flex-col gap-4 overflow-y-auto pr-2">
          {filteredMemories.length === 0 ? (
            <div className="p-4 text-md-sys-color-secondary text-sm">No memories extracted yet. Chat with ELIZA to populate!</div>
          ) : filteredMemories.map((mem, i) => (
            <div key={mem.id || i} className="p-4 rounded-xl border border-md-sys-color-outline-variant bg-md-sys-color-surface cursor-pointer hover:border-ecos-success transition-colors">
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-mono font-bold text-ecos-success tracking-widest">{mem.id ? mem.id.substring(0, 12).toUpperCase() : `MEM_${i}`}</span>
                <span className="text-xs text-md-sys-color-secondary">Just now</span>
              </div>
              <h3 className="font-bold mb-1 line-clamp-1">{mem.content}</h3>
              <p className="text-sm text-md-sys-color-secondary line-clamp-2">
                {mem.content}
              </p>
            </div>
          ))}
        </div>

        {/* Right Inspector */}
        <div className="flex-1 bg-md-sys-color-surface-variant rounded-xl border border-md-sys-color-outline-variant p-6 flex flex-col">
          <div className="flex items-center gap-3 mb-6 pb-4 border-b border-md-sys-color-outline-variant">
            <span className="material-symbols-outlined text-ecos-success">memory</span>
            <h2 className="text-xl font-bold">Memory Inspector</h2>
          </div>
          
          <div className="flex-1 flex flex-col gap-6">
            <div>
              <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest mb-2">TRANSFORMER TRACE</div>
              <div className="bg-md-sys-color-background p-4 rounded-lg font-mono text-sm text-md-sys-color-on-background border border-md-sys-color-outline-variant">
                Attention Head 4 -&gt; Identified Context: "Sleek Dark Mode"<br/>
                Vector Embedding -&gt; [0.12, -0.45, 0.88, ...]<br/>
                Similarity Score -&gt; 0.94 (Match: User Preferences)
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-md-sys-color-surface p-4 rounded-lg border border-md-sys-color-outline-variant">
                <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest mb-1">SOURCE</div>
                <div className="text-sm">Conversation #42 (Workspace)</div>
              </div>
              <div className="bg-md-sys-color-surface p-4 rounded-lg border border-md-sys-color-outline-variant">
                <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest mb-1">CONFIDENCE</div>
                <div className="text-sm text-ecos-success font-bold">99.9%</div>
              </div>
            </div>

            <div>
              <div className="text-xs font-bold text-md-sys-color-secondary tracking-widest mb-2">ASSOCIATED BELIEFS</div>
              <div className="flex gap-2">
                <span className="px-3 py-1 bg-md-sys-color-primary-container text-md-sys-color-primary rounded-full text-xs">Tailwind CSS</span>
                <span className="px-3 py-1 bg-md-sys-color-primary-container text-md-sys-color-primary rounded-full text-xs">Zinc/Slate</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
