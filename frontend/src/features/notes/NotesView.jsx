import { useState } from 'react'
import { api } from '../../api/client'
import { Icon } from '../../components/Icon'
import { EmptyState, Modal, PageHeader } from '../../components/Ui'
import { formatDate } from '../../utils/formatters'

const types = [['general', 'General'], ['interview_prep', 'Interview prep'], ['oa_prep', 'OA prep'], ['company_specific', 'Company specific']]

function NoteForm({ note, data, token, mutate, onClose }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')

    const values = Object.fromEntries(new FormData(event.currentTarget))
    values.application_id = values.application_id || null
    values.company_id = values.company_id || null

    try {
      const method = note ? 'PATCH' : 'POST'
      const path = note ? `/notes/${note.id}` : '/notes/'
      await mutate(
        () => api(path, { method, token, body: values }),
        note ? 'Note updated.' : 'Note saved.',
      )
      onClose()
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setBusy(false)
    }
  }

  return <form className="modal-form" onSubmit={submit}>
    <label>Title<input name="title" required placeholder="What I want to prepare" defaultValue={note?.title ?? ''}/></label>
    <label>Note type<select name="note_type" defaultValue={note?.note_type ?? 'general'}>{types.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
    <label>Link to application <span className="optional">optional</span><select name="application_id" defaultValue={note?.application_id ?? ''}><option value="">No application</option>{data.applications.map((app) => <option key={app.id} value={app.id}>{app.company.name} - {app.role}</option>)}</select></label>
    <label>Link to company <span className="optional">optional</span><select name="company_id" defaultValue={note?.company_id ?? ''}><option value="">No company</option>{data.companies.map((company) => <option key={company.id} value={company.id}>{company.name}</option>)}</select></label>
    <label>Details<textarea name="content" required rows="5" placeholder="Questions, reminders, resources..." defaultValue={note?.content ?? ''}/></label>
    {error && <p className="form-error">{error}</p>}
    <div className="modal-actions"><button className="button secondary" type="button" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy}>{busy ? 'Saving...' : note ? 'Save changes' : 'Save note'}</button></div>
  </form>
}

export function NotesView({ data, token, mutate }) {
  const [formOpen, setFormOpen] = useState(false)
  const [noteToEdit, setNoteToEdit] = useState(null)

  function closeForm() {
    setFormOpen(false)
    setNoteToEdit(null)
  }

  function editNote(note) {
    setNoteToEdit(note)
    setFormOpen(true)
  }

  async function remove(id) { if (window.confirm('Delete this note?')) await mutate(() => api(`/notes/${id}`, { method: 'DELETE', token }), 'Note deleted.') }
  const emptyAction = <button className="button primary" onClick={() => setFormOpen(true)}><Icon name="plus"/> New note</button>
  return <div className="page">
    <PageHeader eyebrow="PREPAREDNESS" title="Notes" description="Capture questions, research, and interview preparation." action={emptyAction}/>
    {data.notes.length ? <section className="notes-grid">{data.notes.map((note) => {
      const application = data.applications.find((item) => item.id === note.application_id)
      const company = data.companies.find((item) => item.id === note.company_id)
      const links = [application && `${application.company.name} · ${application.role}`, company?.name].filter(Boolean)
      return <article className="note-card" key={note.id}>
        <div className="note-card-head"><span className="note-type">{types.find(([value]) => value === note.note_type)?.[1]}</span><div className="card-actions"><button className="icon-button" onClick={() => editNote(note)} title="Edit note" aria-label={`Edit ${note.title}`}><Icon name="edit"/></button><button className="icon-button danger" onClick={() => remove(note.id)} title="Delete note" aria-label={`Delete ${note.title}`}><Icon name="trash"/></button></div></div>
        <h2>{note.title}</h2>
        {links.length > 0 && <p className="note-links">{links.join(' · ')}</p>}
        <p>{note.content}</p><footer>Last updated {formatDate(note.updated_at)}</footer>
      </article>
    })}</section> : <EmptyState title="Save the details that matter" description="Keep interview preparation, OA resources, and company research close at hand." action={emptyAction}/>}
    {formOpen && <Modal title={noteToEdit ? 'Edit note' : 'Create a note'} onClose={closeForm}><NoteForm key={noteToEdit?.id ?? 'new'} note={noteToEdit} data={data} token={token} mutate={mutate} onClose={closeForm}/></Modal>}
  </div>
}
