NAME_REGEX = "[A-Z][a-z]* [A-Z][a-z]*"
NAME_SLASH_REGEX = "[A-Z][a-z]*/[A-Z][a-z]*"
NAME_HASHTAG_REGEX = "#[A-Z][a-z]*[ .,]"
HOST_REGEX = f"host {NAME_REGEX}"

OPENING_MONOLOGUE_REGEX = f"{NAME_REGEX}.*(?i:opening monologue)"

EMOJI_REGEX = r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001F004-\U0001F0CF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F]+"

EMOJI_UNICODE_REGEX = r"\\u[0-9a-fA-F]{4}"

TOKENIZER_REGEX = r"\S+|\s"

AWARDS_REGEX = [
    r"(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?",
    r"[lL]ifetime [aA]chievement [aA]ward",
]

AWARDS_VALIDATION_REGEX = [
    r"(?:won|wins|winning|takes home|takes|gets|got|getting) (?:the\s)?(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?",
    r"(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)? (?:goes to|is awarded to)",
    r"[lL]ifetime [aA]chievement [aA]ward",
]

NOMINEES_REGEX = [
    r"{Winner}.* beat .*([A-Z][a-z]+ [A-Z][a-z]+)",
    r"{Winner}.* over .*([A-Z][a-z]+ [A-Z][a-z]+)",
    r"{Winner}.*snub.*([A-Z][a-z]+ [A-Z][a-z]+)",
    r"{Winner}.* [won|win] .*([A-Z][a-z]+ [A-Z][a-z]+)",
    r"{Winner}.*([A-Z][a-z]+ [A-Z][a-z]+)",
    r"([A-Z][a-z]+ [A-Z][a-z]+).*{Winner}",
]

PRESENTERS_REGEX = r"\b[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+\b\s+(presenting|presents|present|announces|announce|introduces|introducing|intros|announcer|announcers)"

WINNERS_REGEX = [r'[A-Z][a-zA-Z\s]*[A-Z][a-z]*', #Regex to find names of person winners
                          r'for ([A-Z][a-z]*\s)+']

FILM_REGEX = r'for ([A-Z][a-z]*\s)+'
PERSON_REGEX = r'[A-Z][a-z]*[A-Z][a-z]*'
MOVIE_REGEX = r"[A-Za-z0-9\s'\"&!@$%^*()_+=\[\]{};:,.<>?/\-\\]+"