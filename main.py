from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.alarm import schedule_alarm
from app.ai_parser import parse_alarm_text
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aialarmclock.vercel.app/"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlarmRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "AI Alarm Clock API is running."}

@app.post("/set-alarm")
async def set_alarm(request: AlarmRequest):
    try:
        parsed_alarm = parse_alarm_text(request.text)
        schedule_alarm(parsed_alarm)
        return {
            "status": "success",
            "alarm_time": parsed_alarm.get("time", f"every {parsed_alarm['interval']} {parsed_alarm['unit']}"),
            "reason": parsed_alarm["reason"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ✅ This is critical for Railway to work
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
