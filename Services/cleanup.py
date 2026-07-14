from sqlalchemy import func,text
from Core.database import session
import logging
from Model.model import ChatMessages

logger=logging.getLogger(__name__)

def cleanup_inactive_chats():
    try:
        db=session()

        inactive_session=(db.query(ChatMessages.session_id).group_by(ChatMessages.session_id).having(
            func.max(ChatMessages.created_at)< func.now()-text("INTERVAL '15 minutes'")
        ).all()
        )
        inactive_session=[s[0] for s in inactive_session]

        if inactive_session:
            (
                db.query(ChatMessages).filter(ChatMessages.session_id.in_(inactive_session)).delete(synchronize_session=False))
            db.commit()

        logger.info("Successfully deleted inactive chats")
        
    except Exception:
        db.rollback()
        logger.exception("Failed to retrieve the chats")

    finally:
        db.close()

    