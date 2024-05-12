from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError
import smtplib

from aw.record import Record
from aw.timestamper import TimeStamper

class Mailer:
    """Class containing everything to compose and send results via email.
    
    Attributes:
    -----------
    sender : str
        email address which you want to send result from
    receiver : str
        email address which receives results
    password : str
        password to login to sender mail
    smtp : str
        server address of where sender mail is hosted
    port : str
        port number of the smtp server
    timestamper : TimeStamper
        TimeStamper object which gives current timestamps
    msg : MIMUEMultipart | None
        MIMEMUltipart object, contains message to send via smtp
    msgBody : str
        string containing HTML code of the message body

    Public methods:
    ---------------
    sendMail(records)
    resetMailerConfig()
    emptyMessage()

    
    """
    def __init__(self, sender: str, receiver: str, password: str, smtp: str, port: str | int, timestamper: TimeStamper) -> None:
        """Constructor.

        Parameters:
        -----------
        sender : str
            email address which you want to send result from
        receiver : str
            email address which receives results
        password : str
            password to login to sender mail
        smtp : str
            server address of where sender mail is hosted
        port : str
            port number of the smtp server


        """
        self.sender = sender
        self.receiver = receiver
        self.password = password
        self.smtp = smtp
        if type(port) == str:
            try:
                self.port = int(port)
            except ValueError:
                self.port = None
        else:
            self.port = port
                    
            

        self.timestamper = timestamper

        self.msg = None
        self.msgBody = None

    def sendMail(self, records: list[Record]) -> None:
        """Send composed HTML email with results.
        
        Parameters:
        -----------
        records : list[Record]
            list of Record objects
        """

        if not self.sender:
            raise Exception("Sender address is not set.")
        
        if not self.receiver:
            raise Exception("Receiver address is not set.")
        
        if not self.password:
            raise Exception("Password is not set.")
        
        if not self.smtp:
            raise Exception("SMTP server address is not set.")
    
        if not self.port:
            raise Exception("SMTP server port is not set.")

        self._composeMail(records)

        with smtplib.SMTP_SSL(self.smtp, self.port) as server:
            try:
                server.login(self.sender, self.password)
            except SMTPAuthenticationError:
                raise Exception("Login email / password combination is wrong.")
            
            if not self.msg or not self.msgBody:
                raise Exception("Message or MessageBody is empty.")
            else:
                server.send_message(self.msg)

    def _composeMail(self, records: list[Record]) -> None:
        self.msg = MIMEMultipart()
        self.msg["From"] = self.sender
        self.msg["To"] = self.receiver
        self.msg["Subject"] = f"Record from {self.timestamper.getDateStamp}."

        self.msgBody = self._composeMsgBody(self, records)

        self.msg.attach(MIMEText(self.msgBody, "html"))

    def _composeMsgBody(self, records: list[Record]) -> str:
        header = "<h1>Results:</h1>"
        table = self._composeHtmlTable(records)
        html = f"<html><body>{header}{table}</body></html>"

        return html
    
    def _composeHtmlTable(self, records: list[Record]) -> str:
        tableHeader = "<th>Book</th><th>Author</th><th>Price</th><th>Year</th><th>Publisher</th><th>Link</th>"
        htmlTable = f"<table border='1'><tr>{tableHeader}</tr>"
        for rec in records:
            htmlTable += f"<tr><td>{rec.book}</td><td>{rec.author}</td><td>{rec.price}</td><td>{rec.year}</td><td>{rec.publisher}</td><td><a href=\"{rec.link}\">LINK</a></td></tr>"
        htmlTable += "</table>"

        return htmlTable
    
    def resetMailer(self, sender: str | None = None, receiver: str | None = None, password: str | None = None, smtp: str | None = None, port: str | int | None = None) -> None:
        """Reset attributes related to smtp server and mail sending.

        Keyword parameters:
        -------------------
        sender: str | None
            sender mail address
        receiver: str | None
            receiver mail address
        password: str | None
            sender mail password
        smtp: str | None
            smtp server where sender is hosted
        port: str | int | None
            port of the smtp server
        """

        if sender:
            self.sender = sender
        if receiver:
            self.receiver = receiver
        if password:
            self.password = password
        if smtp:
            self.smtp = smtp
        if port:
            if type(port) == str:
                try:
                    self.port = int(port)
                except ValueError:
                    self.port = None
            else:
                self.port = port

    def emptyMessage(self) -> None:
        """Reset content of self.msg and self.msgBody."""
        self.msg = None
        self.msgBody = None