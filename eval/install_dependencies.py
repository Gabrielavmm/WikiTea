import subprocess
import sys
import os

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {package}: {e}")
        return False

def main():
    print("🚀 Instalando dependências para avaliação RAGAS...")
    
    packages = [
        "ragas>=0.1.0",
        "datasets>=2.14.0",
        "openai>=1.3.0",
        "langchain>=0.3.0",
        "langchain-openai>=0.0.2",
        "chromadb>=1.0.0",
        "sentence-transformers>=2.2.0"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Resultado: {success_count}/{len(packages)} pacotes instalados")
    
    if success_count == len(packages):
        print("✅ Todas as dependências foram instaladas com sucesso!")
        print("Execute: python eval/rag_evaluation.py")
    else:
        print("⚠️ Algumas dependências falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main()