import React from 'react';
import { Header } from './components/Header';
import { LegacyMediaCard } from './components/LegacyMediaCard';
import { filterAssets, MediaAsset } from './lib/assetfilters';
import { AdobeTheme } from './lib/theme';

const mockAssets: MediaAsset[] = [
  {
    id: 'asset-001',
    filename: 'sunset-beach.jpg',
    sizeBytes: 2457600,
    mimeType: 'image/jpeg',
    metadata: { location: 'California' },
  },
  {
    id: 'asset-002',
    filename: 'product-hero.png',
    sizeBytes: 1048576,
    mimeType: 'image/png',
    metadata: { campaign: 'Q3-launch' },
  },
  {
    id: 'asset-003',
    filename: 'team-photo.jpg',
    sizeBytes: 3145728,
    mimeType: 'image/jpeg',
    metadata: { department: 'Engineering' },
  },
];

export const App = () => {
  const assets = filterAssets(mockAssets);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: AdobeTheme.colors.surface }}>
      <Header />
      <main
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: AdobeTheme.spacing.md,
          padding: AdobeTheme.spacing.lg,
        }}
      >
        {assets.map((asset) => (
          <LegacyMediaCard key={asset.id} asset={asset} />
        ))}
      </main>
    </div>
  );
};
