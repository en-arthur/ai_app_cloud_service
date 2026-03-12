from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.storage import Storage
from typing import List, Optional
import uuid
from datetime import datetime

class StorageService:
    @staticmethod
    def create(db: Session, app_id: uuid.UUID, user_id: uuid.UUID, collection: str, data: dict) -> Storage:
        """Create a new storage item"""
        item = Storage(
            id=uuid.uuid4(),
            app_id=app_id,
            user_id=user_id,
            collection=collection,
            data=data
        )
        
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    
    @staticmethod
    def list(db: Session, app_id: uuid.UUID, user_id: uuid.UUID, collection: str) -> List[Storage]:
        """List all items in a collection for a user"""
        return db.query(Storage).filter(
            and_(
                Storage.app_id == app_id,
                Storage.user_id == user_id,
                Storage.collection == collection
            )
        ).order_by(Storage.created_at.desc()).all()
    
    @staticmethod
    def get(db: Session, app_id: uuid.UUID, user_id: uuid.UUID, collection: str, item_id: uuid.UUID) -> Optional[Storage]:
        """Get a single item"""
        return db.query(Storage).filter(
            and_(
                Storage.id == item_id,
                Storage.app_id == app_id,
                Storage.user_id == user_id,
                Storage.collection == collection
            )
        ).first()
    
    @staticmethod
    def update(db: Session, app_id: uuid.UUID, user_id: uuid.UUID, collection: str, item_id: uuid.UUID, data: dict) -> Optional[Storage]:
        """Update an item"""
        item = StorageService.get(db, app_id, user_id, collection, item_id)
        
        if not item:
            return None
        
        item.data = data
        item.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(item)
        return item
    
    @staticmethod
    def delete(db: Session, app_id: uuid.UUID, user_id: uuid.UUID, collection: str, item_id: uuid.UUID) -> bool:
        """Delete an item"""
        item = StorageService.get(db, app_id, user_id, collection, item_id)
        
        if not item:
            return False
        
        db.delete(item)
        db.commit()
        return True
    
    @staticmethod
    def batch_create(db: Session, app_id: uuid.UUID, user_id: uuid.UUID, collection: str, items: List[dict]) -> List[Storage]:
        """Create multiple items at once"""
        storage_items = []
        
        for data in items:
            item = Storage(
                id=uuid.uuid4(),
                app_id=app_id,
                user_id=user_id,
                collection=collection,
                data=data
            )
            storage_items.append(item)
        
        db.add_all(storage_items)
        db.commit()
        
        for item in storage_items:
            db.refresh(item)
        
        return storage_items
    
    @staticmethod
    def batch_delete(db: Session, app_id: uuid.UUID, user_id: uuid.UUID, collection: str, item_ids: List[uuid.UUID]) -> int:
        """Delete multiple items at once"""
        deleted = db.query(Storage).filter(
            and_(
                Storage.id.in_(item_ids),
                Storage.app_id == app_id,
                Storage.user_id == user_id,
                Storage.collection == collection
            )
        ).delete(synchronize_session=False)
        
        db.commit()
        return deleted
