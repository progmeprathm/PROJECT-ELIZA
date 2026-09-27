import React from 'react';

export default function Goals() {
  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Global Goals</h1>
        <p className="text-md-sys-color-secondary">Hierarchical task management and strategic objectives.</p>
      </header>

      <div className="flex gap-6 h-full">
        {/* Board Column 1 */}
        <div className="flex-1 bg-md-sys-color-surface-variant rounded-xl p-4 border border-md-sys-color-outline-variant flex flex-col gap-4">
          <h2 className="font-bold flex items-center justify-between">
            Active
            <span className="bg-md-sys-color-surface px-2 py-1 rounded-full text-xs">1</span>
          </h2>
          <div className="bg-md-sys-color-surface p-4 rounded-lg border-l-4 border-md-sys-color-primary cursor-pointer hover:opacity-80">
            <h3 className="font-bold mb-2">Build ECOS Kernel</h3>
            <div className="w-full bg-md-sys-color-surface-variant h-2 rounded-full mb-2">
              <div className="bg-md-sys-color-primary h-full rounded-full w-[85%]"></div>
            </div>
            <div className="flex justify-between text-xs text-md-sys-color-secondary">
              <span>Phase 3 Integration</span>
              <span>85%</span>
            </div>
          </div>
        </div>

        {/* Board Column 2 */}
        <div className="flex-1 bg-md-sys-color-surface-variant rounded-xl p-4 border border-md-sys-color-outline-variant flex flex-col gap-4 opacity-70">
          <h2 className="font-bold flex items-center justify-between">
            Backlog
            <span className="bg-md-sys-color-surface px-2 py-1 rounded-full text-xs">2</span>
          </h2>
          <div className="bg-md-sys-color-surface p-4 rounded-lg border-l-4 border-md-sys-color-secondary">
            <h3 className="font-bold mb-2">Build Vision Module</h3>
            <div className="text-xs text-md-sys-color-secondary">Waiting for LLM multi-modal integration</div>
          </div>
          <div className="bg-md-sys-color-surface p-4 rounded-lg border-l-4 border-md-sys-color-secondary">
            <h3 className="font-bold mb-2">Dockerize Deployment</h3>
            <div className="text-xs text-md-sys-color-secondary">DevOps task</div>
          </div>
        </div>
      </div>
    </div>
  );
}
