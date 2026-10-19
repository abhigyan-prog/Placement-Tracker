import { useState } from 'react'
import { api } from '../../api/client'
import { Icon } from '../../components/Icon'
import { EmptyState, Modal, PageHeader } from '../../components/Ui'
import { formatDate } from '../../utils/formatters'

function UploadForm({ token, mutate, onClose }) {
  const [busy, setBusy] = useState(false); const [error, setError] = useState('')
  async function submit(event) { event.preventDefault(); setBusy(true); try { await mutate(() => api('/resumes/', { method: 'POST', token, body: new FormData(event.currentTarget) }), 'Resume uploaded.'); onClose() } catch (requestError) { setError(requestError.message) } finally { setBusy(false) } }
  return <form className="modal-form" onSubmit={submit}><label>Version name<input name="version_name" required placeholder="Product roles - October 2026" /></label><label>PDF file<input name="file" type="file" accept="application/pdf" required /></label><p className="field-hint">PDF only, up to 5 MB.</p>{error && <p className="form-error">{error}</p>}<div className="modal-actions"><button className="button secondary" type="button" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy}>{busy ? 'Uploading...' : 'Upload resume'}</button></div></form>
}

function RenameResumeForm({ resume, token, mutate, onClose }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    const values = Object.fromEntries(new FormData(event.currentTarget))

    try {
      await mutate(
        () => api(`/resumes/${resume.id}`, { method: 'PATCH', token, body: values }),
        'Resume name updated.',
      )
      onClose()
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setBusy(false)
    }
  }

  return <form className="modal-form" onSubmit={submit}>
    <label>Version name<input name="version_name" required maxLength="255" defaultValue={resume.version_name}/></label>
    {error && <p className="form-error">{error}</p>}
    <div className="modal-actions"><button className="button secondary" type="button" onClick={onClose}>Cancel</button><button className="button primary" disabled={busy}>{busy ? 'Saving...' : 'Save changes'}</button></div>
  </form>
}

export function ResumesView({ data, token, mutate, notify }) {
  const [open, setOpen] = useState(false)
  const [resumeToRename, setResumeToRename] = useState(null)
  const [previewResume, setPreviewResume] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [previewLoading, setPreviewLoading] = useState(false)
  const [previewError, setPreviewError] = useState('')
  const [downloadingId, setDownloadingId] = useState(null)

  async function activate(id) { await mutate(() => api(`/resumes/${id}/activate`, { method: 'PATCH', token }), 'Active resume updated.') }
  async function remove(id) { if (window.confirm('Delete this resume?')) await mutate(() => api(`/resumes/${id}`, { method: 'DELETE', token }), 'Resume deleted.') }

  async function preview(resume) {
    setPreviewResume(resume)
    setPreviewUrl('')
    setPreviewError('')
    setPreviewLoading(true)

    try {
      const access = await api(`/resumes/${resume.id}/signed-url`, { token })
      setPreviewUrl(access.url)
    } catch (requestError) {
      setPreviewError(requestError.message)
    } finally {
      setPreviewLoading(false)
    }
  }

  async function download(resume) {
    setDownloadingId(resume.id)

    try {
      const access = await api(`/resumes/${resume.id}/signed-url?download=true`, { token })
      window.location.assign(access.url)
    } catch (requestError) {
      notify(requestError.message, 'error')
    } finally {
      setDownloadingId(null)
    }
  }

  function closePreview() {
    setPreviewResume(null)
    setPreviewUrl('')
    setPreviewError('')
  }

  function closeRenameForm() {
    setResumeToRename(null)
  }

  const emptyAction = <button className="button primary" onClick={() => setOpen(true)}><Icon name="plus"/> Upload resume</button>
  return <div className="page">
    <PageHeader eyebrow="YOUR MATERIALS" title="Resumes" description="Keep versions ready and mark the one you are currently using." action={emptyAction}/>
    {data.resumes.length ? <section className="resume-list">{data.resumes.map((resume) => <article className={`resume-card ${resume.is_active ? 'active' : ''}`} key={resume.id}>
      <span className="resume-icon"><Icon name="file" size={22}/></span>
      <div className="resume-info"><div><h2>{resume.version_name}</h2>{resume.is_active && <span className="active-badge">Active version</span>}</div><p>Uploaded {formatDate(resume.uploaded_at)}</p></div>
      <div className="resume-actions">
        <button className="button secondary" onClick={() => preview(resume)}>Preview</button>
        <button className="button secondary" onClick={() => download(resume)} disabled={downloadingId === resume.id}>{downloadingId === resume.id ? 'Preparing...' : 'Download'}</button>
        {!resume.is_active && <button className="button secondary" onClick={() => activate(resume.id)}>Make active</button>}
        <button className="button secondary" onClick={() => setResumeToRename(resume)}>Rename</button>
        <button className="icon-button danger" onClick={() => remove(resume.id)} title="Delete resume" aria-label={`Delete ${resume.version_name}`}><Icon name="trash"/></button>
      </div>
    </article>)}</section> : <EmptyState title="No resumes uploaded" description="Upload a PDF to keep your latest version on hand." action={emptyAction}/>}
    {open && <Modal title="Upload a resume" onClose={() => setOpen(false)}><UploadForm token={token} mutate={mutate} onClose={() => setOpen(false)}/></Modal>}
    {resumeToRename && <Modal title="Rename resume" onClose={closeRenameForm}><RenameResumeForm key={resumeToRename.id} resume={resumeToRename} token={token} mutate={mutate} onClose={closeRenameForm}/></Modal>}
    {previewResume && <Modal title={previewResume.version_name} onClose={closePreview} wide>
      <div className="resume-preview">
        {previewLoading && <p className="resume-preview-message">Preparing preview...</p>}
        {previewError && <p className="form-error">{previewError}</p>}
        {previewUrl && <iframe title={`Preview of ${previewResume.version_name}`} src={previewUrl} referrerPolicy="no-referrer"/>}
      </div>
    </Modal>}
  </div>
}
