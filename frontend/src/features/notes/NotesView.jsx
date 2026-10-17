import { useState } from 'react'
import { api } from '../../api/client'
import { Icon } from '../../components/Icon'
import { EmptyState, Modal, PageHeader } from '../../components/Ui'
import { formatDate } from '../../utils/formatters'

const types = [['general', 'General'], ['interview_prep', 'Interview prep'], ['oa_prep', 'OA prep'], ['company_specific', 'Company specific']]
function NoteForm({ data, token, mutate, onClose }) {
  const [busy, setBusy] = useState(false); const [error, setError] = useState('')
  async function submit(event) { event.preventDefault(); setBusy(true); const values = Object.fromEntries(new FormData(event.currentTarget)); if (!values.application_id) delete values.application_id; if (!values.company_id) delete values.company_id; try { await mutate(() => api('/notes/', { method: 'POST', token, body: values }), 'Note saved.'); onClose() } catch (requestError) { setError(requestError.message) } finally { setBusy(false) } }
  return <form className="modal-form" onSubmit={submit}><label>Title<input name="title" required placeholder="What I want to prepare" /></label><label>Note type<select name="note_type">{types.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label><label>Link to application <span className="optional">optional</span><select name="application_id" defaultValue=""><option value="">No application</option>{data.applications.map((app) => <option key={app.id} value={app.id}>{app.company.name} - {app.role}</option>)}</select></label><label>Link to company <span className="optional">optional</span><select name="company_id" defaultValue=""><option value="">No company</option>{data.companies.map((company) => <option key={company.id} value={company.id}>{company.name}</option>)}</select></label><label>Details<textarea name="content" required rows="5" placeholder="Questions, reminders, resources..." /></label>{error && <p className="form-error">{error}</p>}<div className="modal-actions"><button className="button secondary" type="button" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy}>{busy ? 'Saving...' : 'Save note'}</button></div></form>
}
export function NotesView({ data, token, mutate }) {
  const [open, setOpen] = useState(false)
  async function remove(id) { if (window.confirm('Delete this note?')) await mutate(() => api(`/notes/${id}`, { method: 'DELETE', token }), 'Note deleted.') }
  const emptyAction = <button className="button primary" onClick={() => setOpen(true)}><Icon name="plus"/> New note</button>
  return <div className="page"><PageHeader eyebrow="PREPAREDNESS" title="Notes" description="Capture questions, research, and interview preparation." action={emptyAction}/>{data.notes.length ? <section className="notes-grid">{data.notes.map((note) => <article className="note-card" key={note.id}><div className="note-card-head"><span className="note-type">{types.find(([value]) => value === note.note_type)?.[1]}</span><button className="icon-button danger" onClick={() => remove(note.id)} title="Delete note"><Icon name="trash"/></button></div><h2>{note.title}</h2><p>{note.content}</p><footer>Last updated {formatDate(note.updated_at)}</footer></article>)}</section> : <EmptyState title="Save the details that matter" description="Keep interview preparation, OA resources, and company research close at hand." action={emptyAction}/>} {open && <Modal title="Create a note" onClose={() => setOpen(false)}><NoteForm data={data} token={token} mutate={mutate} onClose={() => setOpen(false)}/></Modal>}</div>
}
