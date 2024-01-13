from flask import Flask, render_template
import boto3

# create and configure the app
app = Flask(__name__)   #creates the Flask instance - __name__ is the name of the current Python module




def get_dynamodb_data():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1') #get dynamodb resource
    table = dynamodb.Table('Sensor_Data') #get data from dynamodb table
    #scan table
    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data



def get_chart_data(labels,values):
    data = get_dynamodb_data()
    data.sort(key=lambda s: s['date'])
    bar_labels = []
    bar_values = []
    for i in data:
      bar_labels.append(i[labels])
      bar_values.append(i[values])
    return bar_labels,bar_values


@app.route('/bar')
def bar():
    bar_labels,bar_values = get_chart_data('date','level')
    return render_template('bar.html', title='Water Level Monitoring: Level Chart', max=4, labels=bar_labels, values=bar_values)


@app.route('/line')
def line():
    bar_labels,bar_values = get_chart_data('date','percentage')
    return render_template('line.html', title='Water Level Monitoring: Percentage Chart', max=100, labels=bar_labels, values=bar_values)



@app.route("/") #creates a connection between the URL "/" and a function that returns a response
def main():
    data  = get_dynamodb_data()
    data.sort(key=lambda s: s['date'], reverse=True)
    return render_template('index.html',title='Water Level Monitoring: Data',data=data) #return a page "index.html" with data




if __name__ == "__main__":      
        app.run(host="0.0.0.0", port=80) #run app
