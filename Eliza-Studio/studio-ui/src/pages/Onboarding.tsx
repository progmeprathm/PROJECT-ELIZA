import React from 'react';

const personas = [
  { id: 'Researcher', icon: 'science', color: 'bg-md-sys-color-primary-container text-md-sys-color-primary', desc: 'Literature review, hypothesis generation, and experimental design.' },
  { id: 'Engineer', icon: 'code', color: 'bg-md-sys-color-tertiary-container text-md-sys-color-tertiary', desc: 'Architecture planning, implementation, testing, and deployment.' },
  { id: 'Founder', icon: 'rocket_launch', color: 'bg-ecos-success-container text-ecos-success', desc: 'Market research, product roadmaps, and execution tracking.' },
  { id: 'Student', icon: 'school', color: 'bg-ecos-warning-container text-ecos-warning', desc: 'Mastery tracking, topic exploration, and practice plans.' },
];

export default function Onboarding({ setPersona }: { setPersona: (p: string) => void }) {
  return (
    <div className="w-full h-screen bg-md-sys-color-background text-md-sys-color-on-background flex flex-col items-center justify-center p-6 overflow-y-auto">
      <div className="max-w-[800px] w-full flex flex-col gap-8 animate-[fadeIn_0.4s_ease-out]">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-3">Welcome to ELIZA.</h1>
          <p className="text-lg text-md-sys-color-secondary">What are you trying to achieve today?</p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
          {personas.map(p => (
            <div 
              key={p.id}
              onClick={() => {
                localStorage.setItem('eliza_persona', p.id);
                setPersona(p.id);
              }}
              className="flex flex-col gap-3 p-6 rounded-xl border border-md-sys-color-outline-variant bg-md-sys-color-surface-variant hover:bg-[#27272a] cursor-pointer transition-colors"
            >
              <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${p.color}`}>
                <span className="material-symbols-outlined">{p.icon}</span>
              </div>
              <h3 className="font-bold text-lg">{p.id}</h3>
              <p className="text-sm text-md-sys-color-secondary">{p.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
