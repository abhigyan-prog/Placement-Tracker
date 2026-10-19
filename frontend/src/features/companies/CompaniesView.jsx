import { useState } from 'react'
import { api } from '../../api/client'
import { Icon } from '../../components/Icon'
import { EmptyState, Modal, PageHeader } from '../../components/Ui'

function CompanyForm({ company, token, mutate, onClose }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')

    const values = Object.fromEntries(new FormData(event.currentTarget))
    values.website = values.website || null
    values.industry = values.industry || null

    try {
      const method = company ? 'PATCH' : 'POST'
      const path = company ? `/companies/${company.id}` : '/companies/'
      await mutate(
        () => api(path, { method, token, body: values }),
        company ? 'Company updated.' : 'Company added.',
      )
      onClose()
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setBusy(false)
    }
  }

  return <form className="modal-form" onSubmit={submit}>
    <label>Company name<input name="name" required placeholder="Figma" defaultValue={company?.name ?? ''}/></label>
    <label>Website <span className="optional">optional</span><input name="website" type="url" placeholder="https://figma.com" defaultValue={company?.website ?? ''}/></label>
    <label>Industry <span className="optional">optional</span><input name="industry" placeholder="Product design" defaultValue={company?.industry ?? ''}/></label>
    {error && <p className="form-error">{error}</p>}
    <div className="modal-actions"><button className="button secondary" type="button" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy}>{busy ? 'Saving...' : company ? 'Save changes' : 'Add company'}</button></div>
  </form>
}

export function CompaniesView({ data, token, mutate }) {
  const [formOpen, setFormOpen] = useState(false)
  const [companyToEdit, setCompanyToEdit] = useState(null)
  async function remove(id) { if (window.confirm('Delete this company? Companies with applications cannot be deleted.')) await mutate(() => api(`/companies/${id}`, { method: 'DELETE', token }), 'Company deleted.') }

  function closeForm() {
    setFormOpen(false)
    setCompanyToEdit(null)
  }

  function editCompany(company) {
    setCompanyToEdit(company)
    setFormOpen(true)
  }

  const emptyAction = <button className="button primary" onClick={() => setFormOpen(true)}><Icon name="plus"/> Add company</button>
  return <div className="page"><PageHeader eyebrow="YOUR NETWORK" title="Companies" description="Keep every target company organised in one place." action={emptyAction}/>
    {data.companies.length ? <section className="company-grid">{data.companies.map((company) => { const count = data.applications.filter((app) => app.company_id === company.id).length; return <article className="company-card" key={company.id}><div className="company-card-top"><span className="company-initial">{company.name[0]}</span><div className="card-actions"><button className="icon-button" onClick={() => editCompany(company)} title="Edit company" aria-label={`Edit ${company.name}`}><Icon name="edit"/></button><button className="icon-button danger" onClick={() => remove(company.id)} title="Delete company" aria-label={`Delete ${company.name}`}><Icon name="trash"/></button></div></div><h2>{company.name}</h2><p>{company.industry || 'Industry not set'}</p><div className="company-meta"><span>{count} application{count === 1 ? '' : 's'}</span>{company.website && <a href={company.website} target="_blank" rel="noreferrer">Visit site</a>}</div></article> })}</section> : <EmptyState title="Build your company list" description="Add organisations first, then attach applications and notes to them." action={emptyAction}/>}
    {formOpen && <Modal title={companyToEdit ? 'Edit company' : 'Add a company'} onClose={closeForm}><CompanyForm key={companyToEdit?.id ?? 'new'} company={companyToEdit} token={token} mutate={mutate} onClose={closeForm}/></Modal>}
  </div>
}
