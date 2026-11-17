# Screenshots

Referenced by the README. All are real output from one live session (2026-11-16,
A-share closing report), captured from the running UI and the rendered charts.

| File | Content | Size |
|---|---|---|
| `chat-uat.gif` | full chat UAT: new session → type → send → fetch plan → tools → conclusion → K-line (12 s, 11 frames) | 713 KB |
| `01-overview.jpg` | report page: hero, conclusion, six-index KPI strip (change % red/green, everything else black) | 127 KB |
| `02-kline.png` | SSE Composite K-line with MA5/20/60 and volume | 132 KB |
| `03-distribution.png` | market breadth by change bucket | 58 KB |
| `04-turnover.png` | turnover by index | 60 KB |

Budget: images ≤ 300 KB each, GIF ≤ 5 MB. No video: the demo is screenshots + GIF.

The GIF is captured from the real frontend (headless Edge over CDP), not a mockup:
frames are typed input, the fetch-plan card, the tool audit card, the streamed
answer and the chart, assembled into one loop.

Naming: `NN-<layer>.png` where layer is `overview`, `kline`, `distribution`, `turnover`.
