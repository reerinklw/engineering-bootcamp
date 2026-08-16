export interface MediaAsset {
    id: string;
    filename: string;
    sizeBytes: number;
    mimeType: string;
    metadata: Record<string, string>;
  }
  
  export const MAX_EXPORT_SIZE = 104857600; // 100MB

// filter an array of assets to remove anything over MAX_EXPORT_SIZE and sort them by size descending
export const filterAssets = (assets: MediaAsset[]) => {
  return assets.filter(asset => asset.sizeBytes <= MAX_EXPORT_SIZE).sort((a, b) => b.sizeBytes - a.sizeBytes);
};  

