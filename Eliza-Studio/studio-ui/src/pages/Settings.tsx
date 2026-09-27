import React from 'react';

export default function Settings() {
  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">System Settings</h1>
        <p className="text-md-sys-color-secondary">Configure ECOS Kernel parameters and integrations.</p>
      </header>

      <div className="max-w-[600px] flex flex-col gap-6">
        <div className="bg-md-sys-color-surface-variant p-6 rounded-xl border border-md-sys-color-outline-variant">
          <h2 className="font-bold mb-4 border-b border-md-sys-color-outline-variant pb-2">Cognitive Models</h2>
          
          <div className="mb-4">
            <label className="block text-xs font-bold text-md-sys-color-secondary tracking-widest mb-2">PRIMARY CLOUD MODEL (LITELLM)</label>
            <input type="text" defaultValue="huggingface/HuggingFaceH4/zephyr-7b-beta" className="w-full bg-md-sys-color-surface border border-md-sys-color-outline-variant rounded p-2 text-sm focus:border-md-sys-color-primary outline-none" />
          </div>

          <div className="mb-4">
            <label className="block text-xs font-bold text-md-sys-color-secondary tracking-widest mb-2">LOCAL FALLBACK MODEL (OLLAMA)</label>
            <input type="text" defaultValue="ollama/llama3" className="w-full bg-md-sys-color-surface border border-md-sys-color-outline-variant rounded p-2 text-sm focus:border-md-sys-color-primary outline-none" />
          </div>
        </div>

        <div className="bg-md-sys-color-surface-variant p-6 rounded-xl border border-md-sys-color-outline-variant">
          <h2 className="font-bold mb-4 border-b border-md-sys-color-outline-variant pb-2">Persistence</h2>
          
          <div className="flex items-center justify-between">
            <div>
              <div className="font-bold">Clear Cognitive Memory</div>
              <div className="text-sm text-md-sys-color-secondary">Wipes the SQLite database (ecos.db).</div>
            </div>
            <button className="bg-md-sys-color-error text-md-sys-color-on-error px-4 py-2 rounded font-bold hover:opacity-90">
              Nuke DB
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
