from pathlib import Path

import uvicorn

from core.registrar import register_app

app = register_app()



if __name__ == '__main__':
    uvicorn.run(app=f'{Path(__file__).stem}:app', host='127.0.0.1', port=8080, reload=True)
