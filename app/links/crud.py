from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas


def get_link(db: Session, short_id: str):
    return db.query(models.Link).filter(
        models.Link.short_id == short_id
    ).first()


def create_link(db: Session, link: schemas.LinkCreate):
    db_link = models.Link(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def update_link(db: Session, link: schemas.LinkUpdate):
    db_link = get_link(db, link.short_id)
    db_link.
    return db_link
