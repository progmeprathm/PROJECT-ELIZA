import React from 'react';

export default function Marketplace() {
  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold mb-2">Cognitive Marketplace</h1>
          <p className="text-md-sys-color-secondary">Install external plugins, models, and specialized engines.</p>
        </div>
        <div className="bg-md-sys-color-surface-variant rounded flex overflow-hidden border border-md-sys-color-outline-variant">
          <input type="text" placeholder="Search engines..." className="bg-transparent px-4 py-2 outline-none text-sm" />
          <button className="px-4 py-2 hover:bg-md-sys-color-surface transition-colors">
            <span className="material-symbols-outlined text-sm">search</span>
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Item 1 */}
        <div className="bg-md-sys-color-surface-variant p-6 rounded-xl border border-md-sys-color-outline-variant flex flex-col">
          <div className="flex justify-between items-start mb-4">
            <div className="w-12 h-12 bg-ecos-success/20 text-ecos-success rounded-lg flex items-center justify-center">
              <span className="material-symbols-outlined">visibility</span>
            </div>
            <span className="text-xs font-bold bg-md-sys-color-surface px-2 py-1 rounded text-md-sys-color-secondary">v1.2.0</span>
          </div>
          <h2 className="text-lg font-bold mb-1">Vision Engine</h2>
          <p className="text-sm text-md-sys-color-secondary mb-6 flex-1">Allows ELIZA to interpret images, UI mocks, and diagrams.</p>
          <button className="w-full bg-md-sys-color-primary text-md-sys-color-on-primary py-2 rounded font-bold hover:opacity-90 transition-opacity">
            Install Plugin
          </button>
        </div>

        {/* Item 2 */}
        <div className="bg-md-sys-color-surface-variant p-6 rounded-xl border border-md-sys-color-outline-variant flex flex-col">
          <div className="flex justify-between items-start mb-4">
            <div className="w-12 h-12 bg-md-sys-color-tertiary/20 text-md-sys-color-tertiary rounded-lg flex items-center justify-center">
              <span className="material-symbols-outlined">memory</span>
            </div>
            <span className="text-xs font-bold bg-md-sys-color-surface px-2 py-1 rounded text-md-sys-color-secondary">v0.9.beta</span>
          </div>
          <h2 className="text-lg font-bold mb-1">Ollama Local Fallback</h2>
          <p className="text-sm text-md-sys-color-secondary mb-6 flex-1">Connects to localhost:11434 to run LLaMA3 when offline.</p>
          <button className="w-full bg-ecos-success text-[#111] py-2 rounded font-bold" disabled>
            Installed
          </button>
        </div>

      </div>
    </div>
  );
}
