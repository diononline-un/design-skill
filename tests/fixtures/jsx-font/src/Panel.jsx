export function Panel({ code }) {
  return (
    <div style={{ fontFamily: "'Source Sans 3', system-ui, sans-serif", padding: '8px 12px', borderRadius: 4 }}>
      <code style={{ fontFamily: 'monospace', letterSpacing: '.15em', wordBreak: 'break-all' }}>{code}</code>
      <pre style={{fontFamily:"monospace",padding:'4px 8px',borderRadius:4}}>{code}</pre>
    </div>
  );
}
