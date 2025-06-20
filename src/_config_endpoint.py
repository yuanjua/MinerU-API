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
    model_list_url = f'https://huggingface.co/models'
    
    # Use a specific check for the Hugging Face source
    if os.environ['MINERU_MODEL_SOURCE'] == 'huggingface':
        try:
            # response = requests.head(model_list_url, timeout=TIMEOUT)
            request = urllib.request.Request(model_list_url, method='HEAD')
            response = urllib.request.urlopen(request, timeout=TIMEOUT)
            
            # Check for any successful status code (2xx)
            if response.ok:
                logging.info(f"Successfully connected to Hugging Face. Using 'huggingface' as model source.")
                return True
            else:
                logging.warning(f"Hugging Face endpoint returned a non-200 status code: {response.status_code}")

        except Exception as e:
            logging.info(f"Failed to connect to Hugging Face at {model_list_url}: {e}")

        # If any of the above checks fail, switch to modelscope
        logging.info("Falling back to 'modelscope' as model source.")
        os.environ['MINERU_MODEL_SOURCE'] = 'modelscope'
    
    elif os.environ['MINERU_MODEL_SOURCE'] == 'modelscope':
        try:
            request = urllib.request.Request(model_list_url, method='HEAD')
            response = urllib.request.urlopen(request, timeout=TIMEOUT)

            if response.ok:
                logging.info(f"Successfully connected to ModelScope. Using 'modelscope' as model source.")
                return True
        except Exception as e:
            logging.info(f"Failed to connect to ModelScope at {model_list_url}: {e}")
        
    elif os.environ['MINERU_MODEL_SOURCE'] == 'local':
        logging.info("Using 'local' as model source.")
        return True
    
    else:
        logging.error(f"Using custom model source: {os.environ['MINERU_MODEL_SOURCE']}")
        return True
    
    return False

if __name__ == '__main__':
    config_endpoint()
    print(os.environ['MINERU_MODEL_SOURCE'])
