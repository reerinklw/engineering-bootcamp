import React, { useState } from 'react';
import { AdobeTheme } from './theme';

export const Header = () => {
  const [isExporting, setIsExporting] = useState(false);

  const handleBatchExport = async () => {
    setIsExporting(true);
    try {
      const response = await fetch('/api/export', { method: 'POST' });
      if (!response.ok) {
        throw new Error('Export failed');
      }
      const data = await response.json();
      console.log('Export ready:', data.zipUrl);
    } catch (error) {
      console.error('Batch export error:', error);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: AdobeTheme.spacing.md,
        backgroundColor: AdobeTheme.colors.surface,
        borderBottom: `1px solid ${AdobeTheme.colors.textSecondary}`,
      }}
    >
      <h1 style={{ margin: 0, color: AdobeTheme.colors.textPrimary, fontSize: '20px' }}>
        Media Library
      </h1>
      <button
        onClick={handleBatchExport}
        disabled={isExporting}
        style={{
          background: AdobeTheme.colors.brandRed,
          color: '#fff',
          border: 'none',
          borderRadius: AdobeTheme.borderRadius,
          padding: `${AdobeTheme.spacing.sm} ${AdobeTheme.spacing.md}`,
          cursor: isExporting ? 'not-allowed' : 'pointer',
          opacity: isExporting ? 0.7 : 1,
        }}
      >
        {isExporting ? 'Exporting...' : 'Batch Export'}
      </button>
    </header>
  );
};
