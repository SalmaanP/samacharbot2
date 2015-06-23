import praw
import re
from re import findall
import config



def deletemsg():

    r = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
    r.login(config.uname, config.passwd)
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

                if msg.author.name == comment_parent.link_author or msg.author.name == 'sallurocks':
                    comment_parent.delete()
                    print "deletedd"
                    #deleted += 1
                    #msg.reply('I have deleted [my comment]('+comment.permalink+'), which was reply to your [this comment]('+comment_parent.permalink+').\n\nHave an amazing day, '+str(msg.author.name)+'!\n\n-AutoWikibot')
                    #success("DELETION AT %s" % comment_parent.id)
                    msg.mark_as_read()
                else:
                    #msg.reply('Oops, only /u/'+str(comment_parent.author.name)+' can delete that [comment]('+comment.permalink+'). Downvote the comment if you think it is not helping.\n\nHave an amazing day, '+str(msg.author.name)+'!\n\n-AutoWikibot')
                    #fail("BAD DELETE REQUEST BY /u/%s" % str(msg.author.name))
                    msg.mark_as_read()
                continue
            except Exception as e:

                if str(e) == "'NoneType' object has no attribute 'name'":
                    comment = r.get_info(thing_id=idd)
                    parentid = comment.parent_id
                    comment_parent.delete()
                    print "deleted"
                    #deleted += 1
                    #msg.reply('[My comment]('+comment.permalink+') which was reply to [this comment]('+comment_parent.permalink+') is also found orphan. I have deleted it as requested.\n\nHave an amazing day, '+str(msg.author.name)+'!\n\n-AutoWikibot')
                    #success("DELETION (ORPHAN) AT %s" % comment_parent.id)
                else:
                    print "5Unknown ERROR"
                    print type(e)
                    print e.args
                    print e
                    print "\n"
                    continue
                msg.mark_as_read()
                continue


if __name__ == '__main__':
    deletemsg()