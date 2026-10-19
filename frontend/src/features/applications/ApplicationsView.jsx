import { useMemo, useState } from 'react'
import { api } from '../../api/client'
import { Icon } from '../../components/Icon'
import { EmptyState, Modal, PageHeader } from '../../components/Ui'
import { formatDate, statuses, today } from '../../utils/formatters'

function ApplicationForm({ application, companies, resumes, token, mutate, onClose }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')

    const values = Object.fromEntries(new FormData(event.currentTarget))
    values.resume_id = values.resume_id || null

    try {
      const method = application ? 'PATCH' : 'POST'
      const path = application ? `/applications/${application.id}` : '/applications/'
      await mutate(
        () => api(path, { method, token, body: values }),
        application ? 'Application updated.' : 'Application added.',
      )
      onClose()
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setBusy(false)
    }
  }

  return <form className="modal-form" onSubmit={submit}>
    {!companies.length && <p className="form-error">Create a company first, then add an application.</p>}
    <label>Company<select name="company_id" required defaultValue={application?.company_id ?? ''} disabled={!companies.length}><option value="" disabled>Select a company</option>{companies.map((company) => <option key={company.id} value={company.id}>{company.name}</option>)}</select></label>
    <label>Role<input name="role" required placeholder="Software Engineer Intern" defaultValue={application?.role ?? ''}/></label>
    <label>Application date<input name="application_date" type="date" required defaultValue={application?.application_date ?? today()}/></label>
    <label>Resume <span className="optional">optional</span><select name="resume_id" defaultValue={application?.resume_id ?? ''}><option value="">No resume selected</option>{resumes.map((resume) => <option key={resume.id} value={resume.id}>{resume.version_name}</option>)}</select></label>
    {error && <p className="form-error">{error}</p>}
    <div className="modal-actions"><button type="button" className="button secondary" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy || !companies.length}>{busy ? 'Saving...' : application ? 'Save changes' : 'Add application'}</button></div>
  </form>
}

export function ApplicationsView({ data, token, mutate, setSection }) {
  const [formOpen, setFormOpen] = useState(false)
  const [applicationToEdit, setApplicationToEdit] = useState(null)
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('All')
  const applications = useMemo(() => data.applications.filter((app) => (status === 'All' || app.status === status) && `${app.company.name} ${app.role}`.toLowerCase().includes(query.toLowerCase())), [data.applications, query, status])

  function closeForm() {
    setFormOpen(false)
    setApplicationToEdit(null)
  }

  function editApplication(application) {
    setApplicationToEdit(application)
    setFormOpen(true)
  }

  async function changeStatus(id, next) {
    await mutate(() => api(`/applications/${id}/status`, { method: 'PATCH', token, body: { status: next } }), 'Status updated.')
  }

  async function remove(id) {
    if (window.confirm('Delete this application? This cannot be undone.')) {
      await mutate(() => api(`/applications/${id}`, { method: 'DELETE', token }), 'Application deleted.')
    }
  }

  const emptyAction = <button className="button secondary" onClick={() => data.companies.length ? setFormOpen(true) : setSection('companies')}>{data.companies.length ? 'Add application' : 'Create company'}</button>

  return <div className="page">
    <PageHeader eyebrow="OPPORTUNITIES" title="Applications" description={`${data.applications.length} opportunities in your tracker.`} action={<button className="button primary" onClick={() => setFormOpen(true)}><Icon name="plus"/> Add application</button>}/>
    <section className="toolbar"><label className="search"><Icon name="search"/><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search companies or roles" /></label><select value={status} onChange={(event) => setStatus(event.target.value)}><option>All</option>{statuses.map((item) => <option key={item}>{item}</option>)}</select></section>
    {applications.length ? <section className="table-card"><table><thead><tr><th>Company & role</th><th>Applied</th><th>Status</th><th>Update stage</th><th/></tr></thead><tbody>{applications.map((app) => {
      const resume = data.resumes.find((item) => item.id === app.resume_id)
      return <tr key={app.id}><td><div className="company-cell"><span className="company-initial">{app.company.name[0]}</span><div><strong>{app.company.name}</strong><small>{app.role}{resume ? ` · ${resume.version_name}` : ''}</small></div></div></td><td>{formatDate(app.application_date)}</td><td><span className={`status-pill ${app.status.toLowerCase()}`}>{app.status}</span></td><td><select className="stage-select" value={app.status} onChange={(event) => changeStatus(app.id, event.target.value)}>{statuses.map((item) => <option key={item}>{item}</option>)}</select></td><td><div className="card-actions"><button className="icon-button" onClick={() => editApplication(app)} title="Edit application" aria-label={`Edit ${app.role} at ${app.company.name}`}><Icon name="edit"/></button><button className="icon-button danger" onClick={() => remove(app.id)} title="Delete application" aria-label={`Delete ${app.role} at ${app.company.name}`}><Icon name="trash"/></button></div></td></tr>
    })}</tbody></table></section> : <EmptyState title="Nothing matches yet" description={data.companies.length ? 'Try a different search, or add a new application.' : 'Add a company before you create your first application.'} action={emptyAction}/>}
    {formOpen && <Modal title={applicationToEdit ? 'Edit application' : 'Add an application'} onClose={closeForm}><ApplicationForm key={applicationToEdit?.id ?? 'new'} application={applicationToEdit} companies={data.companies} resumes={data.resumes} token={token} mutate={mutate} onClose={closeForm}/></Modal>}
  </div>
}
