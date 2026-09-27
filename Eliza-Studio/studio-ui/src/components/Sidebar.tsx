import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const navItems = [
  { name: 'Home', icon: 'home', path: '/' },
  { name: 'Workspace', icon: 'dashboard', path: '/workspace/current' },
  { name: 'Chat', icon: 'forum', path: '/chat' },
  { name: 'Goals', icon: 'track_changes', path: '/goals' },
  { name: 'Memory', icon: 'memory', path: '/memory' },
  { name: 'World Model', icon: 'public', path: '/world' },
  { name: 'Planner', icon: 'account_tree', path: '/planner' },
  { name: 'Simulation', icon: 'science', path: '/simulation' },
  { name: 'Projects', icon: 'folder', path: '/projects' },
  { name: 'Knowledge', icon: 'menu_book', path: '/knowledge' },
  { name: 'Skills', icon: 'psychology', path: '/skills' },
  { name: 'Agents', icon: 'group', path: '/agents' },
  { name: 'Marketplace', icon: 'storefront', path: '/marketplace' },
  { name: 'Benchmarks', icon: 'speed', path: '/benchmarks' },
  { name: 'Settings', icon: 'settings', path: '/settings' },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <aside className="w-[240px] bg-md-sys-color-surface-variant border-r border-md-sys-color-outline-variant flex flex-col h-full shrink-0">
      <div className="p-4 border-b border-md-sys-color-outline-variant flex items-center gap-2 cursor-pointer hover:text-md-sys-color-primary transition-colors" onClick={() => navigate('/')}>
        <span className="material-symbols-outlined text-md-sys-color-primary">bolt</span>
        <span className="font-bold tracking-widest text-lg">ELIZA</span>
      </div>
      
      <nav className="flex-1 overflow-y-auto py-2">
        <ul className="flex flex-col gap-1 px-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
            return (
              <li key={item.name}>
                <button
                  onClick={() => navigate(item.path)}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive 
                      ? 'bg-md-sys-color-primary-container text-md-sys-color-primary' 
                      : 'text-md-sys-color-secondary hover:bg-md-sys-color-surface hover:text-md-sys-color-on-surface'
                  }`}
                >
                  <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
                  {item.name}
                </button>
              </li>
            );
          })}
        </ul>
      </nav>
      
      <div className="p-4 border-t border-md-sys-color-outline-variant">
        <div className="flex items-center gap-2 text-xs text-md-sys-color-secondary">
          <span className="w-2 h-2 rounded-full bg-ecos-success"></span>
          Kernel Online
        </div>
      </div>
    </aside>
  );
}
