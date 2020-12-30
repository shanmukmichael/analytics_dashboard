from flask import Flask, render_template, make_response, request, url_for, redirect
import io
import pandas as pd
import plotly
import json
import plotly.graph_objs as go

app = Flask(__name__)


global df
@app.route('/', methods=['GET','POST'])
def index():

    return render_template('index.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    try:
        f = request.files['file']

        if not f:
            return "No file"
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        data = pd.read_csv(stream)
        print(data)
        global df
        df = data
        stream.seek(0)
        result = stream.read().replace("=", ",")
        response = make_response(result)
        response.headers["Content-Disposition"] = "attachment; filename=result.csv"
        cols = data.columns.values
        col_list = []
        for i in cols:
            col_list.append(i)
        graph_list = ['Bar', 'Scatter','Scatter3d']
        return render_template('dashboard.html', col_list=col_list, graph_list=graph_list,
                               data=data.to_html(header=True, index=False), response=response)
    except:
        return redirect(url_for('index'))



@app.route('/graph', methods=['POST'])
def graph():

        x = request.form.get('x-axiss')
        y = request.form.get('y-axiss')
        graph_name = request.form.get('graph')
        print(x, y, graph_name)
        if graph_name == 'Bar':
            bar = create_plot_bar(x, y)
            return render_template('graph.html', plot=bar)
        elif graph_name == 'Scatter':
            Scatter = create_plot_Scatter(x, y)
            return render_template('graph.html', plot=Scatter )
        elif graph_name == 'Scatter':
            Scatter3d = create_plot_Scatter3d(x, y)
            return render_template('graph.html', plot=Scatter3d )




def create_plot_bar(x,y):
    data = [go.Bar(x=df[x],y=df[y])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_plot_Scatter(x,y):
    data = [go.Scatter(x=df[x],y=df[y])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_plot_Scatter3d(x,y):
    data = [go.scatter3d(x=df[x],y=df[y])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == "__main__":
    app.run(debug=True)