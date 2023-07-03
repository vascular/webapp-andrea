
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
#from matplotlib import pyplot as plt



import datetime 
import streamlit as st
st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["ENTRADA", "RESULTADOS"])


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1ScVtYHJiJtt55tf5tPowPqgJFBukdAwMtG3uv0GT2-o'
SAMPLE_RANGE_NAME = 'Página1!A1:Z'
creds = None


############################################
### AUTH E CONECT SHEETS 
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


if __name__ == '__main__':
    main()
################################################

creds = Credentials.from_authorized_user_file('token.json', SCOPES) #credenciais e serviço do sheets
service = build('sheets', 'v4', credentials=creds)
  # Call the Sheets API
sheet = service.spreadsheets()

############################################ STREAMLIT


novaLinha=[[]]


#data de hoje
#LISTAS PARA SELEÇÃO---------

#DATAS
today = datetime.date.today()
mes = today.month
diaSemana = today.weekday() #Monday is 0 and Sunday is 6
diaSemanaText=""
#converte p texto dia da semana para evitar incompatibilidade com google sheets ( numeros dos dias diferentes)
if ( diaSemana == 0):diaSemanaText = "segunda-feira"
if ( diaSemana == 1):diaSemanaText = "terça-feira"
if ( diaSemana == 2):diaSemanaText = "quarta-feira"
if ( diaSemana == 3):diaSemanaText = "quinta-feira"
if ( diaSemana == 4):diaSemanaText = "sexta-feira"
if ( diaSemana == 5):diaSemanaText = "sábado"
if ( diaSemana == 6):diaSemanaText = "domingo"


ano = today.year

#LISTA DE OPÇÕES 
FaixaEtaria= ['','0 a 1','2 a 3','3 a 5','5 a 18']
Sexo=['M','F']
modoPagamento=['PIX','Dinheiro']

with tab1:
    st.title("WEBAPP INOVACLIN -  DRA ANDREA")
    #####---------------------------
    optionFaixaEtaria = st.selectbox(
        'FAIXA ETÁRIA : ',
        FaixaEtaria)

    optionSexo = st.selectbox(
        'Sexo : ',
        Sexo)

    valor = st.number_input("Valor :",min_value=0,)

    optionModoPag = st.selectbox(
        'Modo de Pagamento : ',
        modoPagamento)
    #####-----------------------

    novaLinha=[[str(today),optionFaixaEtaria,optionSexo,float(valor),optionModoPag,mes,diaSemanaText,ano]]

    if st.button('Grava'):
        escreve = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Página1!A2:E",
                                        valueInputOption = "USER_ENTERED", insertDataOption = "INSERT_ROWS",
                                        body = {"values":novaLinha} ).execute()

        
    'novaLinha: ', novaLinha
    
    

with tab2:
    #'RESULTADOS: POR ANO , POR MES , POR FAIXA ETARIA E SEXO , POR DIA DA SEMANA '
    
    #valor da celula J1 - total do dia - função sumif do google sheets 
    hoje = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Página1!J1").execute()
    hoje = hoje.get('values',[])
    
    #valor da celula resultados!f2 - soma do dia 
    fatHoje = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Resultados!F2").execute()
    fatHoje = fatHoje.get('values',[])
    
    #valor da celula resultados!f3 - soma do mes
    fatMes = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Resultados!F3").execute()
    fatMes = fatMes.get('values',[])
    
    #valor da celula resultados!f4 - soma do ano
    fatAno = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Resultados!F4").execute()
    fatAno = fatAno.get('values',[])
    
    #st.write(hoje[0][0] )
    st.write("HOJE : ",fatHoje[0][0])
    st.write("ESTE MÊS : ",fatMes[0][0])
    st.write("ESTE ANO : ",fatAno[0][0])
    
                        
        
    