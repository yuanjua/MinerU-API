import requests
import os
import logging
import socket

logging.basicConfig(level=logging.INFO)

# test connection to huggingface
TIMEOUT = 3

def config_endpoint():
    """
    Checks for connectivity to Hugging Face and sets the model source accordingly.
    If the Hugging Face endpoint is reachable, it sets MINERU_MODEL_SOURCE to 'huggingface'.
    Otherwise, it falls back to 'modelscope'.
    """

    os.environ.setdefault('MINERU_MODEL_SOURCE', 'huggingface')
    model_list_url = f'https://huggingface.co/models'
    
    # Use a specific check for the Hugging Face source
    if os.environ['MINERU_MODEL_SOURCE'] == 'huggingface':
        try:
            response = requests.head(model_list_url, timeout=TIMEOUT)
            
            # Check for any successful status code (2xx)
            if response.ok:
                logging.info(f"Successfully connected to Hugging Face. Using 'huggingface' as model source.")
                return True
            else:
                logging.warning(f"Hugging Face endpoint returned a non-200 status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to connect to Hugging Face at {model_list_url}: {e}")

        # If any of the above checks fail, switch to modelscope
        logging.info("Falling back to 'modelscope' as model source.")
        os.environ['MINERU_MODEL_SOURCE'] = 'modelscope'
    
    elif os.environ['MINERU_MODEL_SOURCE'] == 'modelscope':
        try:
            response = requests.head(model_list_url, timeout=TIMEOUT)
            if response.ok:
                logging.info(f"Successfully connected to ModelScope. Using 'modelscope' as model source.")
                return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to connect to ModelScope at {model_list_url}: {e}")
        
    elif os.environ['MINERU_MODEL_SOURCE'] == 'local':
        logging.info("Using 'local' as model source.")
        return True
    
    else:
        logging.error(f"Using custom model source: {os.environ['MINERU_MODEL_SOURCE']}")
        return True
    
    return False

def get_self_ip_address():
    """
    Get the IP address of the current server.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
        s.close()
        return host_ip
    except Exception as e:
        return None

if __name__ == '__main__':
    config_endpoint()
    ip_address = get_self_ip_address()
    print(f"IP address: {ip_address}")
    exit(f"{os.environ['MINERU_MODEL_SOURCE']}")