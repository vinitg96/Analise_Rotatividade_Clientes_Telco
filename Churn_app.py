import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pickle

#options
st.set_page_config(page_title="Telco Company Churn", layout="wide", initial_sidebar_state="expanded",
menu_items=None)
config = {'displayModeBar': False, "showTips": False    }
st.title("Análise de Rotatividade dos Clientes da Telco Company")

#constantes
PATH = "./data/plots/"

@st.cache
def load_plot_df(file_name):
    df = pd.read_csv(PATH+file_name)
    return df

def load_model():
    model = pickle.load(open("./trained_models/dt.sav", "rb"))
    return model
@st.cache
def load_df():
    df = pd.read_csv("./data/final_df.csv")
    return df

model = load_model()
df = load_df()


html = """<p>
    <p>
    <p>
    <p>
      <a href="https://www.linkedin.com/in/vinicius-torres-05a35695/" rel="nofollow noreferrer">
        <img src= "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAABHtJREFUWEelV09olEcU/80mWEuhQmg9xOKhoSBW46EgPUaR4kUPbVOPPUqhhx68GdHtBgr14slDDx4CZl1LkZpDL202NQUPRWhNtnV3I4n5Z3ZNNFRSGt3syJuZN9/MfPNtAp3Lfvt9b9783u/93psZARoXZQ7d4wuA6FX/JQChnoJBL+lj5L2UwZzENj1LLqF1fD/yoi0weLML/W+1rMvMxcnCuOpoYzyxTZbt6gKw/Hq3QOGXJRs5o/AmZUUdY0i/c2f4s80/WnxtERCiKVAY9zglky+PvoOT7/Zg4tE6Lt+dT5wqSwEIdwrnyk9NJmxe3OB3AOgpcmggJQAxXPYjy6B1O67E6gIkRc6DYmEGaPKnB/fi5sfvp7j9/Me/MTK1krznYKNCNSyFoqTIny4qDTNQ+vVScO7D/bh8oi8F4Ovf5nCxPEs5y6gCf4q2cgS7pnMemy1EYZywKmS5HLB1/pjvTQK7vpnAy3as/LKFaL8EOU8XcCDCg2+/gcrZo9au/7vfMdXcSGorkv84LwJYnddqD0vDQeFpwNe2gEw1l52VnsqyWbxz0ihRAQM7a0gcksmdI2tBlRSl3VAXIEoBkEO+BmhabrhsBUTflSsnFflfZ3Fpcg5XPnoPJ/dsoF6vK0hs8u3deUzOr0fpSwAYawtA0a/rjPuAcsoAHHf5O7P44oN9eLY4axcPV6uu/YtzP8+4LcAA5BS4AAKhiULZbjTtoWNe9OTx+WYLy3MP9eLsR1J+Vaexg7rqHWbCpEKgUDbak2qyvGAodpVqOqFmwHRKB2S1Ws2M3GVCQuJ0aSqpKAUxEGGoAZ2CCduAwu+8+NP/XoI6Jo3unMCtwcNeFhjv6dJ9b0PfIQC9F7AG+NmN/FTpfrKgAHZ35fD9J4d8KUiJ/OQc7j1+bkH4AEwKXAXTM1WBfifQHhpQaaXFa/W6ev5pZg1X7y2lVD52pj91urn2x2Pcqj5xxFgYl25pxlRuU6AADqBaq6Fe06VGY3S6gWKlker1GoA/rk+v4Eal6WxIVgO8HTsi5N7hiPDBYK+NnJkqGgAmSXY77wSAbeMa4LowVWT7wOoCxk70pKLyGHDo3B5AsB2HIlMHFAitAdNeyakmJqlDBkDz7V4vgNufZaeAo9iRCMVXI3ZXi0U1OtVA8a+GIyz9eJs0wH1bCpDYitMrSi8MNbMMOT5S+4HhH6zzKACrAf+olLKVwGhFizCxjDYikrtAraZLza3xOIAmihXnyGbyENrSoqOmCuIpAEydC1XnvKtpAHpzGnPyyixdn27ghqLVHRJjZ45Ey7C0HQPVag31es1OPlX6s2NpKRGSBoJTmwIbHFy5D2Qy0LPRQKv5yEEu8M+LllI9VcSbu7rNc2KyuSWxudVOMUC2ajilGdoaERqLJ+boHLgyLcq/L3Q4a4WfOh3L6GpGd6R9XOcdbqapfP7/F6Ih1M14fWTLnl4jXlUE7m3CyXXG60xsHht9L7q0ROiG/NrMMiD3atHoMoyNxEHG/Ww7WnQ0DfRt9iKfb78CLOl4lgOx5t8AAAAASUVORK5CYII="> LinkedIn
      </a> &nbsp; 
      <a href="https://github.com/vinitg96/Projetos_Data_Science/tree/main/Analise_Rotatividade_Clientes_Telco" rel="nofollow noreferrer">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAABMpJREFUWEeVV02IHEUUfq97Z8yCIsp6iGgCih7iHhREAzNVs+shB8lBECXJKQchEZUkm+lkL7IQxOD07GYvrhoPIvgvKOrFHKI71bPgQQWJwYMREveirAEVnSTsTD2prv6p7q7uWesyM/WqXr33ve99VYNQNTAyUrqoOR/cRpt40HXkDADu0Ba8QlL23NHordXl2T/DGQAwtmVOSWyo140dzaNiO9TwGwdgBwIBUXZn8TC6XKvVd59/effvpnNzXfw9DUD5pGzUjZP9W1wpNwDwpnyUVRkaa687g+Edqyuz/9jhwBwCkVf1wbzVZQD3yDg4x8KnSoGwFHTYce0+G3qEQHay5YlLBHivPUtV2S1VziAQAhBdEl1+X95nzhMC93rrSHiXKnM6YjoZk0YcFg6UBfmr8NnO1K9RAvWVe70vAHCvXkARXPFyfWLVYVvhBQF+FvjNJ2KvSUoz7bVpifKCmbcEerrv848bJ/t3OpIuIMDtmqZmf+rvucpedaA+3fMf+a3R7h9wUL5rlm00xOm15eZF5SoJoOUFlO9b4bNMIdic2IUOHgAp3xBLrXUMS6tD5nO9u8nFww7SO71O66ckEQTgbWEeFZoCn6EiZHgAmxPPoosreUYnAZhNGwNg0qJMcSKHvB2E5M+gJOGQWGRnwwC4FxRcKE3odRoOOE5oi6sfknPMgZlEFsjhg/4omTMqqFDAmYWvt8nBxDVbv9cm6lPnTz961YSzTFAyURkUmTn+7ZR0rm3Y9MLZGE4i94IuABy3BPCq8NnzacKRjKi66yaxDJOckTnkQPA6ABzKbyBCH7knBgA4mTUSCJ9Xqk0Yzv8ohy5zQcQGCgFrLvkOsOVbfeeZnU7AvWInhKjHDLV2gJlhLlsTnnxj2IItJBptqkTAptv5y8SOTJFRZUiHCISCkvOkSpBQqrTWMTERqCBjWYca6TwHCBQJCyqVKtUWiR4mYMii5UWUQcC8yJgnrjjR0yqHwkvCZy+Oh7iCKNHmphecdoDm89c4AV7GphcccQCWbQdZO8E4z1qZZDJ9YmXrn6ZPRC+USrEKSBJs9rusXo5C1mILiLfFJiBO5H2otb2YZ7wdDAHBDRcR/QGINwPAtmSTlAeDxdbbW7oCoigannjGBXyzLHgCGAY+q2kE5noPoet8ryWWhOjyVnM+uMcZwS8ZB0QjdPHT3ivsqaJj9aARnwPRXkDdQFVCKUfwYH+J/5DoCW+L64D69UsEf/e77NaG4gfBcuIJARyC2dUuW7WLzdoeAHkutcXqm1N1ohuiy0OEE8uuhY/qU4PtN5LNo9GTYmnmE+aJJQQ4Fi8dR8wywTED/vevyfp3Zx/ezASgfrTawX5CeE9Dl15IljsuA4B5Y2pdqRq4T/jND+MVCOa7Kvw/IF5DwMMRIX8WXX5/ZTFzoWQCiEJJlBZhJeiw58wIjeKkebATa6eQZCJCRCABYB2RdhavafVWUnjpoUqgf2frTkCnAp8v2NoxnEv1Q0tq49hXD7gTtR9TqPR9UeBAjuo2DoyGm9NrZx67mPeV5UBJz7ROBO8Twb7wfyMCiC5TCZaOlicozh4RPuh12H5zcYqLiZPt8MwcAmuLo+jAHtFhj1dRjHvBOSnpy/4iP1NNRm39D5AhBpJuROh9AAAAAElFTkSuQmCC" alt="github"> Github
        <i class="fa-brands fa-medium"></i>
      </a>
    </p>"""

