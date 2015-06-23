import praw
import re
from re import findall



def deletemsg():

    r = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
    r.login("samacharbot2", "prawisverygood")
    unread = r.get_unread(limit=None)
    print "here"
    for msg in unread:
        print msg.body
        if msg.body.lower() == 'delete':
            try:
                print "found one"
                idd = msg.id
                idd = 't1_' + idd
                print idd
                comment = r.get_info(thing_id=idd)
                parentid = comment.parent_id
                print parentid
                comment_parent = r.get_info(thing_id=parentid)
                sublink = comment_parent.link_id
                author1 = r.get_info(thing_id=sublink)
                print author1.author
                print msg.author.name
                if (str(msg.author.name) == str(author1.author)):
                    comment_parent.delete()
                    print "deletedd"

                    msg.mark_as_read()
                else:

                    msg.mark_as_read()
                continue
            except Exception as e:
                print "5Unknown ERROR"
                print type(e)
                print e.args
                print e
                print "\n"
                # continue
                msg.mark_as_read()
                continue


if __name__ == '__main__':
    deletemsg()