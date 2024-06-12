import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Simulation discrete",
    page_icon="🌟",  # Optional
    layout="wide",   # This enables wide mode
    initial_sidebar_state="collapsed"  # Optional: "auto", "expanded", "collapsed"
)

st.logo('./interactive.png',icon_image='./interactive.png')

Data = {
    'périodes de normalité' : {
            'Temps en mn':[1, 2, 3, 4, 5, 6],
            'Fréquence en %' : [30, 50, 10, 5, 3, 2]
            } ,
    'périodes de pointes' : {
           'Temps en mn':[0, 1, 2, 3],
           'Fréquence en %' : [15, 30, 40, 15]
           } ,
    'temps de magasinage' : {
           'Temps en mn':[2, 4, 6, 8, 10],
           'Fréquence en %' : [10, 20, 40, 20, 10]
           } ,
    'temps de paiement' : {
           'Temps en mn':[1, 2, 3, 4],
           'Fréquence en %' : [20, 40, 25, 15]
           } ,
}

H1,H2,H3  = st.columns([1.5,3.5,0.5])
H2.title("📑 Projet Simulation ")

st.divider()

l,a,b,r = st.columns([1,2,2,1]) # type: ignore
with a :
        a1,a2  = st.columns([1,2])
        a1.write("Presenté par :")
        a2.markdown('''👨‍🎓 RAOUANE AMINE  
                       👨‍🎓 EL KHOUAKHI AMINE  
                       👨‍🎓 ELHATIMI TOUFIQ  
                       👩‍🎓 MANSOURI ABIR  
                       👩‍🎓 ZAROIL KHADIJA''')
with b :
        b1,b2  = st.columns([1,2])
        b1.write("Encadré par :")
        b2.markdown('👩‍🏫 KHADIJA Ouazzani')

st.divider()


C1,C2,C3  = st.columns([1.5,3.5,0.5])
C2.write("## Tableau de fréquence des temps")

C4,C5 = st.columns(2)
C6,C7 = st.columns(2)

for column , label in zip([C4,C5,C6,C7],Data.keys()):
    column.subheader(label)
    df = pd.DataFrame(Data[label])
    df_transposed = df.T
    df_transposed.columns = [f'Col{i+1}' for i in range(df_transposed.shape[1])]
    column.table(df_transposed)

st.write('Le but de la simulation étant de mesurer l’impact de l’ajout d’une 3ème caisse sur le nombre de clients perdus. Pour cela la simulation sera faite avec 2 caisses et avec 3 caisses.')
st.write("il y a des clients qui ne passent pas par la caisse après le magasinage, car ils n’ont pas trouvé ce qu’ils cherchaient, et par conséquent, n’ont rien acheté.")
