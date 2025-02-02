
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
from app.log import logger

class database:
    def __init__(self):
        self.db = psycopg2.connect(
                    dbname=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT')
                )
        
    def initialize_database(self):
        cur = self.db.cursor()
        try:
            query = """
                DROP TABLE IF EXISTS faq CASCADE;
                CREATE TABLE IF NOT EXISTS faq (
                    id SERIAL PRIMARY KEY,
                    question TEXT NOT NULL,
                    question_hi TEXT,
                    question_bn TEXT,
                    answer TEXT NOT NULL
                );
            """
            cur.execute(query)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error while Initializing: {e}")
            raise 
        finally:
            cur.close()

    def create_faq(self, question, answer, question_hi=None, question_bn=None):
        cur = self.db.cursor()
        try:
            query = """
                INSERT INTO faq (question, question_hi, question_bn, answer)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """
            cur.execute(query, (question, question_hi, question_bn, answer))
            self.db.commit()
            return cur.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error while Creating FAQ: {e}")
            raise 
        finally:
            cur.close()

    def get_faq(self, faq_id):
        cur = self.db.cursor()
        try:
            query = """
                SELECT * FROM faq WHERE id = %s;
            """
            cur.execute(query, (faq_id,))
            return cur.fetchone()
        except Exception as e:
            logger.error(f"Database Error while Fetching FAQ: {e}")
            raise 
        finally:
            cur.close()

    def get_all_faqs(self, lang=None):
        cur = self.db.cursor()
        try:
            if lang:
                query = f"""
                    SELECT id, question_{lang}, answer FROM faq WHERE question_{lang} IS NOT NULL;
                """
            else:
                query = """
                    SELECT id, question, answer FROM faq;
                """
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            logger.error(f"Database Error while Fetching FAQs: {e}")
            raise 
        finally:
            cur.close()

    def get_all_not_translated_faqs(self):
        cur = self.db.cursor()
        try:
            query = """
                SELECT id, question FROM faq WHERE question_hi IS NULL OR question_bn IS NULL;
            """
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            logger.error(f"Database Error while Fetching Not Translated FAQs: {e}")
    
    def update_faq(self, faq_id, question, answer, question_hi=None, question_bn=None):
        cur = self.db.cursor()
        try:
            query = """
                UPDATE faq
                SET question = %s, question_hi = %s, question_bn = %s, answer = %s
                WHERE id = %s;
            """
            cur.execute(query, (question, question_hi, question_bn, answer, faq_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error while Updating FAQ: {e}")
            raise 
        finally:
            cur.close()

    def update_translation(self, faq_id, question_hi, question_bn):
        cur = self.db.cursor()
        try:
            query = """
                UPDATE faq
                SET question_hi = %s, question_bn = %s
                WHERE id = %s;
            """
            cur.execute(query, (question_hi, question_bn, faq_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error while Updating Translation: {e}")
            raise 
        finally:
            cur.close()



db = database()