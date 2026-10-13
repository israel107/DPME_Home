import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

def bar_vertical(m_x, m_y, grd_titre, y_titre, m_corner, m_color='rgb(194, 72, 48)'):
    fig = go.Figure()

    fig.add_trace(go.Bar(
            x=m_x,
            y= m_y,
            text =  m_y,
            name='Vol_sect', textposition="outside", marker_color= m_color, marker=dict(cornerradius=m_corner)) )

    #fig.layout.template = CHART_THEME
    fig.update_layout(
        separators=",.",
        title= {
            'text':grd_titre,
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=y_titre,
            
            ))
    
    return fig

def chart_Waterfall(m_x, m_values, m_titre, m_measure):

    fig = go.Figure(go.Waterfall(
    name="Cash-flow",
    orientation="v",
    measure= m_measure,
    x=m_x,
    y=m_values,
    textposition="outside",
    texttemplate="%{y}",
    ))

    fig.update_layout(
        separators=",.",
        title= m_titre ,
        waterfallgap=0.3
    )

    return fig

def chart_pie(m_label, m_values, m_color, m_hole, m_size_font, m_titre):
    
    fig = go.Figure(data=[go.Pie(labels= m_label, values=m_values, marker_colors=m_color,  hole=m_hole)])

    fig.update_traces(
        textinfo="label+value+percent",
        textposition="inside",
        textfont=dict(size=m_size_font)   # Taille du texte sur les barres
            )

    fig.update_layout(
    separators=",.",
    title= {
        'text':m_titre,
        'y':0.9,
        'x':0.4,
        'xanchor': "center",
        'yanchor': 'top'
    },)

    return fig

def bar_horizontal(m_x, m_y, grd_titre,x_titre, y_titre, m_corner, m_color='rgb(194, 72, 48)'):
    fig = go.Figure()
   
    fig.add_trace(go.Bar(
        x= m_x,
        y= m_y,
        text =  m_x,
        name='Vol_sect',textposition="outside", orientation='h', marker_color=m_color, marker=dict(cornerradius=m_corner)) )

    #fig.layout.template = CHART_THEME
    fig.update_layout(
    title= {
        'text':grd_titre,
        'y':0.9,
        'x':0.5,
        'xanchor': "center",
        'yanchor': 'top'
    },
    xaxis=dict(
        title=x_titre,
        ),
    yaxis=dict(
        title=y_titre,
        
        ))
    
    return fig

def scatterMultiSelect(m_X, m_list,df,  grd_titre, y_title):

    fig = go.Figure()

    for pays in m_list:
        fig.add_trace(go.Scatter(
            x= m_X, y=df[pays],
            mode="lines",
            name=pays
        ))


    fig.update_layout(
        title= {
            'text':grd_titre,
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=y_title,
            
            ))

    return fig

def credit_par_mois(m_X, m_Y, grd_titre ,y_title,  m_col1='rgb(133, 32, 12)'):
    fig = go.Figure()
    
    fig.add_trace( go.Scatter( x= m_X, y=m_Y, mode='lines+markers+text', text=m_Y, textposition='bottom left' , marker_color=m_col1))

    fig.update_layout(
            title= {
                'text':grd_titre,
                'y':0.9,
                'x':0.5,
                'xanchor': "center",
                'yanchor': 'top'
            },
            xaxis_tickfont_size=12,
            yaxis=dict(
                title=y_title,
                
                ))
    
    return fig

def scatterRatios(m_X, m_y1, m_y2,  grd_titre, y_title, leg_1, leg_2, m_col1='rgb(133, 32, 12)', m_col2='rgb(194, 72, 48)'):

    fig = go.Figure()

    fig.add_trace( go.Scatter( x= m_X, y=m_y1, mode='lines', marker_color=m_col1, name=leg_1))

    fig.add_trace(go.Scatter( x=m_X, y=m_y2, mode='lines', marker_color=m_col2,name=leg_2))

    fig.update_layout(
        title= {
            'text':grd_titre,
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=y_title,
            
            ))

    return fig

def scatter_3_Ratios(m_X, m_y1, m_y2, m_y3,  grd_titre, y_title, leg_1, leg_2, leg_3, m_col1='rgb(133, 32, 12)', m_col2='rgb(194, 72, 48)', m_col3='rgb(194, 72, 48)'):

    fig = go.Figure()

    fig.add_trace( go.Scatter( x= m_X, y=m_y1, mode='lines', marker_color=m_col1, name=leg_1))

    fig.add_trace(go.Scatter( x=m_X, y=m_y2, mode='lines', marker_color=m_col2,name=leg_2))

    fig.add_trace(go.Scatter( x=m_X, y=m_y3, mode='lines', marker_color=m_col3,name=leg_3))

    fig.update_layout(
        title= {
            'text':grd_titre,
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=y_title,
            
            ))

    return fig


