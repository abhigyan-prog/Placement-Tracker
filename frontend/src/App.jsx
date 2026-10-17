import { useEffect, useState } from 'react'
import { api } from './api/client'
import { AppShell } from './components/AppShell'
import { AuthScreen } from './components/AuthScreen'
import { Toast } from './components/Toast'
import { usePlacementData } from './hooks/usePlacementData'
import { ApplicationsView } from './features/applications/ApplicationsView'
import { CompaniesView } from './features/companies/CompaniesView'
import { DashboardView } from './features/dashboard/DashboardView'
import { NotesView } from './features/notes/NotesView'
import { ResumesView } from './features/resumes/ResumesView'
import { SettingsView } from './features/settings/SettingsView'

const views = { dashboard: DashboardView, applications: ApplicationsView, companies: CompaniesView, notes: NotesView, resumes: ResumesView, settings: SettingsView }

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem('placement_token'))
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('placement_user') || 'null'))
  const [section, setSection] = useState('dashboard')
  const [toast, setToast] = useState(null)
  const { data, error, loading, refresh } = usePlacementData(token)

  useEffect(() => {
    if (!token || user) return
    api('/auth/me', { token }).then((profile) => setProfile(profile)).catch(logout)
  }, [token, user])

  function setProfile(profile) { setUser(profile); localStorage.setItem('placement_user', JSON.stringify(profile)) }
  function notify(message, tone = 'success') { setToast({ message, tone }) }
  function logout() { localStorage.removeItem('placement_token'); localStorage.removeItem('placement_user'); setToken(null); setUser(null); setSection('dashboard') }
  function login(nextToken, profile) { localStorage.setItem('placement_token', nextToken); setToken(nextToken); setProfile(profile); notify(`Welcome back, ${profile.full_name.split(' ')[0]}.`) }
  async function mutate(action, successMessage) {
    try { const result = await action(); await refresh(); if (successMessage) notify(successMessage); return result }
    catch (requestError) { notify(requestError.message, 'error'); throw requestError }
  }

  if (!token || !user) return <AuthScreen onLogin={login} />
  const ActiveView = views[section]
  return <AppShell activeSection={section} onNavigate={setSection} onLogout={logout} user={user}>
    <ActiveView data={data} token={token} loading={loading} error={error} mutate={mutate} refresh={refresh} notify={notify} setSection={setSection} user={user} setUser={setProfile}/>
    {toast && <Toast {...toast} onClose={() => setToast(null)} />}
  </AppShell>
}
