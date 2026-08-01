import React, { useState, useEffect } from 'react';

export default function WorldModel() {
  const [nodes, setNodes] = useState([
    { id: '1', label: 'USER (Creator)', x: 50, y: 50 },
    { id: '2', label: 'ELIZA Kernel', x: 50, y: 250 },
    { id: '3', label: 'SQLite DB', x: 250, y: 150 }
  ]);
  const [edges, setEdges] = useState([
    { from: '1', to: '2', label: 'Commands' },
    { from: '2', to: '3', label: 'Persists' }
  ]);

  useEffect(() => {
    fetch('http://localhost:8001/api/world')
      .then(res => res.json())
      .then(data => {
        if (data.entities && data.entities.length > 0) {
          // Dynamic layout generation (naive circular layout)
          const newNodes = data.entities.map((e: any, i: number) => ({
            id: e.id,
            label: e.name,
            x: 400 + Math.cos(i * (Math.PI * 2) / data.entities.length) * 150,
            y: 250 + Math.sin(i * (Math.PI * 2) / data.entities.length) * 150
          }));
          setNodes(newNodes);
          setEdges(data.relationships.map((r: any) => ({
            from: r.source, to: r.target, label: r.relation
          })));
        }
      })
      .catch(console.error);
  }, []);

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold mb-2">World Model</h1>
          <p className="text-md-sys-color-secondary">The cognitive graph of entities, relationships, and context.</p>
        </div>
        <div className="bg-md-sys-color-surface-variant px-4 py-2 rounded flex items-center gap-2 border border-md-sys-color-outline-variant">
          <span className="material-symbols-outlined text-ecos-success text-sm">circle</span>
          <span className="text-xs font-bold tracking-widest text-md-sys-color-secondary">GRAPH ONLINE</span>
        </div>
      </header>

      <div className="flex-1 border border-md-sys-color-outline-variant rounded-xl bg-[#111] relative overflow-hidden flex items-center justify-center">
        
        {/* Grid Background */}
        <div className="absolute w-full h-full opacity-20 pointer-events-none" style={{
          backgroundImage: 'radial-gradient(circle at 50% 50%, #3f3f46 2px, transparent 2px)',
          backgroundSize: '40px 40px'
        }}></div>

        {/* Lines (SVG) */}
        <svg className="absolute w-full h-full top-0 left-0 pointer-events-none z-0">
          {edges.map((edge, i) => {
            const sourceNode = nodes.find(n => n.id === edge.from);
            const targetNode = nodes.find(n => n.id === edge.to);
            if (!sourceNode || !targetNode) return null;
            return (
              <line 
                key={i} 
                x1={sourceNode.x + 48} // Offset to center of node (approx)
                y1={sourceNode.y + 48} 
                x2={targetNode.x + 48} 
                y2={targetNode.y + 48} 
                stroke="#52525b" strokeWidth="2" strokeDasharray="5,5" 
              />
            );
          })}
        </svg>

        {/* Dynamic Nodes */}
        {nodes.map(node => (
          <div 
            key={node.id}
            className="absolute w-24 h-24 rounded-full border-2 border-md-sys-color-primary flex items-center justify-center bg-md-sys-color-surface z-10 hover:scale-110 transition-transform cursor-pointer"
            style={{ left: `${node.x}px`, top: `${node.y}px` }}
            title={node.label}
          >
            <div className="text-center p-2">
              <div className="text-xs font-bold line-clamp-2 leading-tight">{node.label}</div>
            </div>
          </div>
        ))}

        {/* Overlay Panel */}
        <div className="absolute bottom-4 left-4 bg-md-sys-color-surface-variant p-4 rounded-lg border border-md-sys-color-outline-variant max-w-[300px] z-20">
          <h3 className="font-bold mb-2 flex items-center gap-2">
            <span className="material-symbols-outlined text-sm">info</span>
            Graph Statistics
          </h3>
          <p className="text-sm text-md-sys-color-secondary mb-2">
            Total Entities: {nodes.length}<br/>
            Total Relationships: {edges.length}
          </p>
        </div>

      </div>
    </div>
  );
}
