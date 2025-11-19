from google import genai

# ⚠️ PEGA TU API KEY AQUÍ ABAJO
api_key = "AIzaSyD25MUFU4pxbcziDt4w-SJ8mHyiACbi6XE" 

print("🔍 Escaneando red neuronal de Google...")

try:
    client = genai.Client(api_key=api_key)
    # CORRECCIÓN: Usamos .list() en lugar de .list_models()
    pager = client.models.list() 
    
    print("\n✅ MODELOS AUTORIZADOS:")
    for model in pager:
        # Filtramos para mostrar solo los que generan texto
        print(f" -> {model.name}")
        
except Exception as e:
    print(f"❌ Error: {e}")