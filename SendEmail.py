
__author__ = 'avthakar'

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import json
import pymongo
from bson import SON
import time

colorArray = ["#3366CC","#DC3912","#FF9900","#109618","#990099","#e4a14b","#e98125","#cb2121","#830909","#923e99"]


client = pymongo.MongoClient('localhost', 27017)
db = client.paragon.projects
db1 = client.paragon.schedule

def sendEmail(text, file, emailid):
    sender = 'ikyalnoo@cisco.com'
    receivers = ['ikyalnoo@cisco.com']
    msg = MIMEMultipart()
    msg['Subject'] = 'ISSU Daily Report'
    msg['From'] = 'ikyalnoo@cisco.com'
    msg['To'] = 'ikyalnoo@cisco.com'
    fp = open(file, 'rb')
    textbody = MIMEText("Irfan", 'plain')
    msg.attach(MIMEApplication(
                fp.read(),
                Content_Disposition='attachment; filename="%s"' % fp.
                    name,
                Name=fp.name))
    msg.attach(textbody)
    try:
        smtpn7k = smtplib.SMTP('outbound.cisco.com')
        smtpn7k.sendmail(sender, receivers, msg.as_string())
        print ("Successfully sent email")
    except :
        print ("Error: unable to send email")
    finally:
        smtpn7k.close()

def sendEmailReport(text,  emailid='avthakar@cisco.com'):
    sender = 'avthakar@cisco.com'
    receivers = ['avthakar@cisco.com','ipandher@cisco.com']
    msg = MIMEMultipart()
    msg['Subject'] = 'Paragon Status Report'
    msg['From'] = 'avthakar@cisco.com'
    msg['To'] = 'avthakar@cisco.com, ipandher@cisco.com'
    text = "Hi Inderpal!\nPlease find attached project status report for paragon.\n\n\nThanks\nTeam Paragon"
    html = create_html_page()



    part1 = MIMEText(text, 'plain')

    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)
    try:
        smtpn7k = smtplib.SMTP('outbound.cisco.com')
        smtpn7k.sendmail(sender, receivers, msg.as_string())
        print ("Successfully sent email")
    except :
        print ("Error: unable to send email")
    finally:
        smtpn7k.close()




def create_html_page():
    html = """
    <html>
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" rel="stylesheet">
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://code.jquery.com/ui/1.12.0/jquery-ui.js"></script>
<link href="/static/css/style.css" rel="stylesheet">
<link href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css" rel="stylesheet">

<script type="text/javascript"
        src="http://cdn.datatables.net/1.10.2/js/jquery.dataTables.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.6.0/d3.min.js"></script>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="https://rawgit.com/benkeen/d3pie/master/d3pie/d3pie.min.js"></script>

<body>

<nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container">
        <div class="navbar-header">




        </div>
        <p class="navbar-text hidden-xs" style="color:white"><I>Paragon Status Report </I></p>        <!-- Collect the nav links, forms, and other content for toggling -->

    </div>
    <!--/.nav-collapse -->

</nav>

<br>
	<div id="page-wrapper">
<br><br>

		<div class="container" style="border:1px solid">
		        <div class="row">
            <div class="col-sm-4"></div>
                         <div class="col-sm-4">
                <div class="panel-heading1">
                </div>
                <div class="pie-pannel text-center">


                        <svg width="500" height="270" id="pieChartSrc"></svg>

</div>
                             </div>
            </div>

	<div class="row">





    """
    body =''
    records = db.find().sort('_id', pymongo.DESCENDING)

    count = 0
    project = {}
    for record in records:
        html = html +'<div class="col-sm-12"><hr class="featurette-divider"><h2>'+record['name'] +'</h2><hr class="featurette-divider">'
        html = html +   """

    <table table id="reporttable{count}" class="table table-striped  table-bordered" >
		 <thead>
             	<th> FEATURE </th>
             	<th> DT </th>
             	<th> DE </th>
             	<th> FROM </th>
             	<th> END </th>
             	<th> TIMS </th>
             	<th> COMPLETION </th>

        </thead>
		             <tbody id="reporttablebody">

    """.format(count=count)

        count +=1
        tablebody = ''
        results = db1.find({'project': record['_id']}).sort('end_date', pymongo.ASCENDING)

        for result in results:
            result['start'] = str(time.strftime("%m/%d/%Y", time.localtime(result['start'])))
            result['end'] = str(time.strftime("%m/%d/%Y", time.localtime(result['end'])))

            tablebody = """

    <tr>
             	<td> {feature} </td>
             	<td> {dt} </td>
             	<td> {de} </td>
             	<td> {start} </td>
             	<td> {end} </td>
             	<td> <a href="{tims}" target="_blank">Click Here</a> </td>
             	<td> {completion} </td>
            </tr>
    """.format(feature=result['feature'], dt= result['dt'], de= result['de'], start =result['start'], end=result['end'], tims=result['tims'], completion=result['completion'] )

            html = html + tablebody

        html = html + """
         </tbody>
        </table>
        </div>
        """

    html = html + '<script>'
    scriptbody = ''
    for counter in range(count):
        str1 = 'dataTable({"order": [[ 1, "desc" ]]})'

        script =  """
            $( "#reporttable{counter}" ).
            """.format(counter=counter)
        str1 =  script + str1
        scriptbody = scriptbody + str1


    html = html + scriptbody + """
    </script>
</div>
			</div>
		</div>
		 <script>



    """
    counter = 0
    projjson = {}
    result1 = db1.aggregate([{"$group":{"_id":"$project","sum":{"$sum":1}}}, {"$sort": SON([("sum", -1)])}, { "$limit": 10 }])

    projectarray = []
    for records in result1:
        id = db.find_one({'_id': records['_id']})
        projjson = dict({"label": id['name'], "value": records["sum"], 'color': colorArray[counter]})
        projectarray.append(projjson)
        counter += 1
    jsonobj1 = dict({"content": projectarray})



    finalsection = """
    data1 = '{"size": {"canvasHeight":280,"canvasWidth":300,"pieOuterRadius": "75%"	},"tooltips": {"enabled": true,"type": "placeholder","string": "{label}: {value}, {percentage}%"}, "data":"""+json.dumps(jsonobj1)+""","labels": {"outer": {"pieDistance": 15	}   ,"inner": {"format": "value"},"misc": {"canvasPadding": {"top": 0,			"right": 0,			"bottom": 0,			"left": 0   		}	}}}';
        data2 = JSON.parse(data1);
        var pie = new d3pie("pieChartSrc", data2);
    </script>
 </body>
 </html>
"""
    html = html + finalsection
    return html

if __name__ == '__main__':
    sendEmailReport(    '')