"""
Interface Flask Simples para o Assistente RAG sobre Autismo
Versão ultra-básica e funcional
"""

from flask import Flask, render_template_string, request, jsonify
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.graph.rag_graph import create_rag_graph
except ImportError as e:
    print(f"Erro de import: {e}")
    exit(1)

app = Flask(__name__)

# Carregar sistema RAG
print("Carregando sistema RAG...")
rag_system = create_rag_graph()
print("✅ Sistema RAG carregado!")

# Template HTML simples
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assistente RAG - Autismo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .input-group {
            margin: 20px 0;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #2980b9;
        }
        .response {
            margin-top: 20px;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 5px;
            white-space: pre-wrap;
        }
        .loading {
            text-align: center;
            color: #7f8c8d;
        }
        .examples {
            margin-top: 30px;
        }
        .example-btn {
            background-color: #95a5a6;
            margin: 5px;
            padding: 10px 15px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            color: white;
            font-size: 14px;
        }
        .example-btn:hover {
            background-color: #7f8c8d;
        }
        .warning {
            background-color: #f39c12;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Assistente RAG sobre Autismo</h1>
        <p style="text-align: center; color: #7f8c8d;">
            Sistema de perguntas e respostas sobre Transtorno do Espectro Autista
        </p>
        
        <form id="questionForm">
            <div class="input-group">
                <input type="text" id="question" name="question" 
                       placeholder="Ex: O que é autismo? Quais são os sintomas?" 
                       required>
            </div>
            <button type="submit">🔍 Buscar Resposta</button>
        </form>
        
        <div id="response" class="response" style="display: none;"></div>
        
      
        
        <div class="warning">
            ⚠️ <strong>Importante:</strong> Este sistema é apenas informativo e não substitui consulta médica profissional.
        </div>
    </div>

    <script>
        function setQuestion(question) {
            document.getElementById('question').value = question;
        }
        
        document.getElementById('questionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const question = document.getElementById('question').value;
            const responseDiv = document.getElementById('response');
            
            if (!question.trim()) {
                alert('Por favor, digite uma pergunta.');
                return;
            }
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '<div class="loading">🔄 Processando sua pergunta...</div>';
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({question: question})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    responseDiv.innerHTML = data.response;
                } else {
                    responseDiv.innerHTML = '❌ Erro: ' + data.error;
                }
            } catch (error) {
                responseDiv.innerHTML = '❌ Erro de conexão: ' + error.message;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'success': False, 'error': 'Pergunta vazia'})
        
        # Processar pergunta
        response = rag_system.process_query(question)
        
        return jsonify({
            'success': True, 
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': str(e)
        })

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📱 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)