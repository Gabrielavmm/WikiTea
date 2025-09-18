"""
Servidor HTTP Simples para o Assistente RAG sobre Autismo
Versão ultra-básica usando apenas Python padrão
"""

import http.server
import socketserver
import json
import urllib.parse
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.graph.rag_graph import create_rag_graph
except ImportError as e:
    print(f"Erro de import: {e}")
    exit(1)

# Carregar sistema RAG
print("Carregando sistema RAG...")
rag_system = create_rag_graph()
print("✅ Sistema RAG carregado!")

# HTML simples
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assistente RAG - Autismo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        input[type="text"] { width: 100%; padding: 15px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; margin: 10px 0; }
        button { background-color: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background-color: #2980b9; }
        .response { margin-top: 20px; padding: 20px; background-color: #ecf0f1; border-radius: 5px; white-space: pre-wrap; }
        .example-btn { background-color: #95a5a6; margin: 5px; padding: 10px 15px; border: none; border-radius: 3px; cursor: pointer; color: white; font-size: 14px; }
        .example-btn:hover { background-color: #7f8c8d; }
        .warning { background-color: #f39c12; color: white; padding: 15px; border-radius: 5px; margin-top: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Assistente RAG sobre Autismo</h1>
        <p style="text-align: center; color: #7f8c8d;">Sistema de perguntas e respostas sobre Transtorno do Espectro Autista</p>
        
        <form id="questionForm">
            <input type="text" id="question" name="question" placeholder="Ex: O que é autismo? Quais são os sintomas?" required>
            <button type="submit">🔍 Buscar Resposta</button>
        </form>
        
        <div id="response" class="response" style="display: none;"></div>
        
        <div style="margin-top: 30px;">
            <h3>💡 Exemplos de perguntas:</h3>
            <button class="example-btn" onclick="setQuestion('O que é autismo?')">O que é autismo?</button>
            <button class="example-btn" onclick="setQuestion('Quais são os sintomas do TEA?')">Sintomas do TEA</button>
            <button class="example-btn" onclick="setQuestion('Como funciona o diagnóstico?')">Diagnóstico</button>
            <button class="example-btn" onclick="setQuestion('Quais são as terapias disponíveis?')">Terapias</button>
        </div>
        
        <div class="warning">⚠️ <strong>Importante:</strong> Este sistema é apenas informativo e não substitui consulta médica profissional.</div>
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
            responseDiv.innerHTML = '🔄 Processando sua pergunta...';
            
            try {
                const response = await fetch('/ask?q=' + encodeURIComponent(question));
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

class RAGHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        elif self.path.startswith('/ask'):
            # Extrair pergunta da URL
            query_string = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query_string)
            question = params.get('q', [''])[0]
            
            try:
                if not question.strip():
                    response_data = {'success': False, 'error': 'Pergunta vazia'}
                else:
                    # Processar pergunta
                    answer = rag_system.process_query(question)
                    response_data = {'success': True, 'response': answer}
            except Exception as e:
                response_data = {'success': False, 'error': str(e)}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    PORT = 8000
    
    with socketserver.TCPServer(("", PORT), RAGHandler) as httpd:
        print(f"🚀 Servidor iniciado!")
        print(f"📱 Acesse: http://localhost:{PORT}")
        print(f"📱 Ou: http://127.0.0.1:{PORT}")
        print("Pressione Ctrl+C para parar")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Servidor parado!")