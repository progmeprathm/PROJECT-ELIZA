import React from 'react';

export default function Benchmarks() {
  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Performance Benchmarks</h1>
        <p className="text-md-sys-color-secondary">Historical cognitive performance metrics.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Metric 1 */}
        <div className="bg-md-sys-color-surface-variant p-6 rounded-xl border border-md-sys-color-outline-variant">
          <h2 className="text-sm font-bold text-md-sys-color-secondary tracking-widest mb-4">PLANNING SUCCESS RATE</h2>
          <div className="flex items-end gap-4 mb-6">
            <span className="text-5xl font-bold text-ecos-success">94%</span>
            <span className="text-sm text-md-sys-color-secondary mb-1">Over last 30 days</span>
          </div>
          <div className="flex items-end h-32 gap-2 mt-4 pt-4 border-t border-md-sys-color-outline-variant">
            {/* Mock Bar Chart */}
            {[40, 60, 50, 80, 90, 85, 94].map((h, i) => (
              <div key={i} className="flex-1 bg-ecos-success/20 rounded-t hover:bg-ecos-success transition-colors cursor-crosshair" style={{ height: `${h}%` }}></div>
            ))}
          </div>
        </div>

        {/* Metric 2 */}
        <div className="bg-md-sys-color-surface-variant p-6 rounded-xl border border-md-sys-color-outline-variant">
          <h2 className="text-sm font-bold text-md-sys-color-secondary tracking-widest mb-4">AVG. COGNITIVE LATENCY</h2>
          <div className="flex items-end gap-4 mb-6">
            <span className="text-5xl font-bold text-md-sys-color-tertiary">1.2s</span>
            <span className="text-sm text-md-sys-color-secondary mb-1">Per LLM Inference</span>
          </div>
          <div className="flex items-end h-32 gap-2 mt-4 pt-4 border-t border-md-sys-color-outline-variant">
            {/* Mock Bar Chart */}
            {[20, 25, 22, 30, 28, 25, 20].map((h, i) => (
              <div key={i} className="flex-1 bg-md-sys-color-tertiary/20 rounded-t hover:bg-md-sys-color-tertiary transition-colors cursor-crosshair" style={{ height: `${h}%` }}></div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
