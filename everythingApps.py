from AppOpener import open, close, give_appnames

# def check_app(app):
#     if app.lower() in give_appnames():
#         return True
#     return False

def check_app(app):
    for a in give_appnames():
        if app.lower() in a.lower():
            return True
    return False

def openApp(app):
    try:
        open(app, match_closest=True, throw_error=True)
        return True
    except:
        return False

def closeApp(app):
    try:
        close(app, match_closest=True, throw_error=True)
        return True
    except:
        return False