def scatterChart(m_x1,m_x2,m_x3, m_y1,m_y2,m_y3, grd_titre, y_title, m_col1='rgb(133, 32, 12)',m_col2='rgb(194, 72, 48)',
                  m_col3='rgb(228, 185, 176)'):
    fig = go.Figure()

    fig.add_trace( go.Scatter( x= m_x1, y=m_y1, mode='lines', marker_color=m_col1, name='Long terme')
    )

    fig.add_trace(go.Scatter( x=m_x2, y=m_y2, mode='lines', marker_color=m_col2,name='Moyen terme')
    )

    fig.add_trace(go.Scatter( x=m_x3, y=m_y3, mode='lines', marker_color=m_col3, name='Court terme')
    )

    fig.update_layout(
        title= {
            'text':grd_titre,
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=y_title,
            
            ))

    return fig

def doubleBar(mx, my_1, my_2, m_titre, y_titre, legend_1, legend_2,m_color1,m_color2 ):

    fig = go.Figure(data=[
    go.Bar(name=legend_1, x=mx, y=my_1, text = my_1, textposition="outside",
           marker_color= m_color1),
    go.Bar(name=legend_2, x= mx, y=my_2, text = my_2, textposition="outside",
           marker_color= m_color2)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group',
                      title= {
            'text':m_titre ,
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        yaxis=dict(
            title=y_titre,
            ),
        )
    
    return fig

def m_SunBurts(m_labels, m_parents, m_values, m_titre):

    brown_gradient = [
    "#f5e6d3",  # marron très clair
    "#e0c097",
    "#c89b6a",
    "#a47148",
    "#7a4a2e",
    "#4e2f1c"   # marron foncé
    ]

    fig = go.Figure(
        go.Sunburst(
            labels=m_labels,
            parents=m_parents,
            values= m_values,
            branchvalues="total",
            textinfo="label+value+percent parent",
            hoverinfo="label+value+percent parent",
            marker = dict(colors= brown_gradient),
        )
    )

    fig.update_layout(barmode='group',
                      title= {
            'text':m_titre ,
            'y':1.0,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        margin = dict(t=15, l=0, r=0, b=0),
        width=400,
        height=400,
        )

    return fig

def m_polarChart(cred_net, cre_souffrance,caisse, cre_douteuse, cred_ct, cpropres, cap_dotation,DAT, CCT, excedent, m_bank):
    #Actif

    df = pd.DataFrame(
        [
            ["Crédits nets", cred_net, "Actif"],
            ["Créances nets en souffrance", cre_souffrance, "Actif"],
            ["Caisse", caisse, "Actif"],
            ["Creances douteuses ou litigieuses", cre_douteuse, "Actif"],
            ["Crédits à court terme", cred_ct, "Actif"],

            ["Capitaux propres et ressources assimilés", cpropres, "Passif"],
            ["Capital-Dotation-Réserves", cap_dotation, "Passif"],

            ["Dépots et emprunts à terme", DAT, "Comptes de résultats"],
            ["Depots clientelle à terme", CCT, "Comptes de résultats"],
            ["Excedent ou deficit", excedent, "Comptes de résultats"],
        ],
        columns=["Libellés", "Valeur", "group"],
    )

    fig = px.bar_polar(
        df,
        r="Valeur",
        theta="Libellés",
        color=["Crédits nets", "Créances nets en souffrance", "Caisse","Creances douteuses ou litigieuses", "Crédits à court terme",
               "Capitaux propres et ressources assimilés", "Capital-Dotation-Réserves",
               "Dépots et emprunts à terme", "Depots clientelle à terme","Excedent ou deficit"],

        color_discrete_map={
        "Crédits nets": "#8B4513",
        "Créances nets en souffrance": "rgb(188, 92, 48)",
        "Caisse": "rgb(228, 185, 176)",
        "Creances douteuses ou litigieuses": "rgb(133, 32, 12)",
        "Crédits à court terme": "rgb(194, 72, 48)",

        "Capitaux propres et ressources assimilés": "#D2B48C",
        "Capital-Dotation-Réserves": "rgb(225, 185, 176)",
        
        "Dépots et emprunts à terme": "rgb(228, 165, 176)",
        "Depots clientelle à terme": "#7a4a2e",
        "Excedent ou deficit": "#4e2f1c"
    },
         
    )
    fig.update_layout(
        polar_hole=0.25,
        height=350,
        width=350,
        #text':m_titre 
        margin=dict(b=25, t=30, l=0, r=0),#b=30, t=30, l=0
        title={
        "text": "Données annuelles de "+m_bank+ " (Mds FCFA)",
        'y':1.0,
        "x": 0.5,
        "xanchor": "center"
        },
        showlegend=False,
    )
     

    return fig