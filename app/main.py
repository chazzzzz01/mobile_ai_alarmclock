from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .alarm import schedule_alarm
from .ai_parser import parse_alarm_text
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://alarm-clock-umber.vercel.app",  # ✅ replace with actual deployed frontend domain
        "http://localhost:3000"
    ],
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
            "alarm_time": parsed_alarm.get(
                "time", f"every {parsed_alarm['interval']} {parsed_alarm['unit']}"
            ),
            "reason": parsed_alarm["reason"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
