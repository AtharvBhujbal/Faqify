IS_SUCCESS = {
    "DATABASE_INITIALIZED": {"code": "db_init", "message": "Database initialized successfully"},
    "FAQ_CREATED": {"code": "faq_create", "message": "FAQ created successfully"},
    "FAQ_FETCHED": {"code": "faq_fetch", "message": "FAQ fetched successfully"},
    "FAQ_DELETED": {"code": "faq_delete", "message": "FAQ deleted successfully"},
}

IS_ERROR = {
    "ERR_DATABASE_INITIALIZATION": {"code": "db_init", "message": "Database initialization failed"},
    "ERR_FAQ_CREATE": {"code": "faq_create", "message": "FAQ creation failed"},
    "ERR_FAQ_FETCH": {"code": "faq_fetch", "message": "FAQ fetch failed"},
    "ERR_FAQ_NOT_FOUND": {"code": "faq_not_found", "message": "FAQ not found"},
    "ERR_FAQ_DELETE": {"code": "faq_delete", "message": "FAQ deletion failed"},
    "ERR_FAQ_INVALID_LANG": {"code": "faq_invalid_lang", "message": "Invalid Language"},
}


STATUS = {
    "INTERNAL_SERVER_ERROR": 500,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "OK": 200,
}

IND_LANGUAGES = {
    "English":"en",
    "Hindi":"hi",
    "Kannada":"kn",
    "Tamil":"ta",
    "Telugu":"te",
    "Bengali":"bn",
    "Malayalam":"ml",
    "Gujarati":"gu",
    "Marathi":"mr",
    "Punjabi":"pa",
}