from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, verification, risk_assessment, investment_analysis

from database import SessionLocal, Analysis

app = FastAPI(title="Financial Document Analyzer")


# -----------------------------
# Background Worker
# -----------------------------
def run_crew_background(task_id: str, query: str, file_path: str):

    db = SessionLocal()

    try:
        financial_crew = Crew(
            agents=[
                verifier,
                financial_analyst,
                risk_assessor,
                investment_advisor,
            ],
            tasks=[
                verification,
                analyze_financial_document,
                risk_assessment,
                investment_analysis,
            ],
            process=Process.sequential,
        )

        result = financial_crew.kickoff(
            inputs={"query": query, "file_path": file_path}
        )

        record = db.query(Analysis).filter(
            Analysis.task_id == task_id
        ).first()

        record.status = "completed"
        record.result = str(result)

        db.commit()

    except Exception as e:
        record = db.query(Analysis).filter(
            Analysis.task_id == task_id
        ).first()

        record.status = "failed"
        record.error = str(e)

        db.commit()

    finally:
        db.close()

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


# -----------------------------
# Routes
# -----------------------------
@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_financial_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(
        default="Analyze this financial document for investment insights"
    ),
):

    task_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{task_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        db = SessionLocal()

        new_record = Analysis(
            task_id=task_id,
            status="processing",
            file_name=file.filename,
            query=query.strip(),
        )

        db.add(new_record)
        db.commit()
        db.close()

        # Queue execution
        background_tasks.add_task(
            run_crew_background,
            task_id,
            query.strip(),
            file_path,
        )

        return {
            "status": "success",
            "message": "Task added to queue successfully",
            "task_id": task_id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}",
        )


@app.get("/status/{task_id}")
async def get_task_status(task_id: str):

    db = SessionLocal()

    record = db.query(Analysis).filter(
        Analysis.task_id == task_id
    ).first()

    db.close()

    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": record.task_id,
        "status": record.status,
        "file_name": record.file_name,
        "query": record.query,
        "result": record.result,
        "error": record.error,
    }


# -----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)