#barra lateral
st.sidebar.title("Seções")
sidebar = st.sidebar.radio("",options=("Dashboard","Insights Obtidos","Cadastro de Novo Cliente", "Interpretando as Previsões"))
#st.sidebar.write("O objetivo desse projeto foi avaliar dados reais de rotatividade em empresas de telecomunicação, buscar insigths através de visualizações e propor soluções que possam auxiliar os tomadores de decisão a por em prática medidas afim de reduzir a evasão de clientes.")
#st.sidebar.write("Também foram empregradas técncias de aprendizado de máquina para obter a probabilidade de um cliente vir a deixar a empresa (aprendizagem supervisionada) e segmentar clientes em grupos com base em seus comportamentos (aprendizagem não-supervisionada).")


#links para github e linkedin
with st.sidebar:
        st.markdown(html, unsafe_allow_html=True)

#Dashboard
if sidebar == "Dashboard":

    col1,col2,col3 = st.columns(3)

    col1.metric("Clientes na base de dados", "5.000")
    col2.metric("Ativos", "4.293 (85,9%)")
    col3.metric("Rotativos","707 (14,1%)")

### Plot dos mapas
    df_map = load_plot_df("df_map.csv")

    def mapplot(df_map, user_choice, sufix = ""):
        
        fig = px.choropleth(df_map,
        locations='Sigla',
        color= user_choice,
        color_continuous_scale='ice',
        hover_name='Estado',
        hover_data = {user_choice:True,"Sigla":False},
        basemap_visible = True,
        locationmode='USA-states',
        labels={'Evasão':'Evasão'},
        scope = "usa"
                )

        fig.update_layout(
        title='',
        margin=dict(l=0, r=0, t=30, b=0),
        height = 400
        )

        fig.update_coloraxes(
        showscale = True,
        autocolorscale = False,
        reversescale = True,
        cmin = df_map[user_choice].min(),
        cmax = df_map[user_choice].max(),
        cmid= df_map[user_choice].median(),
        colorbar = dict(orientation = "h", tickfont_size = 15, thickness = 15, lenmode = "fraction", len = 0.75,
                        ticksuffix = sufix, ypad = 5, xpad = 10, title_side = "top"),
        colorbar_title_text=""
                )
        
        return fig


    col1,col2 = st.columns(2)

    with col1:
        choice = st.selectbox("", ["Arrecadação", "Chamadas", "Clientes", "Rotatividade"],key = "left", index = 3)

        if (choice == "Arrecadação") or (choice == "Rotatividade"):
            st.subheader(f"{choice} média por estado")
        else:
            st.subheader(f"Média de {choice} por estado")
        
        if choice == "Rotatividade":
            map1 = mapplot(df_map, choice, sufix="%")
        else:
            map1 = mapplot(df_map, choice)

        st.plotly_chart(map1, use_container_width=True, config = config)

    with col2:
        choice2 = st.selectbox("", ["Arrecadação", "Chamadas", "Clientes", "Rotatividade"],key = "right", index = 2)

        if (choice2 == "Arrecadação") or (choice2 == "Rotatividade"):
            st.subheader(f"{choice2} média por estado")
        else:
            st.subheader(f"Média de {choice2} por estado")

        if choice2 == "Rotatividade":
            map2 = mapplot(df_map, choice2, sufix="%")
        else:
            map2 = mapplot(df_map, choice2)

        st.plotly_chart(map2, use_container_width=True, config = config)
    
    ############# barllot horario

    def barplot_day_hour(input, input_enc):

        df_plot_day_hour = df.groupby("churn").mean()[[f"total_day_{input_enc}",f"total_eve_{input_enc}", f"total_night_{input_enc}"]].reset_index()
        df_plot_day_hour = df_plot_day_hour.melt("churn")
        df_plot_day_hour["churn"] = df_plot_day_hour["churn"].map({0:"Ativo", 1:"Rotativo"})
        df_plot_day_hour["variable"] = df_plot_day_hour["variable"].map({f"total_day_{input_enc}":"Manhã", 
        f"total_eve_{input_enc}": "Tarde", f"total_night_{input_enc}": "Noite",})

        fig = px.bar(data_frame=df_plot_day_hour,
        x  =  "variable", 
        y="value", 
        color = "churn", 
        barmode = "group",
        labels={
            "value":f"{input}",
            "churn":"Status",
            "variable":"Período do Dia"
    },
        hover_data= {
            "variable":False,
            "value": ":.2f",
    })
        fig.update_layout(font=dict(size=17), hoverlabel = dict(font=dict(size=17)))
        return fig

    container = st.container()
    choice3 = st.selectbox("",["Cobranças", "Minutos em Chamadas", "Número de Chamadas"], index=0)
    with container:
        st.subheader(f"Consumo por Período do Dia: Média de {choice3}")
    
    #encode
    if choice3 == "Cobranças":
        choice3_enc = "charge"
    elif choice3 == "Minutos em Chamadas":
        choice3_enc = "minutes"
    else:
        choice3_enc = "calls"

    bar = barplot_day_hour(choice3, choice3_enc)
    st.plotly_chart(bar, config = config, use_container_width=True)

    ############## barplot comaracao
    def barplot_churn_comparative(input,input_enc):
        to_compare= ["recharge_total","number_customer_service_calls","calls_total","number_vmail_messages"]
        df_plot_churn_comparative = df.groupby("churn").mean()[to_compare].reset_index()
        df_plot_churn_comparative["churn"]=  df_plot_churn_comparative["churn"].map({0:"Ativo",1:"Rotativo"})
        fig = px.bar(data_frame=df_plot_churn_comparative,
                    x  =  "churn", 
                    y= input_enc,
                    color = "churn", 
                    #barmode = "group",
                    labels={
                        input_enc: input,
                        "churn":"Status",
                        },
                    hover_data= {
                        input_enc:":.2f"
        
                    },)
        fig.update_layout(font=dict(size=17), hoverlabel = dict(font=dict(size=17)))
        return fig

    container2 = st.container()
    options2 =["Total de Cobranças", "Ligações Para Serviço ao Consumidor", "Total de Ligações", "SMS Enviados"]
    choice4 = st.selectbox("",["Total de Cobranças", "Ligações Para Serviço ao Consumidor", "Total de Ligações", "SMS Enviados"],index=0)
    with container2:
        st.subheader(f"Comparação Entre Clientes Ativos vs Rotativos: Média de {choice4}")
    
    #encode
    if options2.index(choice4) == 0:
        choice4_enc = "recharge_total"
    elif options2.index(choice4) == 1:
        choice4_enc = "number_customer_service_calls"
    elif options2.index(choice4) == 2:
        choice4_enc = "calls_total"
    else:
        choice4_enc = "number_vmail_messages"

    bar_comp = barplot_churn_comparative(choice4, choice4_enc)
    st.plotly_chart(bar_comp, config = config, use_container_width=True)


    ##########333333333333333 pie pizza 
    st.subheader("Tipos de Planos Aquiridos por Clientes Ativos e Rotativos")

    df_pie =  df.groupby(["churn", "plan"]).count().iloc[:,1].reset_index()
    df_pie["churn"] = df_pie["churn"].map({0: "Ativo", 1: "Rotativo"})

    pie = px.pie(df_pie,
             values="account_length",
             names="plan",
             facet_col = "churn",
             labels={
                 "account_length": "Clientes",
                 "churn": "Status",
                 "plan": "Plano",
                 },
             hover_data  =  {
                 "churn":False,
             })

    pie.update_layout(font=dict(size=17), hoverlabel = dict(font=dict(size=17)))

    pie.update_traces( textfont_color="#000000")
    st.plotly_chart(pie, use_container_width=True, config = config)

    ###Clusters sonarmap

    sonar_df = load_plot_df("sonar_df.csv")

    go.Figure()

    sonar = go.Figure()

    sonar.add_trace(go.Scatterpolar(
    r=sonar_df["0"],
    theta=sonar_df.iloc[:,0],
    fill='toself',
    line = dict(color = "#33FFE3"),
    name='Grupo 1',
    hoverinfo = "none"
    ))
    sonar.add_trace(go.Scatterpolar(
    r=sonar_df["1"],
    theta=sonar_df.iloc[:,0],
    fill='toself',
    name='Grupo 2 ',
    hoverinfo = "none"
    ))

    sonar.add_trace(go.Scatterpolar(
    r=sonar_df["2"],
    theta=sonar_df.iloc[:,0],
    fill='toself',
    name='Grupo 3',
    hoverinfo = "none"
    ))

    sonar.add_trace(go.Scatterpolar(
    r=sonar_df["3"],
    theta=sonar_df.iloc[:,0],
    fill='toself',
    name='Grupo 4',
    hoverinfo = "none"
    ))

    sonar.update_layout(
    polar=dict(
    radialaxis=dict(
    visible=True,
    range=[0, 5]
    )),
    font=dict(size=17),
    showlegend=True, margin=dict(l=0, r=0, t=60, b=30), height = 450, legend_x=0.8
    )
    st.subheader("Segmentação dos Clientes em Grupos")
    st.write("Valores redimensionados em uma escala de pontuação de 0 a 5")
    st.plotly_chart(sonar, use_container_width=True, config = config)

