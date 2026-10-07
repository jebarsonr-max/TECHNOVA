import React from 'react';

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

export class ErrorBoundary extends React.Component<{ children: React.ReactNode }, State> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    this.setState({ errorInfo });
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          backgroundColor: '#090d16',
          color: '#f1f5f9',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          fontFamily: 'monospace',
        }}>
          <div style={{
            maxWidth: '720px',
            width: '100%',
            background: 'rgba(239,68,68,0.08)',
            border: '1px solid rgba(239,68,68,0.3)',
            borderRadius: '1rem',
            padding: '2rem',
          }}>
            <h1 style={{ color: '#f87171', fontSize: '1.25rem', marginBottom: '1rem' }}>
              âš ï¸ React App Crashed
            </h1>
            <p style={{ color: '#fca5a5', marginBottom: '1rem', fontSize: '0.875rem' }}>
              {this.state.error?.message}
            </p>
            <pre style={{
              background: '#0f172a',
              borderRadius: '0.5rem',
              padding: '1rem',
              fontSize: '0.75rem',
              color: '#94a3b8',
              overflowX: 'auto',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-all',
            }}>
              {this.state.error?.stack}
            </pre>
            {this.state.errorInfo && (
              <pre style={{
                background: '#0f172a',
                borderRadius: '0.5rem',
                padding: '1rem',
                marginTop: '1rem',
                fontSize: '0.75rem',
                color: '#64748b',
                overflowX: 'auto',
                whiteSpace: 'pre-wrap',
              }}>
                {this.state.errorInfo.componentStack}
              </pre>
            )}
            <button
              onClick={() => window.location.reload()}
              style={{
                marginTop: '1.5rem',
                padding: '0.5rem 1.25rem',
                background: '#0891b2',
                color: 'white',
                borderRadius: '0.5rem',
                border: 'none',
                cursor: 'pointer',
                fontSize: '0.875rem',
              }}
            >
              Reload App
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
