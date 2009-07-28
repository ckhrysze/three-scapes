import xmpp

login = 'ckhrysze.programatic' # @gmail.com
pwd   = 'gt5HY^ju7'

cnx = xmpp.Client('gmail.com')
cnx.connect( server=('talk.google.com',5223) )

cnx.auth(login, pwd, 'botty')

cnx.send(
    xmpp.Message( "ckhrysze@gmail.com" ,"Hello World from Python" )
    )
