
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
                    question_trans TEXT,
                    language TEXT,
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

    def create_faq(self, question, answer, question_trans=None, language=None):
        cur = self.db.cursor()
        try:
            query = """
                INSERT INTO faq (question, question_trans, language, answer)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """
            cur.execute(query, (question, question_trans, language, answer))
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
                    SELECT id, question_trans, answer FROM faq WHERE language = '{lang}';
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
                SELECT id, question FROM faq WHERE question_trans IS NULL;
            """
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            logger.error(f"Database Error while Fetching Not Translated FAQs: {e}")
    
    def update_faq(self, faq_id, question, answer, question_trans=None, language=None):
        cur = self.db.cursor()
        try:
            query = """
                UPDATE faq
                SET question = %s, question_trans = %s, language = %s, answer = %s
                WHERE id = %s;
            """
            cur.execute(query, (question, question_trans, language, answer, faq_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error while Updating FAQ: {e}")
            raise 
        finally:
            cur.close()

    def update_translation(self, faq_id, question_trans, language):
        cur = self.db.cursor()
        try:
            query = """
                UPDATE faq
                SET question_trans = %s, language = %s
                WHERE id = %s;
            """
            cur.execute(query, (question_trans, language, faq_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error while Updating Translation: {e}")
            raise 
        finally:
            cur.close()

    def get_translated_lang(self):
        cur = self.db.cursor()
        try:
            query = """
                SELECT language FROM faq WHERE id = 1;
            """
            cur.execute(query)
            return cur.fetchone()[0]
        except Exception as e:
            logger.error(f"Database Error while Fetching Translated Language: {e}")
            raise
        finally:
            cur.close()


db = database()