### Novo cliente
if sidebar == "Cadastro de Novo Cliente":

    st.subheader("Preencha com os dados do cliente para obter a probabilidade de evasão")           

    df = pd.read_csv("./data/final_df.csv")
    boruta_cols = ['international_plan', 'total_intl_calls', 
    'total_eve_minutes', 'recharge_total', 'number_customer_service_calls', 'total_intl_minutes',
    'voice_mail_plan']

    to_selectbox = ["international_plan", "voice_mail_plan"]
    to_slider = sorted(list(set(boruta_cols) - set(to_selectbox)))

    to_selectbox_label = ["Plano Internacional", "Plano de Correio de Voz"]
    to_selectbox_help = ["Cliente possui ou não plano internacional", 
    "Cliente possui ou não plano de correio de voz"]

    to_slider_label = ["Ligações para Atendimento ao Cliente", "Cobrança Total", "Minutos em Chamadas à Tarde",
   "Ligações Internacionais", "Minutos em Chamadas Internacionais"]

    to_slider_help = [
       "Total de Chamadas Para o Serviço de Atendimento ao Cliente",
       "Cobrança Total Para o Cliente em $",
       "Total de Minutos em Chamadas Noturnas",
       "Número de Ligações Internacionais Realizadas",
       "Total de Minutos em Chamadas Internacionais"
   ]

    def make_selectbox(label, help):
        selectbox = st.selectbox(label, options = ["Não", "Sim"], index=1, help = help)
        return selectbox

    def make_slider(label, varname, help):
        min = int(df[varname].min())
        max = int(df[varname].max())
        med = int(df[varname].median())
        slider = st.slider(label,min,max,med, help = help)
        return slider

    dic = {}

    for catlabel, catvar, cathelp in zip( to_selectbox_label, to_selectbox, to_selectbox_help):
        selectbox = make_selectbox(catlabel, cathelp)
        dic[catvar] = selectbox

    for numlabel, numvar, numhelp in zip(to_slider_label, to_slider, to_slider_help):
        slider = make_slider(numlabel, numvar, numhelp)
        dic[numvar] = slider

    #organizar internamente na ordem das features que o modelo foi treinado
    order_dic = {}

    for col in boruta_cols: #ordem certa
        for key in dic.keys():
            if col == key:
                order_dic[col] = dic[key]

    #encode internoo para numerico
    if order_dic["international_plan"] == "Sim":
            order_dic["international_plan"] = 1
    else:
            order_dic["international_plan"] = 0

    if order_dic["voice_mail_plan"] == "Sim":
            order_dic["voice_mail_plan"] = 1
    else:
            order_dic["voice_mail_plan"] = 0


    new_input = np.array([i for i in order_dic.values()]).reshape((1,-1))


    if st.button("Obter previsões"):
        prob = model.predict_proba(new_input)[0][1]
        st.write(f"O cliente tem {prob*100:.2f}% de chance de deixar a empresa")




    

