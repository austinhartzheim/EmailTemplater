#! /usr/bin/python
__author__ = 'riccardo mutschlechner'

import smtplib, getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

class Sponsor:
    def __init__(self, name, contactName, email, tier):
        self.name = name
        self.contactName = contactName
        self.email = email
        self.tier = tier

    def printSponsor(self):
        print self.name, " ", self.contactName, " ", self.email, " ", self.tier


def sendEmail(sponsor, content):
    print "Sending email to: ", sponsor.name
    # me == my email address
    # you == recipient's email address
    me = "team@madhacks.org"
    you = sponsor.email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "University of Wisconsin - MadHacks Offer of Sponsorship"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message
    text = content

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)

    user = "team@madhacks.org"
    print "Type in the team password please:"
    passwd = getpass.getpass()

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login(user,passwd)

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()

def buildEmail(sponsor):
    print "Building email for Sponsor: ", sponsor.name, " ", sponsor.email
    fileName = (sponsor.name + ".txt").replace(" ", "_")
    fileName = fileName.replace("/", "") #strip bad stuff for files
    fileName = "./emails/" + fileName

    template = ""

    with open("template.txt") as t:
        template = ''.join(t.readlines())

    #add sponsor contact name with first name of recruiter
    template = template.replace("[RECRUITER NAME]", sponsor.contactName.split(" ")[0])

    #add company name
    template = template.replace("[COMPANY NAME]", sponsor.name)

    with open(fileName, "w") as f:
        f.write(template)

    #print template

    return template


def main():
    Sponsors = []
    with open('data/sponsors_test.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            #print ', '.join(row)
            if len(row) < 3: #please replace this with a better check for a null/bad row
                continue

            # when we add a tier field, if we do, please change [[TIER]] to the appropriate field
            name = row[0]
            if len(name) < 3:
                name = None

            contactName = row[1]
            if len(contactName) < 3:
                contactName = None

            email = row[3]
            if len(email) < 3:
                email = None

            tier = ""
            if len(tier) < 3:
                tier = None

            Sponsors.append(Sponsor(name, contactName, email, tier))

        for sponsor in Sponsors:
            #sponsor.printSponsor()

            #if we have all of the correct fields... build the emails!
            if sponsor.name is not None and sponsor.contactName is not None and sponsor.email is not None:
                template = buildEmail(sponsor)
                sendEmail(sponsor, template)
            else:
                print "Cannot build email for sponsor because missing fields"


if __name__ == "__main__":
    main()