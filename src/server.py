import os
import uuid
import base64
import argparse
from pathlib import Path
import litserve as ls
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from loguru import logger

from mineru.cli.common import do_parse
from mineru.utils.config_reader import get_device
from mineru.utils.model_utils import get_vram
from _config_endpoint import config_endpoint
from _file_utils import scheduler_service, flatten_folder, zip_folder
from contextlib import asynccontextmanager

FILE_OUTPUT_DIR = Path(__file__).parent / 'output'

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the application.
    """
    from contextlib import AsyncExitStack
    async with AsyncExitStack() as stack:
        scheduler = await stack.enter_context(scheduler_service(FILE_OUTPUT_DIR))
        yield

class MinerUAPI(ls.LitAPI):
    def __init__(self):
        super().__init__()
        self.output_dir = FILE_OUTPUT_DIR

    def setup(self, device):
        """Setup environment variables exactly like MinerU CLI does"""
        logger.info(f"Setting up on device: {device}")
                
        if os.getenv('MINERU_DEVICE_MODE', None) == None:
            os.environ['MINERU_DEVICE_MODE'] = device if device != 'auto' else get_device()

        device_mode = os.environ['MINERU_DEVICE_MODE']
        if os.getenv('MINERU_VIRTUAL_VRAM_SIZE', None) == None:
            if device_mode.startswith("cuda") or device_mode.startswith("npu"):
                vram = round(get_vram(device_mode))
                os.environ['MINERU_VIRTUAL_VRAM_SIZE'] = str(vram)
            else:
                os.environ['MINERU_VIRTUAL_VRAM_SIZE'] = '1'
        logger.info(f"MINERU_VIRTUAL_VRAM_SIZE: {os.environ['MINERU_VIRTUAL_VRAM_SIZE']}")

    def decode_request(self, request):
        """Decode file and options from request"""
        file_b64 = request['file']
        file_key = request.get('file_key', None)
        options = request.get('options', {})
        
        file_bytes = base64.b64decode(file_b64)
        
        return {
            'pdf_bytes': file_bytes,
            'file_key': file_key if file_key else str(uuid.uuid4()),
            # === MinerU Custom Options ===
            'backend': options.get('backend', 'pipeline'),
            'method': options.get('method', 'auto'),
            'lang': options.get('lang', 'ch'),
            'formula_enable': options.get('formula_enable', True),
            'table_enable': options.get('table_enable', True),
            'start_page_id': options.get('start_page_id', 0),
            'end_page_id': options.get('end_page_id', None),
            'server_url': options.get('server_url', None),
        }

    def predict(self, inputs):
        """Call MinerU's do_parse - same as CLI"""
        file_key = inputs['file_key']
        pdf_bytes = inputs['pdf_bytes']
        output_dir = self.output_dir / file_key

        logger.info(f"Processing file: {file_key}, output_dir: {output_dir}")
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            do_parse(
                output_dir=str(output_dir),
                pdf_file_names=['file'],
                pdf_bytes_list=[pdf_bytes],
                p_lang_list=[inputs['lang']],
                backend=inputs['backend'],
                parse_method=inputs['method'],
                p_formula_enable=inputs['formula_enable'],
                p_table_enable=inputs['table_enable'],
                server_url=inputs['server_url'],
                start_page_id=inputs['start_page_id'],
                end_page_id=inputs['end_page_id']
            )
            flatten_folder(output_dir, levels=2)
            return str(output_dir)
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def encode_response(self, response):
        output_dir = Path(response)
        
        zip_folder(output_dir, output_dir / "all")
        return {
            'dir_path': str(output_dir),
            'markdown_route': f"/download/{output_dir.name}/file.md",
            'zipfile_route': f"/download/{output_dir.name}/all.zip"
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=24008)
    args = parser.parse_args()

    if not os.getenv('MINERU_MODEL_SOURCE', None):
        config_endpoint()
    logger.info(f"Using model source: {os.environ['MINERU_MODEL_SOURCE']}")

    server = ls.LitServer(
        MinerUAPI(),
        accelerator='auto',
        devices='auto',
        workers_per_device=1,
        timeout=False
    )
    logger.info(f"Serving parsed files from {FILE_OUTPUT_DIR}")
    os.makedirs(FILE_OUTPUT_DIR, exist_ok=True)
    server.app.mount("/download", StaticFiles(directory=FILE_OUTPUT_DIR), name="download")

    logger.info(f"Starting MinerU server on port {args.port}")
    server.run(port=args.port, generate_client_file=False) 