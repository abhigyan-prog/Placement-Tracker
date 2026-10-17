import { Icon } from './Icon'
import { initials } from '../utils/formatters'
const navigation = [['dashboard', 'Overview', 'grid'], ['applications', 'Applications', 'briefcase'], ['companies', 'Companies', 'building'], ['notes', 'Notes', 'note'], ['resumes', 'Resumes', 'file'], ['settings', 'Settings', 'settings']]

export function AppShell({ activeSection, onNavigate, onLogout, user, children }) {
  return <div className="app-shell"><aside className="sidebar"><button className="brand" onClick={() => onNavigate('dashboard')}><span className="brand-mark">P</span><span>Placeboard</span></button><nav className="nav-list" aria-label="Main navigation">{navigation.map(([id, label, icon]) => <button key={id} className={`nav-item ${activeSection === id ? 'active' : ''}`} onClick={() => onNavigate(id)}><Icon name={icon}/><span>{label}</span></button>)}</nav><div className="sidebar-footer"><div className="profile-row"><span className="avatar">{initials(user.full_name)}</span><div><strong>{user.full_name}</strong><small>{user.email}</small></div></div><button className="icon-button" title="Sign out" onClick={onLogout}><Icon name="logout" /></button></div></aside><main className="content">{children}</main></div>
}
