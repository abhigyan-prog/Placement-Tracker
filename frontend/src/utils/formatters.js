export const statuses = ['Applied', 'OA', 'Interview', 'Offer', 'Rejected']
export const today = () => new Date().toISOString().slice(0, 10)
export const initials = (name = '') => name.split(' ').filter(Boolean).slice(0, 2).map((part) => part[0]).join('').toUpperCase() || 'U'
export function formatDate(value, options = { month: 'short', day: 'numeric', year: 'numeric' }) { return value ? new Intl.DateTimeFormat('en-IN', options).format(new Date(`${value.slice(0, 10)}T00:00:00`)) : '—' }
