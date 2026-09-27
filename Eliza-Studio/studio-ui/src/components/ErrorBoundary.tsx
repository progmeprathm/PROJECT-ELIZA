import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  errorMsg: string;
}

export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    errorMsg: ''
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, errorMsg: error.message };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center h-full w-full bg-md-sys-color-background text-md-sys-color-on-background p-6">
          <div className="text-ecos-warning mb-4">
            <span className="material-symbols-outlined text-5xl">warning</span>
          </div>
          <h1 className="text-2xl font-bold mb-2">Cognitive Core Dump</h1>
          <p className="text-md-sys-color-secondary mb-4 text-center max-w-[500px]">
            The ELIZA UI encountered an unexpected rendering exception.
          </p>
          <div className="bg-md-sys-color-surface-variant p-4 rounded border border-md-sys-color-outline-variant font-mono text-sm text-md-sys-color-error w-full max-w-[600px] overflow-auto mb-6">
            {this.state.errorMsg}
          </div>
          <button 
            className="bg-md-sys-color-primary text-md-sys-color-on-primary px-4 py-2 rounded font-bold hover:opacity-90"
            onClick={() => window.location.reload()}
          >
            Reboot Interface
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
