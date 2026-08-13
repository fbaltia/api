import uvicorn
from fastapi import FastAPI, staticfiles

import controllers
from utils.application_utils import load_routers

# créer une instance de FastAPI
app = FastAPI()

app.mount('/public', staticfiles.StaticFiles(directory='static'))

# charger tous les router se trouvant dans controllers
load_routers(app, controllers)

if __name__ == '__main__':
    # exposer FastAPI sur le port 8000
    uvicorn.run(
        'server:app', 
        host='127.0.0.1',
        port=8000,
        reload=True
    )
