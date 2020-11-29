def string_fixer(string, to_db=False):
    if to_db == True:
        string = string.replace("_", " ")
        return string
    else:
        string = string.replace(" ", "_").replace("'", "")
        return string