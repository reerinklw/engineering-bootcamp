import React from 'react';
import { AdobeTheme } from './theme';

interface LegacyMediaCardProps {
  asset: {
    id: string;
    filename: string;
    sizeBytes: number;
  };
}

export const LegacyMediaCard: React.FC<LegacyMediaCardProps> = ({ asset }) => {
  const styles: { [key: string]: React.CSSProperties } = {
    card: {
      backgroundColor: AdobeTheme.colors.surface,
      padding: AdobeTheme.spacing.md,
      margin: AdobeTheme.spacing.sm,
      borderRadius: AdobeTheme.borderRadius,
      width: '100%',
      maxWidth: 320,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'stretch',
      boxSizing: 'border-box',
      boxShadow: '0 2px 6px rgba(0,0,0,0.04)',
      gap: AdobeTheme.spacing.sm,
    },
    image: {
      width: '100%',
      borderRadius: AdobeTheme.borderRadius,
      objectFit: 'cover',
      minHeight: 120,
      maxHeight: 180,
    },
    filename: {
      color: AdobeTheme.colors.textPrimary,
      fontSize: 16,
      fontWeight: 700,
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
    },
    size: {
      fontSize: 12,
      color: AdobeTheme.colors.textSecondary,
    },
    button: {
      background: AdobeTheme.colors.brandRed,
      color: '#fff',
      border: 'none',
      padding: AdobeTheme.spacing.sm,
      borderRadius: AdobeTheme.borderRadius,
      cursor: 'pointer',
      fontWeight: 600,
      fontSize: 14,
      marginTop: AdobeTheme.spacing.sm,
      transition: 'background 0.15s',
      alignSelf: 'flex-end',
    },
  };

  return (
    <div style={styles.card}>
      <img src={`/thumbnails/${asset.id}.jpg`} alt={asset.filename} style={styles.image} />
      <div style={styles.filename}>
        {asset.filename}
      </div>
      <span style={styles.size}>Size: {asset.sizeBytes}</span>
      <button style={styles.button}>
        Edit Asset
      </button>
    </div>
  );
};

export default LegacyMediaCard;