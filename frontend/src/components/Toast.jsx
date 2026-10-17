import { useEffect } from 'react'
export function Toast({ message, tone, onClose }) { useEffect(() => { const timer = setTimeout(onClose, 3500); return () => clearTimeout(timer) }, [onClose]); return <div className={`toast ${tone}`} role="status">{message}<button onClick={onClose}>×</button></div> }
