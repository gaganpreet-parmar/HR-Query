from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from askQuestionWithPrompt import retrieveDb

app = Flask(__name__)
auth = HTTPBasicAuth()
chat_history=[]

# Dummy user credentials (replace with your actual credentials)
users = {
    'username': 'password1',
}

@auth.verify_password
def verify_password(username, password):
    return users.get(username) == password

@app.route('/api/resource', methods=['POST'])
@auth.login_required
def create_resource():
    try:
        data = request.get_json(force=True)
        resource_id = data['id']
        content = data['content']
        storeName = data.get('storename',None)

        question=content
        qa=retrieveDb("stuff", 3,"voice")
        result = qa({"question": question, "chat_history": chat_history})
        chat_history.extend([(f"Human: {question}", f"AIMessage: {result['answer']}")])
        result_data = result["answer"]
        print(f"****************************{chat_history}*************************")
        message = {
        "id": resource_id,
        "result": result_data
        }
        
        response = {
            'status': 'success',
            'message': message
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }
        return jsonify(response), 400

if __name__ == '__main__':
    app.run(port=9091,debug=True)
