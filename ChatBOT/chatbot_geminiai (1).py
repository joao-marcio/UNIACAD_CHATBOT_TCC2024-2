import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import date

GOOGLE_API_KEY='AIzaSyCTawuv8UQ5Q4AacQn1aBQ7BqtXBoZkrn4'
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__) 
CORS(app)
  
@app.route('/date', methods=['GET'])
def get_date():
    return jsonify({'date':  date.today()})
  
"""LISTAR OS MODELOS DISPONÍVEIS"""

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

generation_config = {
    'candidate_count': 1,
    'temperature': 0.5
}

safety_settings = {
    'HARASSMENT': 'BLOCK_NONE',
    'HATE': 'BLOCK_NONE',
    'SEXUAL': 'BLOCK_NONE',
    'DANGEROUS': 'BLOCK_NONE',
}

"""INICIALIZANDO O MODELO"""

def getInfo():
    instituicao = 'Sobre a instituição: Fundado em 1972 como Centro de Ensino Superior de Juiz de Fora (CES/JF), em 2020 tornou-se Centro Universitário Academia (UniAcademia). Atualmente, o UniAcademia oferece cursos de graduação na modalidade presencial - entre bacharelados, licenciaturas e cursos tecnológicos - e pós-graduação. A Instituição conta com três campi em Juiz de Fora: Campus Academia, Campus Arnaldo Janssen e Campus Seminário Santo Antônio. Ao longo de cinco décadas, o UniAcademia traçou caminhos inovadores com a abertura de cursos novos e inexistentes na região.'
    matriz = 'Matriz Curricular: '
    sobre = 'Sobre o curso: O curso de Bacharelado em Sistemas de Informação proporciona um sólido conhecimento em Computação e Administração visando o desenvolvimento e a gestão de soluções baseadas em tecnologia da informação para os processos de negócio das organizações de forma que elas atinjam efetivamente seus objetivos estratégicos de negócio.'
    mapaDeSala = 'Mapa de Sala: '
    corpoDocenteProfessores = 'O Corpo Docente da Uniacademia conta com professores renomados e extremamente qualificados, são eles: Prof. Carlos Alberto Ribeiro, Prof. Daves Marcio Silva Martins, Prof. Evaldo de Oliveira da Silva, Profª. Joseane Pepino de Oliveira, Prof. Robione Antonio Landim, Prof. Tassio Ferenzini Martins Sirqueira, Prof. Christien Lana Rachid, Profª. Débora Marques, Prof. Geraldo Magela Almeida Bessa, Prof. Wesley Carminati Teixeira, Prof. Jacimar Tavares, Prof Marcos Alexandre Miguel'
    localizacao = 'Localização: Rua Halfeld, 1179 - Centro - Juiz de Fora - MG'
    email = 'E-mail: contato@uniacademia.edu.br'
    telefone = 'Telefone: +55 32 3250-3800'
    campi = ''

    f = open("matriz_curricular.csv", "r")
    matriz = matriz + f.read()
    
    f = open("mapa_de_sala.txt", "r")
    mapaDeSala = mapaDeSala + f.read()

    return matriz + ' ' + mapaDeSala + ' ' + corpoDocenteProfessores + ' ' + localizacao + '' + telefone + '' + email + '' + sobre + '' + instituicao
       

def injectText(text):
    prefix = 'A UNIACADEMIA é o antigo CES JF. Só responda a pergunta a seguir se for relacionada a UNIACADEMIA: '
    info = '" Informações auxiliares: "'+ getInfo() + '"'
    return prefix + '"' + text + '" ' + info 

model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                              generation_config=generation_config,
                              safety_settings=safety_settings)

response = model.generate_content("Vamos aprender conteúdo sobre IA. Me dê sugestões")
print(response.text)

chat = model.start_chat(history=[])
@app.route('/process', methods=['POST']) 
def process(): 
    data = request.get_json() 
    originalText = data['value']
    txtToSend = injectText(originalText)
    response = chat.send_message(txtToSend)
    result = response.text
    return jsonify(result=result) 
  
if __name__ == '__main__': 
    app.run(host="0.0.0.0",debug=True) 