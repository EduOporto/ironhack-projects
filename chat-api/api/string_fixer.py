
## Library that fixes any string for it can be inserted as a parameter in and endpoint 
## or the inverse: it can be inserted to the database as a clean string

def string_fixer(string, to_db=False):
    if to_db == True:
        string = string.replace("_", " ")
        return string
    else:
        string = string.replace(" ", "_").replace("'", "")
        return string