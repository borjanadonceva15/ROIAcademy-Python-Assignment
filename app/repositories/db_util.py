from sqlalchemy.exc import SQLAlchemyError

from app import db
"""Utility functions that interact with the database using SQLAlchemy"""


def save_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving data: {e}")
        raise

    except SQLAlchemyError as e:
        db.session.rollback()
        raise "Failed to save data" from e



def delete_data(data):
    try:
        db.session.delete(data)
        db.session.commit()
    except:
        db.session.rollback()
        raise


def flush_and_commit_changes():
    try:
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        raise


def rollback_and_close():
    try:
        db.session.rollback()
        db.session.close()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
