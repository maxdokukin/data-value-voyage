from dash import dcc, html
from components.topbar import get_topbar

layout = html.Div(children=[
    get_topbar(current_path="/about-us", overlay=False),  # Top bar remains outside the container

    html.Div(className='container-about-us', children=[
        html.Link(rel='stylesheet', href='/static/css/about-us-styles.css'),
        # html.H2('About Us', className='section__title'),

        html.Div(className='profiles', children=[

            # Max Dokukin's Profile
            html.Div(className='profile', children=[
                html.Img(src='/static/assets/max.jpg', alt='Max  Dokukin', className='profile__image'),
                html.H3('Max  Dokukin', className='profile__name'),
                html.P('Data Scientist', className='profile__description'),
                html.Div(className='profile__links', children=[
                    html.A(html.Img(src='/static/assets/linkedin.png', alt='LinkedIn', className='icon'), href='https://www.linkedin.com/in/maxdokukin/', target='_blank'),
                    html.A(html.Img(src='/static/assets/github.png', alt='GitHub', className='icon'), href='https://github.com/maxdokukin', target='_blank'),
                ]),
                html.Ul(className='profile__contributions', children=[
                    html.Li('Motivation, Story, and Project Direction'),
                    html.Li('Affordable Quantity Analysis'),
                    html.Li('Web Application Design and Development'),
                    html.Li('Database Design Engineer'),
                ]),
            ]),

            # Ryan Fernald's Profile
            html.Div(className='profile', children=[
                html.Img(src='/static/assets/ryan.jpg', alt='Ryan Fernald', className='profile__image'),
                html.H3('Ryan Fernald', className='profile__name'),
                html.P('Data Scientist', className='profile__description'),
                html.Div(className='profile__links', children=[
                    html.A(html.Img(src='/static/assets/linkedin.png', alt='LinkedIn', className='icon'), href='https://www.linkedin.com/in/ryan-fernald', target='_blank'),
                    html.A(html.Img(src='/static/assets/github.png', alt='GitHub', className='icon'), href='https://github.com/ryanfernald', target='_blank'),
                ]),
                html.Ul(className='profile__contributions', children=[
                    html.Li('Data Collection and Cleaning'),
                    html.Li('Gini Statistical Methods and Housing Analysis'),
                    html.Li('Web Page Design and Development'),
                    html.Li('Cloud Deployment and Maintenance'),
                ]),
            ]),
        ]),

        # Link to the GitHub repository
        html.Div(className='repository-link', children=[
            html.A('View Our GitHub Repository', href='https://github.com/ryanfernald/Value-Voyage', target='_blank', className='repository-link__text mt-4'),
        ]),
    ]),
])
