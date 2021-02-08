from toolbox import log, load_dict, save_dict

def add_cookie(cookie, username, pathname="Cookie.npy"):
    cookie_dict = {}
    try:
        cookie_dict = load_dict(pathname)
    except:
        pass

    cookie_dict[cookie] = True
    save_dict(pathname=pathname, dict=cookie_dict)

def add_account(username, password, pathname="Account_list.npy"):
    account_dict = {}
    try:
        account_dict = load_dict("Account_list.npy")
    except:
        pass

    account_dict[username] = password
    save_dict(pathname=pathname, dict=account_dict)

def delete_cookie(cookie, pathname="Cookie.npy"):
    Cookie_list = {}
    try:
        Cookie_list = load_dict(pathname)
    except:
        pass
    
    Cookie_list[cookie] = False
    save_dict(pathname=pathname, dict=Cookie_list)
    

def check_cookie(cookie, pathname="Cookie.npy"):
    Cookie_list = {}
    try:
        Cookie_list = load_dict(pathname)
    except:
        pass

    check = Cookie_list.get(cookie, False)
    log("check:", check)
    return check


def check_account(username, password, pathname="Account_list.npy"):
    # Read dict from file.
    Account_list = {}
    try:
        Account_list = load_dict(pathname)
    except:
        pass
        
    user_password = Account_list.get(username, -1)
    log("user and password:", username, password)
    log("True password:", user_password)
    if user_password == password:
        return True
    else:
        return False

def check_account_exist(username, password, pathname="Account_list.npy"):
    # Read dict from file.
    Account_list = {}
    try:
        Account_list = load_dict(pathname)
    except:
        pass

    return Account_list.__contains__(username)