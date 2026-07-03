# CyberFlow IDS API Demo Runbook

Use this runbook to record optional Step 8 demo media.

## Demo Script (60-90 seconds)

1. Open terminal in project root.
2. Start server:

```bash
c:/Users/user/cyberflow_ids/.venv/Scripts/python.exe -m uvicorn src.app:app --host 0.0.0.0 --port 8000
```

3. In a second terminal, run:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/metadata
```

4. Send one `/predict` request using features payload.
5. Show JSON prediction response in terminal.
6. Stop server.

## Recording Tips

- Capture both terminals side by side if possible.
- Keep font large enough to read commands and JSON output.
- Save as `cyberflow_api_demo.mp4` or `cyberflow_api_demo.gif`.
