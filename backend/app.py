import os
from flask import Flask, Response, request, jsonify
from flask_mongoengine import MongoEngine
from model.model import *
from http import HTTPStatus
from werkzeug.utils import secure_filename
import uuid
from chain.ExtractConversationChain import *
from agent.agents import *
from chatbot.ChatBot import *
from flask_cors import CORS
from flask_restful import Api
app = Flask(__name__)
CORS(app, supports_credentials=True, origin="http://localhost:3000", methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"])
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ['MONGODB_HOST'],
    'username': os.environ['MONGODB_USERNAME'],
    'password': os.environ['MONGODB_PASSWORD'],
    'db': 'webapp'
}

db = MongoEngine()
db.init_app(app)
import os
print(os.getenv("OPENAI_API_KEY"))

@app.route("/api")
def index():
    character = Character(name="chulsoo", appearance='hello', conversations = [])
    character.save()
    return "hello"

# 소설 파일 업로드
@app.route('/files', methods=['POST'])
def upload_file():
    # pdf 파일과 txt 파일만 허용
    allow_extensions = ['pdf', 'txt']
    f = request.files['file']
    # 확장자를 디렉토리 이름으로 사용 
    extension = f.filename.rsplit('.', 1)[1].lower()
    # pdf, txt 파일이 아니면 거부
    if extension not in allow_extensions:
        return jsonify({
                'code':HTTPStatus.BAD_REQUEST, 
                'message':'허용되지 않은 파일입니다.'
        })
        
    directory = 'documents/'
    os.makedirs(directory, exist_ok=True)
    # 저장할 경로 + 파일명
    documentUuid = str(uuid.uuid1())
    
    filename = str(documentUuid)+'.'+extension
    # 디렉토리에 저장
    path = directory +secure_filename(filename)
    f.save(path)
    # mongo db에 문서 정보 저장
    document_name = f.filename.rsplit('.', 1)[0].lower()
    document_url = request.host_url+path
    novel = Novel(name=document_name, url = document_url, uuid = documentUuid)
    novel.save()
    return jsonify({
            'code':HTTPStatus.CREATED, 
            'documentName':document_name,
            'documentUrl':document_url,
            'documentUuid':documentUuid
    })
# 소설 파일 전처리
@app.route('/files/<uuid>/process', methods=['GET'])
def process_document(uuid):
    document_load_and_split(uuid)
    return jsonify({
            'code':HTTPStatus.OK
    })

# 모든 소설 가져오기
@app.route('/novels', methods=['GET'])
def find_all_novels():
    novels = Novel.objects
    return jsonify({
        'novels' : novels
    })
    
# 특정 소설의 정보 가져오기
@app.route('/novels/<id>', methods=['GET'])
def find_novel_by_id(id):
    novel = Novel.objects.get(id=id)
    novelCharacters = NovelCharacter.objects.filter(novel=novel)
    return jsonify({
        'novel' : novel,
        'characters' : novelCharacters
    })
# 대화
@app.route('/chat', methods=['POST'])
def chatting():
    body = request.get_json()
    novel_id = body['novelId']
    character_id = body['characterId']
    query = body['query']
    
    novel = Novel.objects.get(id=novel_id)
    collection = chroma_client.get_or_create_collection(name=novel.uuid, embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        api_key = os.getenv("OPENAI_API_KEY")
    ))
    db = Chroma(
        client = chroma_client,
        collection_name=novel.uuid,
        embedding_function = OpenAIEmbeddings(api_key = os.getenv("OPENAI_API_KEY"))
    )
    retriever = db.as_retriever()
    chatbot = ChatBot(character_id, retriever, novel.name)
    res, url = chatbot.chat(query)

    return jsonify({
        'res' : res,
        'imageUrl' : url
    })
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)