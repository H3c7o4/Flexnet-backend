from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from .models import Base
from .database import engine
from .routers import user, authentication, movie, score
import requests

from starlette.responses import JSONResponse

app = FastAPI(title='Flexnet API', version='V1.0.0')

Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(movie.router)
app.include_router(score.router)

@app.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def hello_world():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Welcome to flexnet API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f1f1f1;
                    margin: 0;
                    padding: 20px;
                }

                h1 {
                    color: #333;
                    margin-bottom: 20px;
                }

                p {
                    color: #555;
                    margin-bottom: 10px;
                }

                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to our API</h1>
                <p>Thank you for visiting our API. We look forward to welcoming you.</p>
                <p>You can use our API to obtain data, perform operations, etc.</p>
                <p>If you have any questions or need help, please don't hesitate to contact us.</p>
                <p>Go to <b><em>../docs</em></b> to see the swagger</p>
            </div>
        </body>
    </html>
    """


@app.get('/bye', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def good_bye():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Goodbye!</title>
            <style>
                body {
                    background-color: #f7d4c8;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }

                h1 {
                    color: #2e4053;
                    margin-top: 50px;
                }

                p {
                    color: #2e4053;
                    font-size: 18px;
                }

                .image {
                    margin-top: 50px;
                    display: flex;
                    justify-content: center;
                }

                .message {
                    margin-top: 30px;
                    color: #34495e;
                    font-size: 20px;
                }

                .emoji {
                    font-size: 40px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Goodbye!</h1>

            <p>Thank you for visiting our API.</p>

            <div class="image">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQn3vtqryBF7AWKVnkyllmBOLRbCYRbn-rY4HBUWL2-&s" alt="Beautiful Image" width="300" height="200">
            </div>

            <div class="message">
                <p>Have a great day ahead and remember:</p>

                <p> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler</p>

                <span class="emoji">&#128075;</span>
            </div>
        </body>
        </html>
    """
