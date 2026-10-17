import { useMemo, useState } from 'react'
import { api } from '../../api/client'
import { Icon } from '../../components/Icon'
import { EmptyState, Modal, PageHeader } from '../../components/Ui'
import { formatDate, statuses, today } from '../../utils/formatters'

function ApplicationForm({ companies, token, mutate, onClose }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  async function submit(event) {
    event.preventDefault(); setBusy(true); setError('')
    try {
      await mutate(() => api('/applications/', { method: 'POST', token, body: Object.fromEntries(new FormData(event.currentTarget)) }), 'Application added.')
      onClose()
    } catch (requestError) { setError(requestError.message) } finally { setBusy(false) }
  }
  return <form className="modal-form" onSubmit={submit}>
    {!companies.length && <p className="form-error">Create a company first, then add an application.</p>}
    <label>Company<select name="company_id" required defaultValue="" disabled={!companies.length}><option value="" disabled>Select a company</option>{companies.map((company) => <option key={company.id} value={company.id}>{company.name}</option>)}</select></label>
    <label>Role<input name="role" required placeholder="Software Engineer Intern" /></label>
    <label>Application date<input name="application_date" type="date" required defaultValue={today()} /></label>
    {error && <p className="form-error">{error}</p>}
    <div className="modal-actions"><button type="button" className="button secondary" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy || !companies.length}>{busy ? 'Adding...' : 'Add application'}</button></div>
  </form>
}

export function ApplicationsView({ data, token, mutate, setSection }) {
  const [createOpen, setCreateOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('All')
  const applications = useMemo(() => data.applications.filter((app) => (status === 'All' || app.status === status) && `${app.company.name} ${app.role}`.toLowerCase().includes(query.toLowerCase())), [data.applications, query, status])
  async function changeStatus(id, next) { await mutate(() => api(`/applications/${id}/status`, { method: 'PATCH', token, body: { status: next } }), 'Status updated.') }
  async function remove(id) { if (window.confirm('Delete this application? This cannot be undone.')) await mutate(() => api(`/applications/${id}`, { method: 'DELETE', token }), 'Application deleted.') }
  const emptyAction = <button className="button secondary" onClick={() => data.companies.length ? setCreateOpen(true) : setSection('companies')}>{data.companies.length ? 'Add application' : 'Create company'}</button>
  return <div className="page">
    <PageHeader eyebrow="OPPORTUNITIES" title="Applications" description={`${data.applications.length} opportunities in your tracker.`} action={<button className="button primary" onClick={() => setCreateOpen(true)}><Icon name="plus"/> Add application</button>}/>
    <section className="toolbar"><label className="search"><Icon name="search"/><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search companies or roles" /></label><select value={status} onChange={(event) => setStatus(event.target.value)}><option>All</option>{statuses.map((item) => <option key={item}>{item}</option>)}</select></section>
    {applications.length ? <section className="table-card"><table><thead><tr><th>Company & role</th><th>Applied</th><th>Status</th><th>Update stage</th><th/></tr></thead><tbody>{applications.map((app) => <tr key={app.id}><td><div className="company-cell"><span className="company-initial">{app.company.name[0]}</span><div><strong>{app.company.name}</strong><small>{app.role}</small></div></div></td><td>{formatDate(app.application_date)}</td><td><span className={`status-pill ${app.status.toLowerCase()}`}>{app.status}</span></td><td><select className="stage-select" value={app.status} onChange={(event) => changeStatus(app.id, event.target.value)}>{statuses.map((item) => <option key={item}>{item}</option>)}</select></td><td><button className="icon-button danger" onClick={() => remove(app.id)} title="Delete application"><Icon name="trash"/></button></td></tr>)}</tbody></table></section> : <EmptyState title="Nothing matches yet" description={data.companies.length ? 'Try a different search, or add a new application.' : 'Add a company before you create your first application.'} action={emptyAction}/>}
    {createOpen && <Modal title="Add an application" onClose={() => setCreateOpen(false)}><ApplicationForm companies={data.companies} token={token} mutate={mutate} onClose={() => setCreateOpen(false)}/></Modal>}
  </div>
}
