#!/usr/bin/env python2.6
# -*- encoding: utf-8 -*-

# A Simple emailer script.
# Uses correct encodings for header and body.
#
# Author: Antti Jaakkola <annttu(a)removethis.annttu.fi>
#         Kapsi Internet-käyttäjät ry 2012
#
# This code is released under the public domain without any 
# warranty! Use as you wish.

import textwrap
import smtplib
import email.utils
import time
from email.Header import Header
from email.mime.text import MIMEText

smtpserver = 'mail.domain.tld'
# if your SMTP server requires auth fill smtpuser and smtpauth
# else leave empty
smtpuser = ''
smtppass = ''

sender = 'My name <me@domain.tld>'

## header encoding
header_charset = "iso-8859-1"

def makeMessage(message, subject, to, sender, encoding, charset):
    msg = MIMEText(message.decode(encoding), _subtype='plain',
                    _charset=charset)
    msg['Date'] = email.utils.formatdate(localtime=time.localtime(
                                        float(time.strftime("%s"))))
    # headers are always encoded as header_charset
    msg['Subject'] = Header(unicode(subject, encoding), header_charset)
    sender_name, sender_addr = email.utils.parseaddr(sender)
    sender_name = str(Header(unicode(sender_name), header_charset))
    msg['From'] =  email.utils.formataddr((sender_name,
                                            sender_addr.encode('ascii')))
    recipient_name, recipient_addr = email.utils.parseaddr(to)
    recipient_name = str(Header(unicode(recipient_name), header_charset))
    msg['To'] = email.utils.formataddr((recipient_name, 
                                        recipient_addr.encode('ascii')))
    msg = msg.as_string()
    return str(msg)

def sendmail(message, subject, recipients=[], sender=sender,
             encoding="utf-8", charset="iso-8859-1"):
    """Simple function to send emails easily
    encoding: input string encoding
    charset: output message body charset
    recipient: list of recipient address, formatted as 
            realname <email>, 
            email,
            [realname, email] or
            (realname, email)
    """

    if len(recipients) == 0:
        return False
    if len(message) == 0:
        return False
    message = message.replace("—", " - ")
    message = message.replace("”", "\"")
    message = '\n'.join(textwrap.wrap(message,72))
    session = smtplib.SMTP(smtpserver)
    if smtpuser is not '':
        session.login(smtpuser, smtppass)
    error = ""
    for recipient in recipients:
        if type(recipient) == type([]) or type(recipient) == type(('','')):
            mailaddr = recipient[1]
            recipient = email.utils.formataddr(recipient)
        else:
            realname, mailaddr = email.utils.parseaddr(recipient)

        smtpresult = session.sendmail(sender, [mailaddr], 
                                makeMessage(message, subject, recipient, 
                                sender, encoding, charset))
        if smtpresult:
            for recip in smtpresult.keys():
                error += "Couldn't delivery mail to: %s Error: %s\n" % (
                        recip, smtpresult[recip][0], smtpresult[recip][1])
        else:
            print("Message sent successfully to %s" % recipient)

    session.quit()
    if error != "":
        raise smtplib.SMTPException, error


if __name__ == "__main__":
    msg = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse ut mauris elit. Maecenas eu odio non turpis ultricies fermentum. Ut lobortis odio vitae justo mattis dictum. Proin fringilla interdum semper. Curabitur posuere elit molestie neque ullamcorper placerat scelerisque nulla convallis. Proin sit amet bibendum nibh. Aliquam rhoncus vulputate est, id faucibus augue imperdiet sed.

    Maecenas in diam urna. Integer nisl odio, varius eu tempor nec, consequat a enim. Aliquam dapibus lacinia consectetur. Praesent molestie mi fermentum nisi luctus sollicitudin. Vivamus bibendum varius mollis. Quisque accumsan congue dapibus. Aliquam erat volutpat. Etiam ac arcu turpis. Integer sed mi eu velit rhoncus mattis. In dignissim, sapien id condimentum porttitor, nisl metus dapibus lectus, at eleifend dui orci quis purus. Nulla ut est non risus faucibus consectetur. Integer hendrerit augue et nunc egestas sit amet convallis diam feugiat.

    Maecenas ac nunc vel tortor ultricies eleifend. In scelerisque vehicula elit, eget aliquam tellus facilisis id. Ut ultrices feugiat risus, ut gravida libero commodo ac. Sed tincidunt dapibus dolor, sagittis volutpat quam tristique non. Aliquam sodales fringilla augue, sit amet venenatis orci bibendum ac. Curabitur quis magna ut elit volutpat venenatis. Quisque at sem sit amet erat interdum viverra eu ac diam. Curabitur in luctus felis. Morbi at nibh dolor. Ut enim sapien, viverra eu adipiscing sed, mollis id sapien. Pellentesque hendrerit elementum leo sed volutpat. Etiam scelerisque nulla vitae purus facilisis sed adipiscing ante viverra. Curabitur posuere felis non orci luctus id auctor massa malesuada.
'''

    # send mail
    recipients = ['me@somedomain.tld', ['Another me', 'me@otherdomain.tld']]
    sendmail(msg, 'Spam, delete me!!', recipients=recipients)
