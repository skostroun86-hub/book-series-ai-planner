from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PlotPoint, PlotPointCreate
from app.models import PlotPoint as PlotPointModel
import uuid

router = APIRouter()

@router.get("/", response_model=list[PlotPoint])
async def list_plots(book_id: str = None, db: Session = Depends(get_db)):
    """List plot points"""
    query = db.query(PlotPointModel)
    if book_id:
        query = query.filter(PlotPointModel.book_id == book_id)
    return query.all()

@router.post("/", response_model=PlotPoint)
async def create_plot_point(plot: PlotPointCreate, db: Session = Depends(get_db)):
    """Create plot point"""
    db_plot = PlotPointModel(
        id=str(uuid.uuid4()),
        book_id=plot.book_id,
        description=plot.description,
        significance=plot.significance,
        plot_thread=plot.plot_thread,
        chapter_number=plot.chapter_number,
        sequence_order=plot.sequence_order
    )
    db.add(db_plot)
    db.commit()
    db.refresh(db_plot)
    return db_plot

@router.get("/timeline")
async def get_timeline(book_id: str, db: Session = Depends(get_db)):
    """Get timeline view"""
    plots = db.query(PlotPointModel).filter(
        PlotPointModel.book_id == book_id
    ).order_by(PlotPointModel.sequence_order).all()
    return {"timeline": plots}

@router.post("/analyze")
async def analyze_plot(book_id: str, db: Session = Depends(get_db)):
    """Analyze plot coherence"""
    # This would integrate with LLM to analyze plot
    return {"book_id": book_id, "analysis": "Plot analysis coming soon"}
