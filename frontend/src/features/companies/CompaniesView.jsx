import { useState } from 'react'
import { api } from '../../api/client'
import { Icon } from '../../components/Icon'
import { EmptyState, Modal, PageHeader } from '../../components/Ui'

function CompanyForm({ token, mutate, onClose }) {
  const [busy, setBusy] = useState(false); const [error, setError] = useState('')
  async function submit(event) { event.preventDefault(); setBusy(true); setError(''); try { await mutate(() => api('/companies/', { method: 'POST', token, body: Object.fromEntries(new FormData(event.currentTarget)) }), 'Company added.'); onClose() } catch (requestError) { setError(requestError.message) } finally { setBusy(false) } }
  return <form className="modal-form" onSubmit={submit}><label>Company name<input name="name" required placeholder="Figma"/></label><label>Website <span className="optional">optional</span><input name="website" type="url" placeholder="https://figma.com"/></label><label>Industry <span className="optional">optional</span><input name="industry" placeholder="Product design"/></label>{error && <p className="form-error">{error}</p>}<div className="modal-actions"><button className="button secondary" type="button" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy}>{busy ? 'Adding...' : 'Add company'}</button></div></form>
}

export function CompaniesView({ data, token, mutate }) {
  const [open, setOpen] = useState(false)
  async function remove(id) { if (window.confirm('Delete this company? Companies with applications cannot be deleted.')) await mutate(() => api(`/companies/${id}`, { method: 'DELETE', token }), 'Company deleted.') }
  const emptyAction = <button className="button primary" onClick={() => setOpen(true)}><Icon name="plus"/> Add company</button>
  return <div className="page"><PageHeader eyebrow="YOUR NETWORK" title="Companies" description="Keep every target company organised in one place." action={emptyAction}/>
    {data.companies.length ? <section className="company-grid">{data.companies.map((company) => { const count = data.applications.filter((app) => app.company_id === company.id).length; return <article className="company-card" key={company.id}><div className="company-card-top"><span className="company-initial">{company.name[0]}</span><button className="icon-button danger" onClick={() => remove(company.id)} title="Delete company"><Icon name="trash"/></button></div><h2>{company.name}</h2><p>{company.industry || 'Industry not set'}</p><div className="company-meta"><span>{count} application{count === 1 ? '' : 's'}</span>{company.website && <a href={company.website} target="_blank" rel="noreferrer">Visit site</a>}</div></article> })}</section> : <EmptyState title="Build your company list" description="Add organisations first, then attach applications and notes to them." action={emptyAction}/>}
    {open && <Modal title="Add a company" onClose={() => setOpen(false)}><CompanyForm token={token} mutate={mutate} onClose={() => setOpen(false)}/></Modal>}
  </div>
}
