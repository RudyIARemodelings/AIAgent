from config import Config


class ConvosoEndpoints:
    CONVOSO_TOKEN=Config.CONVOSO_TOKEN
    USER_ENDPOINT = 'https://api.convoso.com/v1/users/search'
    CALL_LOGS_ENDPOINT = 'https://api.convoso.com/v1/log/retrieve'

    LEADS_SEARCH_ENDPOINT = 'https://api.convoso.com/v1/leads/search'