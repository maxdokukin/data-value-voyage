from dash import html
from components.topbar import get_topbar

layout = html.Div(className="section-slide", children=[
    get_topbar(show_home=True, overlay=True),

    html.Div(className="hero", children=[
        html.Div(className="overlay", children=[

            html.Div(className="overlay-content", children=[

                html.Div(className='profiles', children=[

                    # Max Dokukin's Profile
                    html.Div(className='profile', children=[
                        html.Img(src='/static/assets/max.jpg', alt='Max  Dokukin', className='profile__image'),
                        html.H3('Max  Dokukin', className='profile__name'),
                        html.P('Data Scientist', className='profile__description'),
                        html.Div(className='profile__links', children=[
                            html.A(html.Img(src='/static/assets/linkedin.png', alt='LinkedIn', className='icon'),
                                   href='https://www.linkedin.com/in/maxdokukin/', target='_blank'),
                            html.A(html.Img(src='/static/assets/github.png', alt='GitHub', className='icon'),
                                   href='https://github.com/maxdokukin', target='_blank'),
                        ]),
                        html.Ul(className='profile__contributions', children=[
                            html.Li('Motivation, Story, and Project Direction'),
                            html.Li('Web App Architecture Design and Development'),
                            html.Li('Affordable Quantity Analysis'),
                            html.Li('Database Design and Maintenance'),
                        ]),
                    ]),

                    # Ryan Fernald's Profile
                    html.Div(className='profile', children=[
                        html.Img(src='/static/assets/ryan.jpg', alt='Ryan Fernald', className='profile__image'),
                        html.H3('Ryan Fernald', className='profile__name'),
                        html.P('Data Scientist', className='profile__description'),
                        html.Div(className='profile__links', children=[
                            html.A(html.Img(src='/static/assets/linkedin.png', alt='LinkedIn', className='icon'),
                                   href='https://www.linkedin.com/in/ryan-fernald', target='_blank'),
                            html.A(html.Img(src='/static/assets/github.png', alt='GitHub', className='icon'),
                                   href='https://github.com/ryanfernald', target='_blank'),
                        ]),
                        html.Ul(className='profile__contributions', children=[
                            html.Li('Data Collection and Cleaning'),
                            html.Li('Gini Statistical Methods and Housing Analysis'),
                            html.Li('Web Page Design and Development'),
                            html.Li('Cloud Deployment and Maintenance'),
                        ]),
                    ]),
                ]),
            ])
        ])
    ])
])
