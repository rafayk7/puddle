def get_db_info():
    uname = ""
    pword = ""
    dbname = ""
    server = ""
    port = 0

    '''
        keys.txt looks like 
            USERNAME=username
            DBNAME=dbname
            PASSWORD=password
            SERVER=server
            PORT=port 
    '''
    
    with open('keys.txt', 'r') as f:
        lines = f.readlines()
        lines = [x.replace('\n', '').split('=')[1] for x in lines]
        uname = lines[0]
        dbname = lines[1]
        pword = lines[2]
        server = lines[3]
        port = lines[4]
    
        return uname, dbname, pword, server, port