if sidebar == "Interpretando as Previsões":
    st.subheader("Estrutura da Árvore de Decisão Treinada")
    st.image("./media/tree.png")

    st.markdown(
        """
- Para obter uma previsão, basta seguir o fluxograma acima, seguindo para esquerda sempre que a resposta para a proposição for 'Verdadeiro' e para direita quando a resposta for 'Falso'.

- Por exemplo, um novo cliente com cobranças igual a 80 (recharge ≤ 74,04 = Falso, segue para direita), que tenha o plano correio de voz (voice_plan ≤ 0.5 = False, segue para direita) e que tenha também o plano internacional (voice_plan ≤ 0.5 = True, segue para direita) terá cerca de 46% de chance de deixar a  emprpesa, uma vez que dos 13 clientes nesse nó, 6 efetuaram o churn.

- Uma observação é que essa previsão foi baseada em poucas obbservações, por isso esse valor não é tão confiável. Em contrapartida, um outro cliente com cobranças igual a 80 (recharge ≤ 74,04 = Falso, segue para direita) e que não tenha o plano correio de voz (voice_plan ≤ 0.5 = True, segue para esquerda) tem 100% de chance de deixar a empresa, uma vez que todos os outros 299 clientes com essas características nos dados de treino foram rotativos. Essa previsão é bem mais confiável que a primeira justamente pelo maior número de observações no nó terminal
""" 
)

