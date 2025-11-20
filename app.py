import os
import json
import hvac 

def get_secret():
    secret_key = "DB_PASSWORD"
    
    try:
        client = hvac.Client(url='http://127.0.0.1:8200', token='root')
        

        read_response = client.secrets.kv.v2.read_secret_version(path='myapp')
        vault_secret = read_response['data']['data'].get(secret_key)
        
        if vault_secret:
            print(f"✅ [Source: HashiCorp Vault] Found secret!")
            return vault_secret
    except Exception as e:
      
        print(f"⚠️ Could not connect to Vault (Is it running?): {e}")

    if secret_key in os.environ:
        print(f"⚠️ [Source: Environment Variable] Found secret!")
        return os.environ[secret_key]
        
    elif os.path.exists("config.json"):
        print(f"❌ [Source: Config File] Found secret in config.json")
        with open("config.json", "r") as f:
            data = json.load(f)
            return data.get(secret_key)
            
    return None

if __name__ == "__main__":
    print("--- Starting Secure App ---")
    secret = get_secret()
    
    if secret:
        print(f"🔓 The Final Secret is: {secret}")
    else:
        print("❌ Error: No secret found anywhere!")