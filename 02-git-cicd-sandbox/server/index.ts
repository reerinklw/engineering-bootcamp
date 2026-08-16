import express from 'express';

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());

app.post('/api/export', (_req, res) => {
  res.status(200).json({
    success: true,
    zipUrl: 'https://cdn.example.com/exports/batch-export-20260815.zip',
  });
});

app.listen(PORT, () => {
  console.log(`Export server listening on port ${PORT}`);
});
