import React, { useState, useEffect } from 'react';

interface Skill {
  id: string;
  name: string;
  description: string;
  endpoint_mock: string;
}

export default function Skills() {
  const [skills, setSkills] = useState<Skill[]>([]);
  
  useEffect(() => {
    fetch('http://localhost:8001/api/skills')
      .then(res => res.json())
      .then(data => setSkills(data))
      .catch(err => console.error(err));
  }, []);

  const installSkill = () => {
    fetch('http://localhost:8001/api/skills', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'new_skill', description: 'A dynamically installed skill' })
    })
    .then(res => res.json())
    .then(data => setSkills([...skills, data]))
    .catch(err => console.error(err));
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold mb-2">Cognitive Skills</h1>
          <p className="text-md-sys-color-secondary">Executable tools and functional capabilities available to ELIZA.</p>
        </div>
        <button onClick={installSkill} className="bg-md-sys-color-primary text-md-sys-color-on-primary px-4 py-2 rounded font-bold hover:opacity-90">
          Install New Skill
        </button>
      </header>

      <div className="bg-md-sys-color-surface-variant rounded-xl border border-md-sys-color-outline-variant overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-md-sys-color-surface">
            <tr>
              <th className="p-4 text-xs tracking-widest text-md-sys-color-secondary font-bold">SKILL NAME</th>
              <th className="p-4 text-xs tracking-widest text-md-sys-color-secondary font-bold">DESCRIPTION</th>
              <th className="p-4 text-xs tracking-widest text-md-sys-color-secondary font-bold">STATUS</th>
            </tr>
          </thead>
          <tbody>
            {skills.map(skill => (
              <tr key={skill.id} className="border-t border-md-sys-color-outline-variant hover:bg-md-sys-color-surface cursor-pointer">
                <td className="p-4 font-bold flex items-center gap-2">
                  <span className="material-symbols-outlined text-md-sys-color-tertiary text-sm">terminal</span>
                  {skill.name}
                </td>
                <td className="p-4 text-sm text-md-sys-color-secondary">{skill.description}</td>
                <td className="p-4"><span className="bg-ecos-success/20 text-ecos-success px-2 py-1 rounded text-xs font-bold">ACTIVE</span></td>
              </tr>
            ))}
            {skills.length === 0 && (
              <tr>
                <td colSpan={3} className="p-4 text-center text-md-sys-color-secondary">No skills installed yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
