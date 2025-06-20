import urllib.request
import os
import logging

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
    hf_endpoint = 'https://huggingface.co/models'
    mc_endpoint = 'https://modelscope.cn/models'
    
    # Use a specific check for the Hugging Face source
    if os.environ['MINERU_MODEL_SOURCE'] == 'huggingface':
        try:
            # response = requests.head(model_list_url, timeout=TIMEOUT)
            request = urllib.request.Request(hf_endpoint, method='HEAD')
            response = urllib.request.urlopen(request, timeout=TIMEOUT)
            
            # Check for any successful status code (2xx)
            if 200 <= response.status < 300:
                logging.info(f"Successfully connected to {hf_endpoint} (Status: {response.status}).")
                return True
            else:
                logging.warning(f"Hugging Face endpoint returned a non-200 status code: {response.status}")

        except Exception as e:
            logging.info(f"Failed to connect to Hugging Face at {hf_endpoint}: {e}")

        # If any of the above checks fail, switch to modelscope
        logging.info("Falling back to 'modelscope' as model source.")
        os.environ['MINERU_MODEL_SOURCE'] = 'modelscope'
    
    elif os.environ['MINERU_MODEL_SOURCE'] == 'modelscope':
        try:
            request = urllib.request.Request(mc_endpoint, method='HEAD')
            response = urllib.request.urlopen(request, timeout=TIMEOUT)

            if 200 <= response.status < 300:
                logging.info(f"Successfully connected to {mc_endpoint} (Status: {response.status}).")
                return True
        except Exception as e:
            logging.info(f"Failed to connect to ModelScope at {mc_endpoint}: {e}, please check your internet connection.")
        
    elif os.environ['MINERU_MODEL_SOURCE'] == 'local':
        logging.info("Using 'local' as model source.")
        return True
    
    else:
        logging.error(f"{os.environ['MINERU_MODEL_SOURCE']} not in ['huggingface', 'modelscope', 'local']")
    
    return False

if __name__ == '__main__':
    config_endpoint()
    print(os.environ['MINERU_MODEL_SOURCE'])
