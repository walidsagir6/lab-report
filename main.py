import io
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from weasyprint import HTML

class ReportRequest(BaseModel):
    html_content: str

app = FastAPI()

# Mount your static file directories securely
app.mount("/static", StaticFiles(directory="static"), name="static")
print("Starting FastAPI backend server application...")

@app.get("/")
def read_root():
    with open("lab_report.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, media_type="text/html")

@app.post("/generate_pdf")
def generate_pdf(report_request: ReportRequest):
    # Receives the clean, fully-compiled layout data package string
    live_html = report_request.html_content
    
    # Create an isolated memory buffer stream inside RAM to prevent pipeline collision bugs
    pdf_buffer = io.BytesIO()
    
    # Process string structure directly. base_url="." hooks up local signature graphics perfectly
    HTML(string=live_html, base_url=".").write_pdf(pdf_buffer)
    
    # Reset internal location track index pointer back to zero index
    pdf_buffer.seek(0)
    
    # Fire data block back down to the browser automatically
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": "attachment; filename=lab_report.pdf"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
