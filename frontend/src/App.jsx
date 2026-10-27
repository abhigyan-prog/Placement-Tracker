import { useEffect, useState } from 'react'
import { Navigate, Outlet, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import { api } from './api/client'
import { AppShell } from './components/AppShell'
import { AuthScreen } from './components/AuthScreen'
import { Toast } from './components/Toast'
import { LoadingBlock } from './components/Ui'
import { usePlacementData } from './hooks/usePlacementData'
import { ApplicationsView } from './features/applications/ApplicationsView'
import { CompaniesView } from './features/companies/CompaniesView'
import { DashboardView } from './features/dashboard/DashboardView'
import { NotesView } from './features/notes/NotesView'
import { ResumesView } from './features/resumes/ResumesView'
import { SettingsView } from './features/settings/SettingsView'

const views = { dashboard: DashboardView, applications: ApplicationsView, companies: CompaniesView, notes: NotesView, resumes: ResumesView, settings: SettingsView }
const sectionPaths = Object.fromEntries(Object.keys(views).map((section) => [section, `/${section}`]))

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem('placement_token'))
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('placement_user') || 'null'))
  const [toast, setToast] = useState(null)
  const { data, error, loading, refresh } = usePlacementData(token)
  const location = useLocation()
  const navigate = useNavigate()
  const authLoading = Boolean(token && !user)

  useEffect(() => {
    if (!token || user) return

    let isCurrent = true
    api('/auth/me', { token })
      .then((profile) => {
        if (isCurrent) setProfile(profile)
      })
      .catch(() => {
        if (isCurrent) logout()
      })

    return () => {
      isCurrent = false
    }
  }, [token, user])

  function setProfile(profile) { setUser(profile); localStorage.setItem('placement_user', JSON.stringify(profile)) }
  function notify(message, tone = 'success') { setToast({ message, tone }) }
  function logout() { localStorage.removeItem('placement_token'); localStorage.removeItem('placement_user'); setToken(null); setUser(null) }
  function login(nextToken, profile) {
    localStorage.setItem('placement_token', nextToken)
    setToken(nextToken)
    setProfile(profile)
    notify(`Welcome back, ${profile.full_name.split(' ')[0]}.`)
    const requestedPath = location.state?.from?.pathname
    const destination = Object.values(sectionPaths).includes(requestedPath) ? requestedPath : sectionPaths.dashboard
    navigate(destination, { replace: true })
  }
  function navigateSection(section) {
    const path = sectionPaths[section]
    if (path) navigate(path)
  }
  async function mutate(action, successMessage) {
    try { const result = await action(); await refresh(); if (successMessage) notify(successMessage); return result }
    catch (requestError) { notify(requestError.message, 'error'); throw requestError }
  }

  const activePath = location.pathname.replace(/\/+$/, '') || '/'
  const activeSection = Object.entries(sectionPaths).find(([, path]) => path === activePath)?.[0] || 'dashboard'
  const authPage = (mode) => {
    if (authLoading) return <LoadingBlock />
    if (token && user) return <Navigate to={sectionPaths.dashboard} replace />
    return <AuthScreen mode={mode} onLogin={login} />
  }

  return <>
    <Routes>
      <Route path="/" element={<Navigate to={token && user ? sectionPaths.dashboard : '/login'} replace />} />
      <Route path="/login" element={authPage('login')} />
      <Route path="/register" element={authPage('register')} />
      <Route element={token && user
        ? <AppShell activeSection={activeSection} onNavigate={navigateSection} onLogout={logout} user={user}><Outlet /></AppShell>
        : authLoading
          ? <LoadingBlock />
          : <Navigate to="/login" state={{ from: location }} replace />}>
        {Object.entries(views).map(([section, View]) => <Route key={section} path={sectionPaths[section]} element={
          <View data={data} token={token} loading={loading} error={error} mutate={mutate} refresh={refresh} notify={notify} setSection={navigateSection} user={user} setUser={setProfile} />
        } />)}
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    {toast && <Toast {...toast} onClose={() => setToast(null)} />}
  </>
}
