from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .alarm import schedule_alarm
from .ai_parser import parse_alarm_text
import os

app = FastAPI()

# ✅ Allow CORS for your frontend domains (deployed + local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← TEMP fix for CORS

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define input model
class AlarmRequest(BaseModel):
    text: str

# ✅ Health check
@app.get("/")
def read_root():
    return {"message": "AI Alarm Clock API is running."}

# ✅ Alarm endpoint
@app.post("/set-alarm")
async def set_alarm(request: AlarmRequest):
    try:
        # 🧠 Parse the text
        parsed_alarm = parse_alarm_text(request.text)

        # ⏰ Schedule alarm
        schedule_alarm(parsed_alarm)

        return {
            "status": "success",
            "alarm_time": parsed_alarm.get(
                "time", f"every {parsed_alarm['interval']} {parsed_alarm['unit']}"
            ),
            "reason": parsed_alarm["reason"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ✅ Run locally
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
