import React, { useState, useEffect, useRef } from 'react';

const TYPE_COLORS: Record<string, string> = {
  Goal: 'border-yellow-500 bg-yellow-500/20 text-yellow-100',
  Skill: 'border-blue-500 bg-blue-500/20 text-blue-100',
  Obstacle: 'border-red-500 bg-red-500/20 text-red-100',
  Belief: 'border-purple-500 bg-purple-500/20 text-purple-100',
  Constraint: 'border-orange-500 bg-orange-500/20 text-orange-100',
  Event: 'border-pink-500 bg-pink-500/20 text-pink-100',
  Entity: 'border-teal-500 bg-teal-500/20 text-teal-100',
  Concept: 'border-gray-500 bg-gray-500/20 text-gray-100'
};

export default function WorldModel() {
  const [nodes, setNodes] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);

  // Pan and Zoom state
  const [transform, setTransform] = useState({ x: 0, y: 0, scale: 1 });
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState({ x: 0, y: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch('http://localhost:8001/api/world')
      .then(res => res.json())
      .then(data => {
        if (data.entities && data.entities.length > 0) {
          // Dynamic layout generation (Sunflower spiral for better scaling)
          const newNodes = data.entities.map((e: any, i: number) => {
            const angle = i * 137.5 * (Math.PI / 180);
            const radius = 80 + Math.sqrt(i) * 60;
            return {
              id: e.id,
              label: e.name,
              type: e.type || 'Concept',
              attributes: e.attributes || {},
              x: 600 + Math.cos(angle) * radius, // Center offset
              y: 350 + Math.sin(angle) * radius
            };
          });
          setNodes(newNodes);
          setEdges(data.relationships.map((r: any) => ({
            from: r.source, to: r.target, label: r.relation
          })));
        } else {
          // Fallback if empty
          setNodes([
             { id: '1', label: 'USER (Creator)', type: 'Entity', x: 600, y: 300, attributes: {} },
             { id: '2', label: 'ELIZA Kernel', type: 'Entity', x: 600, y: 500, attributes: {} }
          ]);
        }
      })
      .catch(console.error);
  }, []);

  const handleWheel = (e: React.WheelEvent) => {
    const scaleFactor = e.deltaY > 0 ? 0.9 : 1.1;
    setTransform(prev => ({ ...prev, scale: Math.max(0.1, Math.min(5, prev.scale * scaleFactor)) }));
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('.node-element')) return; // Don't pan if clicking node
    setIsPanning(true);
    setPanStart({ x: e.clientX - transform.x, y: e.clientY - transform.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isPanning) return;
    setTransform(prev => ({ ...prev, x: e.clientX - panStart.x, y: e.clientY - panStart.y }));
  };

  const handleMouseUp = () => setIsPanning(false);

  return (
    <div className="p-8 mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col relative w-full overflow-hidden">
      <header className="mb-8 flex justify-between items-end shrink-0 z-20">
        <div>
          <h1 className="text-3xl font-bold mb-2">World Model</h1>
          <p className="text-md-sys-color-secondary">The cognitive graph of entities, relationships, and context.</p>
        </div>
        <div className="bg-md-sys-color-surface-variant px-4 py-2 rounded flex items-center gap-2 border border-md-sys-color-outline-variant">
          <span className="material-symbols-outlined text-ecos-success text-sm">circle</span>
          <span className="text-xs font-bold tracking-widest text-md-sys-color-secondary">GRAPH ONLINE</span>
        </div>
      </header>

      <div 
        ref={containerRef}
        className="flex-1 border border-md-sys-color-outline-variant rounded-xl bg-[#0a0a0a] relative overflow-hidden flex cursor-grab active:cursor-grabbing"
        onWheel={handleWheel}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        {/* Graph Transform Container */}
        <div 
          className="absolute inset-0 pointer-events-none origin-top-left"
          style={{ transform: `translate(${transform.x}px, ${transform.y}px) scale(${transform.scale})` }}
        >
          {/* Grid Background */}
          <div className="absolute w-[4000px] h-[4000px] -left-[1000px] -top-[1000px] opacity-20 pointer-events-none" style={{
            backgroundImage: 'radial-gradient(circle at 50% 50%, #3f3f46 2px, transparent 2px)',
            backgroundSize: '40px 40px'
          }}></div>

          {/* Lines (SVG) */}
          <svg className="absolute w-[4000px] h-[4000px] -left-[1000px] -top-[1000px] pointer-events-none z-0 overflow-visible">
            {edges.map((edge, i) => {
              const sourceNode = nodes.find(n => n.id === edge.from);
              const targetNode = nodes.find(n => n.id === edge.to);
              if (!sourceNode || !targetNode) return null;
              
              // Apply +1000 offset because SVG is shifted by -1000px
              const x1 = sourceNode.x + 48 + 1000;
              const y1 = sourceNode.y + 48 + 1000;
              const x2 = targetNode.x + 48 + 1000;
              const y2 = targetNode.y + 48 + 1000;
              
              // Calculate midpoint for label
              const midX = (x1 + x2) / 2;
              const midY = (y1 + y2) / 2;
              const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;

              return (
                <g key={i}>
                  <line 
                    x1={x1} y1={y1} x2={x2} y2={y2} 
                    stroke="#52525b" strokeWidth="2" strokeDasharray="5,5" 
                  />
                  <text 
                    x={midX} y={midY - 5} 
                    fill="#a1a1aa" fontSize="12px" textAnchor="middle"
                    transform={`rotate(${angle > 90 || angle < -90 ? angle + 180 : angle}, ${midX}, ${midY})`}
                  >
                    {edge.label}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Dynamic Nodes */}
          {nodes.map(node => {
            const colorClass = TYPE_COLORS[node.type] || TYPE_COLORS['Concept'];
            return (
              <div 
                key={node.id}
                className={`node-element absolute w-24 h-24 rounded-full border-2 flex flex-col items-center justify-center shadow-lg shadow-black/50 z-10 hover:scale-110 transition-transform cursor-pointer pointer-events-auto backdrop-blur-md ${colorClass}`}
                style={{ left: `${node.x}px`, top: `${node.y}px` }}
                title={`${node.label} (${node.type})`}
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedNode(node);
                }}
              >
                <div className="text-center p-2">
                  <div className="text-xs font-bold line-clamp-2 leading-tight">{node.label}</div>
                  <div className="text-[10px] opacity-70 mt-1">{node.type}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Overlay Panel: Stats */}
      <div className="absolute bottom-12 left-12 bg-md-sys-color-surface-variant/90 backdrop-blur-md p-4 rounded-lg border border-md-sys-color-outline-variant min-w-[200px] z-20 pointer-events-none shadow-xl">
        <h3 className="font-bold mb-2 flex items-center gap-2 text-md-sys-color-on-surface">
          <span className="material-symbols-outlined text-sm">info</span>
          Graph Statistics
        </h3>
        <p className="text-sm text-md-sys-color-secondary mb-1">Total Entities: <span className="text-md-sys-color-primary font-bold">{nodes.length}</span></p>
        <p className="text-sm text-md-sys-color-secondary">Relationships: <span className="text-md-sys-color-primary font-bold">{edges.length}</span></p>
      </div>

      {/* Attribute Inspector Panel */}
      {selectedNode && (
        <div className="absolute top-32 right-12 bg-md-sys-color-surface-variant/95 backdrop-blur-md p-6 rounded-xl border border-md-sys-color-outline-variant w-[320px] z-30 shadow-2xl animate-[slideInRight_0.2s_ease-out]">
          <div className="flex justify-between items-start mb-4 border-b border-md-sys-color-outline-variant pb-2">
            <div>
              <h3 className="font-bold text-lg text-md-sys-color-on-surface">{selectedNode.label}</h3>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${TYPE_COLORS[selectedNode.type] || TYPE_COLORS['Concept']}`}>
                {selectedNode.type}
              </span>
            </div>
            <button 
              onClick={() => setSelectedNode(null)}
              className="material-symbols-outlined text-md-sys-color-secondary hover:text-white transition-colors"
            >
              close
            </button>
          </div>
          
          <div className="space-y-4 max-h-[400px] overflow-y-auto">
            <div>
              <div className="text-xs text-md-sys-color-secondary mb-1">ID</div>
              <div className="text-sm font-mono bg-black/30 p-2 rounded text-md-sys-color-primary truncate" title={selectedNode.id}>
                {selectedNode.id}
              </div>
            </div>

            {selectedNode.attributes && Object.keys(selectedNode.attributes).length > 0 ? (
              <div className="space-y-2">
                <div className="text-xs text-md-sys-color-secondary font-bold tracking-wider mb-2">ATTRIBUTES</div>
                {Object.entries(selectedNode.attributes).map(([key, val]) => (
                  <div key={key} className="bg-black/20 p-2 rounded border border-white/5">
                    <div className="text-xs text-md-sys-color-secondary capitalize">{key.replace('_', ' ')}</div>
                    <div className="text-sm mt-0.5">{String(val)}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-md-sys-color-secondary italic">No dynamic attributes available.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
