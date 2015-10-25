from cStringIO import StringIO
from flask import Flask, render_template, request, url_for, redirect, \
    make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

from instagram_analyze import instagram_analyzer
from instagram_graphs import instagram_graph
from forms import InstagramAnalyzer


app = Flask(__name__)
app.config.update(
    WTF_CSRF_ENABLED=True,
    SECRET_KEY='my precious'
)


# routes

@app.route('/', methods=['GET', 'POST'])
def main():
    form = InstagramAnalyzer(request.form)
    if form.validate_on_submit():
        text = form.instagram_analyze.data
        return redirect(url_for('instagram_analyze', user_input=text))
    return render_template('index.html', form=form)


@app.route("/instagram_analyze/<user_input>")
def instagram_analyze(user_input):
    return render_template(
        'analysis.html',
        input=user_input,
        filename=user_input+".png"  # create image title based on user input
    )


@app.route("/instagram_analyze/<image_name>.png")
def image(image_name):

    # create the DataFrame
    instagram_analyzed = instagram_analyzer(image_name)

    # format the DataFrame to display plots
    instagram_graph(instagram_analyzed)

    # render matplotlib image to Flask view
    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)

    # create response
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'

    return response
