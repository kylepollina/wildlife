# Fermilab link
# https://www.fnal.gov/cgi-bin/ecology/wildlife/bigbar?Greater+White-fronted+Goose

import pandas as pd
import math


html_start = """
<!-- template.html -->

<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">

    <!-- CSS -->

    <link rel="stylesheet" href="../../styles.css">
    <!-- Fonts -->

    <title></title>
  </head>
  <body>
    <div id="container">
        <div id="posts">
        <div id="birds">
    <h1>Dupage Birding Club Visual Checklist</h1>
"""

html_end = """
    </div>
    </div>
    </div>
  </body>
</html>
"""


def build_page(bird_data, output_file):
    html = html_start

    season, abundance = output_file.split('/')
    abundance = abundance.replace('.html', '')

    html += f'<u><h1>{season}</h1></u>'

    for s in ['winter', 'early-spring', 'late-spring', 'summer', 'post-breeding', 'early-fall', 'late-fall']:
        html += "<a href='https://kylepollina.github.io/wildlife/dbc-checklist/{}/abundant.html'>".format(s)
        html += "{}</a>".format(s.replace('-', ' '))
        if s != 'late-fall':
            html += " - "


    html += "<u><h3>{}</h3></u>".format(abundance.replace('-', ' '))

    for abd in ['abundant', 'common', 'fairly-common', 'uncommon', 'rare', 'extremely-rare']:
        html += "<a href='https://kylepollina.github.io/wildlife/dbc-checklist/{}/{}.html'>".format(season, abd)
        html += "{}</a>".format(abd.replace('-', ' '))
        if abd != 'extremely-rare':
            html += " - "

    for bird, row in bird_data.iterrows():
        html += f"<h1>{bird}</h1>"
        html += '<img src="{}" />'.format(row['img']) if isinstance(row['img'], str) else ''
        html += row['recording_embed_link']

        html += "<details><summary>More Information</summary>"
        html += "<ul>"
        html += "<li><a href='{}'> eBird - {}</a></li>".format(row['ebird'], bird)
        html += "<li><a href='{}'> Wikipedia - {}</a></li>".format(row['wikipedia'], bird)
        html += "<ul><u>All About Birds - {}</u>".format(bird)
        html += "<li><a href='{}'>Overview</a></li>".format(row['allaboutbirds'])
        html += "<li><a href='{}'>ID Info</a></li>".format(row['allaboutbirds'].replace('/overview', '/id'))
        html += "</ul>"
        html += "<h2>Range Map</h2>"
        html += '<a href="{}"><img src="{}" style="width: 75%"/></a>'.format(row['allaboutbirds'].replace('/overview', '/maps-range'), row['migration'])
        html += "</details>"

        html += "<hr>"

    html += html_end

    with open(output_file, 'w+') as f:
        f.write(html)


if __name__ == "__main__":
    df = pd.read_csv('bird_data.csv', index_col='bird')

    for season in ['winter', 'early spring', 'late spring', 'summer', 'post breeding', 'early fall', 'late fall']:
        winter_birds = df.dropna(subset=[season])
        build_page(winter_birds[winter_birds[season] == '1 - abundant'], '{}/abundant.html'.format(season.replace(' ', '-')))
        build_page(winter_birds[winter_birds[season] == '2 - common'], '{}/common.html'.format(season.replace(' ', '-')))
        build_page(winter_birds[winter_birds[season] == '3 - fairly common'], '{}/fairly-common.html'.format(season.replace(' ', '-')))
        build_page(winter_birds[winter_birds[season] == '4 - uncommon'], '{}/uncommon.html'.format(season.replace(' ', '-')))
        build_page(winter_birds[winter_birds[season] == '5 - rare'], '{}/rare.html'.format(season.replace(' ', '-')))
        build_page(winter_birds[winter_birds[season] == '6 - extremely rare'], '{}/extremely-rare.html'.format(season.replace(' ', '-')))
