import fs from 'fs';
import path from 'path';
import express, { Request, Response } from 'express';

const app = express();
const PORT = process.env.PORT || 8080;

function resolveDistPath(): string {
  if (process.env.STATIC_DIR) {
    return process.env.STATIC_DIR;
  }

  const candidates = [
    path.join(__dirname, '../../dist'),
    path.join(__dirname, '../dist'),
  ];

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return candidates[0];
}

const distPath = resolveDistPath();

app.use(express.json());
app.use(express.static(distPath));

app.post('/api/export', (_req: Request, res: Response) => {
  res.status(200).json({
    success: true,
    zipUrl: 'https://cdn.example.com/exports/batch-export-20260815.zip',
  });
});

app.get('*', (_req: Request, res: Response) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Export server listening on port ${PORT}`);
  console.log(`Serving static assets from ${distPath}`);
});