if sidebar == "Insights Obtidos":
    st.subheader("Principais Descobertas: ")
    st.markdown("""
- Os clientes que saem da empresa são em média 12% mais lucrativos do que os que permanecem, o que evidencia a importância de reduzir o churn.
- Clientes que fazem o churn realizam 54% mais chamadas de serviço ao consumidor e enviam cerca de 40% menos mensagens por voz do que clientes que permanecem.
- Clientes que fazem o churn são mais ativos no período da manhã do que clientes que permanecem.
- A adesão apenas do plano internacional parece estar relacionada com uma maior evasão, tendo em vista que mais de 20% dos clientes rotativos possuem somente esse plano enquanto a porcentagem dos que permanecem e tem esse mesmo plano é de apenas 10%.
- A taxa de churn variou de 5% a 26% com uma média de 14% (± 5%) nos estados americanos.
- California (CA) e Virginia Ocidental(WV) e Carolina do Sul (SC) foram estados problemáticos. CA foi o estado com a segunda maior taxa de churn e o menor número de clientes, talvez reflexo da forte concorrência por se tratar de um dos estados mais populosos do EUA. WV e SC apresentaram um alto número de clientes e uma baixa renda média, o que abre a possibilidade de tentar um pequeno reajuste afim de aumentar a rentabilidade nesses locais.
- Por outro lado Wisconsin (WI) e Virginia (VA) foram estados com alto número de clientes e baixa taxa de churn, mostrando que nesses estados a uma fidelidade interessante. 
- A segmentação dos clientes em grupos confirmou que os clientes rotativos tem um comportamento peculiar que permite diferenciá-los dos ativos.
""")



#to_slider_label = ["Ligações para Atendimento ao Cliente", "Cobrança Total", "Minutos em Chamadas Noturnas",
#"Ligações Internacionais", "Minutos em Chamadas Internacionais"]

   
   
   





